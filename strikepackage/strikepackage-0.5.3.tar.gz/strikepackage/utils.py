import sys
import os
import re
import uuid

import hipchat


def abort(errstr, errcode=1):
    sys.stderr.write("\nERROR: {}\n".format(errstr))
    sys.exit(errcode)


def warn(warnstr):
    sys.stderr.write("\nWARNING: {}\n".format(warnstr))


def select_xs_item(options):
    choice = None
    xs_item = None
    for i, rec in enumerate(options, start=1):
        print "[{}] {}".format(i, rec[0])
    while choice is None:
        try:
            choice = int(raw_input("Select a number: "))
            xs_item = options[choice-1]
        except (ValueError, IndexError):
            choice = None
    return xs_item


def validate_ip(ip):
    a = ip.split('.')
    if len(a) != 4:
        return False
    for x in a:
        if not x.isdigit():
            return False
        i = int(x)
        if i < 0 or i > 255:
            return False
    return True


def validate_hostname(hostname):
    if len(hostname) > 255:
        return False
    allowed = re.compile("^(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    if allowed.match(hostname):
        return True
    return False


def review_choices(params, config):
    """ Print out a summary screen from params """
    os.system('clear')
    print "=====PARAMETER REVIEW====="
    print "Instance ID: {}".format(params['iid'])
    print "MCHM URL: {}\n".format(params['mchm_vm_url'])

    print "---XenServer---"
    print "Pool Master: {} ({})".format(
        params['poolmaster'][0], params['poolmaster'][1])
    print "Template: {} ({})".format(
        params['template'][0], params['template'][1])
    print "Network: {} ({})\n".format(
        params['network'][0], params['network'][1])

    print "---VM Network---"
    print "Hostname: {}".format(params['hostname'])
    print "FQDN: {}".format(params['fqdn'])

    # MCHM stuff
    if config['mchm_enable']:
        print "DHCP: {}".format(params['dhcp'])
        if not params['dhcp']:
            print "IP: {}".format(params['ip'])
            print "Netmask: {}".format(params['netmask'])
            print "Gateway: {}".format(params['gw'])
            print "Network: {}".format(params['nw'])
            print "Broadcast: {}".format(params['broadcast'])
            print "DNS servers: {}".format(params['dns_servers'])
            print "DNS search domain: {}".format(params['dns_searchdomain'])

    confirmed = False
    while not confirmed:
        choice = raw_input('\nDeploy? [Y/N]: ')
        if choice.lower() == 'y' or choice.lower() == 'yes':
            confirmed = True
        else:
            print 'Enter "y" or "yes" to deploy. CTRL+C to quit.'


def get_network_details(config):
    dhcp = False
    hostname = ''
    ip = ''
    gw = ''
    nw = ''
    netmask = ''
    broadcast = ''
    domain_suffix = '.' + config['dns_searchdomain']

    # get hostname and set fqdn
    while hostname == '':
        proposal = raw_input("Enter hostname for new VM: ")
        if domain_suffix in proposal:
            proposal = proposal.replace(domain_suffix, '')
        if validate_hostname(proposal):
            hostname = proposal
    fqdn = "{}{}".format(hostname, domain_suffix)

    # If MCHM is disabled, then we're done here
    if not config['mchm_enable']:
        return {
            'hostname': hostname.lower(),
            'fqdn': fqdn.lower(),
            'ip': ip,
            'nw': nw,
            'netmask': netmask,
            'broadcast': broadcast,
            'gw': gw,
            'dns_servers': config['dns_serverstring'],
            'dns_searchdomain': config['dns_searchdomain'],
            'dhcp': dhcp
        }

    while True:
        use_dhcp = raw_input('Does this template use DHCP? [Y/N]: ').lower()
        if use_dhcp == 'y':
            dhcp = True
            break
        elif use_dhcp == 'n':
            break
        else:
            print 'Enter "y" or "n".\n'

    # get ip, network, netmask and broadcast network if not DHCP
    if not dhcp:
        while not validate_ip(ip):
            ip = raw_input("Enter IP for new host: ")
        nw = (ip.rpartition('.')[0])+'.0'
        netmask = '255.255.255.0'
        broadcast = (ip.rpartition('.')[0])+'.255'

        # set gateway
        gw_proposal = (ip.rpartition('.')[0])+'.1'
        while not validate_ip(gw):
            gw = raw_input("Enter gateway. "
                           "Leave blank for default [{}]: ".format(gw_proposal))
            if gw == '':
                gw = gw_proposal

    return {
        'hostname': hostname.lower(),
        'fqdn': fqdn.lower(),
        'ip': ip,
        'nw': nw,
        'netmask': netmask,
        'broadcast': broadcast,
        'gw': gw,
        'dns_servers': config['dns_serverstring'],
        'dns_searchdomain': config['dns_searchdomain'],
        'dhcp': dhcp
    }


def get_params(session, config):
    """ gathers parameters """

    # get pool data
    poolref = session.xenapi.pool.get_all_records()
    if len(poolref) > 1:
        abort("Multiple pools returned by XenAPI. Strikepackage does not "
              "support this scenario.")
    poolrec = poolref.popitem()[1]
    pm_rec = session.xenapi.host.get_record(poolrec['master'])
    poolmaster = (pm_rec['name_label'], pm_rec['uuid'])

    # get a list of strikepackage tagged xenserver templates
    vms = session.xenapi.VM.get_all_records()
    template_list = [(rec['name_label'], rec['uuid'])
                     for ref, rec in vms.iteritems()
                     if (config['sp_tag'] in rec['tags']
                         and rec['is_a_template'] is True
                         and rec['is_a_snapshot'] is False)]
    if len(template_list) < 1:
        abort("No templates found.")

    # get a list of xenserver networks
    nws = session.xenapi.network.get_all_records()
    network_list = [(rec['name_label'], rec['uuid'])
                    for ref, rec in nws.iteritems()]
    if len(network_list) < 1:
        abort("No networks found.")

    # user menus
    os.system('clear')
    print "Available templates:\n"
    template = select_xs_item(sorted(template_list, key=lambda n: n[0]))

    os.system('clear')
    print "Available networks:\n"
    network = select_xs_item(sorted(network_list, key=lambda n: n[0]))

    os.system('clear')
    print "Enter VM network details:\n"
    params = get_network_details(config)

    # add other params to dict
    params['network'] = network
    params['template'] = template
    params['poolmaster'] = poolmaster
    params['iid'] = uuid.uuid4().hex
    params['rand_pass'] = "{}{}".format(uuid.uuid4().hex, uuid.uuid4().hex)
    params['mchm_vm_url'] = "N/A"  # defaults to N/A

    return params


def hipchat_notification(config, msg, color='green'):
    try:
        hc = hipchat.HipChat(token=config['hipchat_api_token'])
        payload = {
            'room_id': config['hipchat_roomid'],
            'from': config['hipchat_from'],
            'message': msg,
            'color': color
        }
        hc.method('rooms/message', method='POST', parameters=payload)
    except (ValueError, IOError) as ex:
       warn("Error sending hipchat notification: {}".format(ex))