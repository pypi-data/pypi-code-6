#!/bin/python3

#1.3.6.1.4.1.9.9.399
#1.3.6.1.4.1.9.9.394

from pysnmp.entity.rfc3413.oneliner import cmdgen
from pysnmp.proto import rfc1902
import ipaddress


cmdGen = cmdgen.CommandGenerator()
target = '0.0.0.0'
security = ''


def is_ipv4(ip, txt):
    try:
        ipaddress.IPv4Address(ip)
        rc = 1
    except ValueError:
        print('ERROR: %s not a valid IPv4 address' % (txt))
        rc = 0

    return rc


def is_ipv6(ip, txt):
    try:
        ipaddress.IPv6Address(ip)
        rc = 1
    except ValueError:
        print('ERROR: %s not a valid IPv6 address' % (txt))
        rc = 0

    return rc


def is_int_range(x, low, high, txt):
    if x.isdigit():
        if int(x) >= low and int(x) <= high:
            return 1
        else:
            print('ERROR: %s not in valid range: <%s-%s>' % (txt, low, high))
            return 0
    else:
        print('ERROR: %s not in right format: <int>, range: <%s-%s>' % (txt, low, high))
        return 0


def is_str_length(x, low, txt):
    if len(x) >= low:
        rc = 1
    else:
        print('\nERROR: %s min length = %s' % (txt, low))
        rc = 0

    return rc


def set_target():
    global target

    while True:
        ip = input('\nEnter IP          : ')

        if is_ipv4(ip, ip):
            target = ip
            break


def print_walk(errorIndication, errorStatus, errorIndex, varBinds):
    global target

    print(' ')
    if errorIndication:
        print('(%s) : errorIndication = %s' % (
            target,
            errorIndication
        )
        )
        if str(errorIndication) == 'No SNMP response received before timeout':
            print('\nPlease verify:')
            print('1. Target IP is correct.')
            print('2. Target IP is reachable.')
            print('3. LI and SNMPv3 are active on the target router.')
        if str(errorIndication) == 'unknownUserName':
            print('\nPlease verify:')
            print('1. SNMPV3 credentials are correct.')
            print('2. SNMPV3 is enabled on target router.')
    else:
        if errorStatus:
            print('RX (%s) : errorStatus = %s at %s' % (
                target,
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1] or '?'
            )
            )
        else:
            for elem in varBinds:
                for name, val in elem:
                    print('RX (%s) : %s = %s' % (target, name.prettyPrint(), val.prettyPrint()))


def print_response(errorIndication, errorStatus, errorIndex, varBinds):
    global target

    print(' ')
    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print('RX (%s) : errorStatus = %s at %s' % (
                target,
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1] or '?'
            )
            )
        else:
            for elem in varBinds:
                name = elem[0]
                val = elem[1]
                print('RX (%s) : %s = %s' % (target, name.prettyPrint(), val.prettyPrint()))


def print_set(oids):
    global target

    print('')
    for elem in oids:
        print('TX (%s) : %s' % (target, elem))


def send_walk(OID):
    global target

    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.nextCmd(
        security,
        cmdgen.UdpTransportTarget((target, 161)),
        OID
    )
    print_walk(errorIndication, errorStatus, errorIndex, varBinds)


def send_set(oids):
    global target
    print_set(oids)

    ## Need this check, because setting single OID single 'tuple', not 'tuple' of tuples

    if type(oids[0]) == tuple:
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
            security,
            cmdgen.UdpTransportTarget((target, 161)),
            *oids
        )
    elif type(oids[0]) == str:
        errorIndication, errorStatus, errorIndex, varBinds = cmdGen.setCmd(
            security,
            cmdgen.UdpTransportTarget((target, 161)),
            oids
        )

    print_response(errorIndication, errorStatus, errorIndex, varBinds)


def walk_mibs():

    if not check_config():
        return

    print('\nPolling: ciscoTap2MIB')
    send_walk('1.3.6.1.4.1.9.9.399')

    print('\nPolling: ciscoIpTapMIB')
    send_walk('1.3.6.1.4.1.9.9.394')


def create_md(*args):
    ip = args[0].split('.')
    hex_ip = "".join([hex(int(value))[2:].zfill(2) for value in ip])
    hex_ip = hex_ip.replace('0x', '')
    hex_ip = hex_ip.upper()

    oids = (
        ('1.3.6.1.4.1.9.9.399.1.1.2.1.2.' + args[5], rfc1902.Integer(1)),
        ('1.3.6.1.4.1.9.9.399.1.1.2.1.3.' + args[5], rfc1902.OctetString(hexValue=hex_ip)),
        ('1.3.6.1.4.1.9.9.399.1.1.2.1.4.' + args[5], rfc1902.Unsigned32(args[1])),
        ('1.3.6.1.4.1.9.9.399.1.1.2.1.5.' + args[5], rfc1902.Integer(args[2])),
        ('1.3.6.1.4.1.9.9.399.1.1.2.1.7.' + args[5], rfc1902.Integer(args[3])),
        ('1.3.6.1.4.1.9.9.399.1.1.2.1.10.' + args[5], rfc1902.OctetString(hexValue=args[4])),
        ('1.3.6.1.4.1.9.9.399.1.1.2.1.11.' + args[5], rfc1902.Integer(1)),
        ('1.3.6.1.4.1.9.9.399.1.1.2.1.13.' + args[5], rfc1902.Integer(4))
    )
    send_set(oids)


def remove_md(cccid):
    oids = (
        ('1.3.6.1.4.1.9.9.399.1.1.2.1.13.' + cccid, rfc1902.Integer(6))
    )
    send_set(oids)


def create_tap_v4(cccid, dPref, dPrefLen, sPref, sPrefLen, tap):
    d_ip = dPref.split('.')
    hex_d_ip = "".join([hex(int(value))[2:].zfill(2) for value in d_ip])
    hex_d_ip = hex_d_ip.replace('0x', '')
    hex_d_ip = hex_d_ip.upper()

    s_ip = sPref.split('.')
    hex_s_ip = "".join([hex(int(value))[2:].zfill(2) for value in s_ip])
    hex_s_ip = hex_s_ip.replace('0x', '')
    hex_s_ip = hex_s_ip.upper()

    oids = (
        ('1.3.6.1.4.1.9.9.394.1.1.2.1.1.' + cccid + '.' + tap, rfc1902.Integer(0)),
        ('1.3.6.1.4.1.9.9.394.1.1.2.1.2.' + cccid + '.' + tap, rfc1902.Integer(1)),
        ('1.3.6.1.4.1.9.9.394.1.1.2.1.3.' + cccid + '.' + tap, rfc1902.OctetString(hexValue=hex_d_ip)),
        ('1.3.6.1.4.1.9.9.394.1.1.2.1.4.' + cccid + '.' + tap, rfc1902.Unsigned32(int(dPrefLen))),
        ('1.3.6.1.4.1.9.9.394.1.1.2.1.5.' + cccid + '.' + tap, rfc1902.OctetString(hexValue=hex_s_ip)),
        ('1.3.6.1.4.1.9.9.394.1.1.2.1.6.' + cccid + '.' + tap, rfc1902.Unsigned32(int(sPrefLen))),
        ('1.3.6.1.4.1.9.9.394.1.1.2.1.7.' + cccid + '.' + tap, rfc1902.Integer(0)),
        ('1.3.6.1.4.1.9.9.394.1.1.2.1.8.' + cccid + '.' + tap, rfc1902.Integer(0)),
        ('1.3.6.1.4.1.9.9.394.1.1.2.1.16.' + cccid + '.' + tap, rfc1902.Integer(4))
    )
    send_set(oids)


def create_tap_v6(cccid, dPref, dPrefLen, sPref, sPrefLen, tap):
    hex_d_ip = ('').join(dPref.split(':'))
    hex_s_ip = ('').join(sPref.split(':'))

    oids = (
        ('1.3.6.1.4.1.9.9.394.1.1.2.1.1.' + cccid + '.' + tap, rfc1902.Integer(0)),
        ('1.3.6.1.4.1.9.9.394.1.1.2.1.2.' + cccid + '.' + tap, rfc1902.Integer(2)),
        ('1.3.6.1.4.1.9.9.394.1.1.2.1.3.' + cccid + '.' + tap, rfc1902.OctetString(hexValue=hex_d_ip)),
        ('1.3.6.1.4.1.9.9.394.1.1.2.1.4.' + cccid + '.' + tap, rfc1902.Unsigned32(int(dPrefLen))),
        ('1.3.6.1.4.1.9.9.394.1.1.2.1.5.' + cccid + '.' + tap, rfc1902.OctetString(hexValue=hex_s_ip)),
        ('1.3.6.1.4.1.9.9.394.1.1.2.1.6.' + cccid + '.' + tap, rfc1902.Unsigned32(int(sPrefLen))),
        ('1.3.6.1.4.1.9.9.394.1.1.2.1.7.' + cccid + '.' + tap, rfc1902.Integer(0)),
        ('1.3.6.1.4.1.9.9.394.1.1.2.1.8.' + cccid + '.' + tap, rfc1902.Integer(0)),
        ('1.3.6.1.4.1.9.9.394.1.1.2.1.16.' + cccid + '.' + tap, rfc1902.Integer(4))
    )
    send_set(oids)


def activate_tap(cccid, tap):
    oids = (
        ('1.3.6.1.4.1.9.9.399.1.2.1.1.2.' + cccid + '.' + tap, rfc1902.Integer(1)),
        ('1.3.6.1.4.1.9.9.399.1.2.1.1.3.' + cccid + '.' + tap, rfc1902.Integer(2)),
        ('1.3.6.1.4.1.9.9.399.1.2.1.1.6.' + cccid + '.' + tap, rfc1902.Integer(4))
    )
    send_set(oids)


def remove_tap():
    cccid = input('Enter CCCid to remove: ')

    oids = (
        ('1.3.6.1.4.1.9.9.399.1.2.1.1.6.' + cccid + '.1', rfc1902.Integer(6)),
        ('1.3.6.1.4.1.9.9.399.1.2.1.1.6.' + cccid + '.2', rfc1902.Integer(6))
    )
    send_set(oids)

    oids = (
        ('1.3.6.1.4.1.9.9.394.1.1.2.1.16.' + cccid + '.1', rfc1902.Integer(6)),
        ('1.3.6.1.4.1.9.9.394.1.1.2.1.16.' + cccid + '.2', rfc1902.Integer(6))
    )
    send_set(oids)

    remove_md(cccid)


def insert_data_md():
    # Define Mediation Device
    md_ip = input('\nMediation Device IP          : ')
    md_port = input('Mediation Device Port        : ')
    md_source = input('Mediation Source Int         : ')
    md_dscp = input('Mediation DSCP               : ')
    cccid = input('CCCid                        : ')

    print('Mediation Timeout (Max 24 days + 1 hour) : ')
    md_year = input('   MD Year     : ')
    md_month = input('   MD Month    : ')
    md_day = input('   MD Day      : ')

    md_timeout = construct_timeout(md_year, md_month, md_day)

    return (md_ip, md_port, md_source, md_dscp, md_timeout, cccid)


def construct_timeout(md_year, md_month, md_day):
    rc_year = 0
    rc_month = 0
    rc_day = 0

    if (is_int_range(md_year, 2014, 2100, 'MD Year') == 0):
        rc_year = 1
    if (is_int_range(md_month, 1, 12, 'MD Month') == 0):
        rc_month = 1
    if (is_int_range(md_day, 1, 31, 'MD Day') == 0):
        rc_day = 1

    if (rc_year == 0 and rc_month == 0 and rc_day == 0):
        hex_year = '0x%04x' % (int(md_year))
        hex_month = '0x%02x' % (int(md_month))
        hex_day = '0x%02x' % (int(md_day))
        print('\nMD Timeout will be set to: %s-%s-%s 23:59' % (md_year, md_month, md_day))
        return ('%s%s%s173B0000' % (hex_year.upper()[2:], hex_month.upper()[2:], hex_day.upper()[2:]))
    else:
        return (0)


def insert_data_tap(id):
    # Define Tap
    dPref = input('Tap' + id + ' Dest. Prefix            : ')
    dPrefLen = input('Tap' + id + ' Dest. Prefix Length     : ')
    sPref = input('Tap' + id + ' Source Prefix           : ')
    sPrefLen = input('Tap' + id + ' Source Prefix Length    : ')

    return (dPref, dPrefLen, sPref, sPrefLen)


def verify_data_md(md_ip, md_port, md_source, md_dscp, md_timeout, cccid):
    rc = 0
    print('')

    if is_ipv4(md_ip, 'MD IP') == 0:
        rc = 1
    if is_int_range(md_port, 1025, 65535, 'MD PORT') == 0:
        rc = 1
    if is_int_range(md_source, 0, 2000000, 'MD SOURCE INT') == 0:
        rc = 1
    if is_int_range(md_dscp, 0, 63, 'MD DSCP') == 0:
        rc = 1
    if md_timeout == 0:
        rc = 1
    if is_int_range(cccid, 1, 2000000, 'CCCid') == 0:
        rc = 1

    return (rc)


def verify_data_tap(dPref, dPrefLen, sPref, sPrefLen, prot):
    rc = 0
    print('')

    if prot == 'ipv4':
        if is_ipv4(dPref, 'Dest. Prefix') == 0:
            rc = 1
        if is_ipv4(sPref, 'Source Prefix') == 0:
            rc = 1
        if is_int_range(dPrefLen, 0, 32, 'Dest. Pref Len') == 0:
            rc = 1
        if is_int_range(sPrefLen, 0, 32, 'Source Pref Len') == 0:
            rc = 1
    elif prot == 'ipv6':
        if is_ipv6(dPref, 'Dest. Prefix') == 0:
            rc = 1
        if is_ipv6(sPref, 'Source Prefix') == 0:
            rc = 1
        if is_int_range(dPrefLen, 0, 128, 'Dest. Pref Len') == 0:
            rc = 1
        if is_int_range(sPrefLen, 0, 128, 'Source Pref Len') == 0:
            rc = 1

    return (rc)


def add_tap_v4():

    if not check_config():
        return

    rc = 1
    while rc == 1:
        md_ip, md_port, md_source, md_dscp, md_timeout, cccid = insert_data_md()
        rc = verify_data_md(md_ip, md_port, md_source, md_dscp, md_timeout, cccid)

    rc = 1
    while rc == 1:
        t1_dPref, t1_dPrefLen, t1_sPref, t1_sPrefLen = insert_data_tap('1')
        rc = verify_data_tap(t1_dPref, t1_dPrefLen, t1_sPref, t1_sPrefLen, 'ipv4')

    rc = 1
    while rc == 1:
        t2_dPref, t2_dPrefLen, t2_sPref, t2_sPrefLen = insert_data_tap('2')
        rc = verify_data_tap(t2_dPref, t2_dPrefLen, t2_sPref, t2_sPrefLen, 'ipv4')

    create_md(
        md_ip, md_port, md_source, md_dscp, md_timeout, cccid
    )

    create_tap_v4(
        cccid, t1_dPref, t1_dPrefLen, t1_sPref, t1_sPrefLen, '1'
    )

    create_tap_v4(
        cccid, t2_dPref, t2_dPrefLen, t2_sPref, t2_sPrefLen, '2'
    )

    activate_tap(cccid, '1')
    activate_tap(cccid, '2')


def add_tap_v6():

    if not check_config():
        return

    rc = 1
    while rc == 1:
        md_ip, md_port, md_source, md_dscp, md_timeout, cccid = insert_data_md()
        rc = verify_data_md(md_ip, md_port, md_source, md_dscp, md_timeout, cccid)

    rc = 1
    while rc == 1:
        t1_dPref, t1_dPrefLen, t1_sPref, t1_sPrefLen = insert_data_tap('1')
        rc = verify_data_tap(t1_dPref, t1_dPrefLen, t1_sPref, t1_sPrefLen, 'ipv6')
        t1_dPref = ipaddress.IPv6Address(t1_dPref).exploded
        t1_sPref = ipaddress.IPv6Address(t1_sPref).exploded

    rc = 1
    while rc == 1:
        t2_dPref, t2_dPrefLen, t2_sPref, t2_sPrefLen = insert_data_tap('2')
        rc = verify_data_tap(t2_dPref, t2_dPrefLen, t2_sPref, t2_sPrefLen, 'ipv6')
        t2_dPref = ipaddress.IPv6Address(t2_dPref).exploded
        t2_sPref = ipaddress.IPv6Address(t2_sPref).exploded

    create_md(
        md_ip, md_port, md_source, md_dscp, md_timeout, cccid
    )

    create_tap_v6(
        cccid, t1_dPref, t1_dPrefLen, t1_sPref, t1_sPrefLen, '1'
    )

    create_tap_v6(
        cccid, t2_dPref, t2_dPrefLen, t2_sPref, t2_sPrefLen, '2'
    )

    activate_tap(cccid, '1')
    activate_tap(cccid, '2')


def show_cccid():
    global target
    cccids = []

    oids = '1.3.6.1.4.1.9.9.399.1.1.2.1.2'

    errorIndication, errorStatus, errorIndex, varBinds = cmdGen.nextCmd(
        security,
        cmdgen.UdpTransportTarget((target, 161)),
        oids
    )
    if errorIndication:
        print(errorIndication)
    else:
        if errorStatus:
            print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1] or '?'
            )
            )
        else:
            for elem in varBinds:
                for name, val in elem:
                    cccid = name.prettyPrint()
                    cccid = cccid.split('.')
                    cccids.append(cccid[14])

    if len(cccids) > 0:
        print('\nThe following CCCid\'s are set: ')
        for elem in cccids:
            print(elem)
    else:
        print('\nNo CCCids found.')


def show_intercept_counters():
    send_walk('1.3.6.1.4.1.9.9.399.1.2.1.1.4')


def set_snmp_security():
    global security

    selection = '1'

    while selection:
        print('\n####################################################')
        print('    1. AuthNoPriv: MD5')
        print('    2. AuthNoPriv: SHA')
        print('    3. AuthPriv  : MD5, DES')
        print('    4. AuthPriv  : MD5, 3DES')
        print('    5. AuthPriv  : MD5, AES')
        print('    6. AuthPriv  : SHA, DES')
        print('    7. AuthPriv  : SHA, 3DES')
        print('    8. AuthPriv  : SHA, AES')
        print('    0. Exit')

        selection = input('\nSelect option: ')

        if selection == '1':
            username = input('\nUsername  : ')
            authpass = input('MD5 Pass  : ')
            if is_str_length(username, 1, 'Username') and is_str_length(authpass, 8, 'AuthPass'):
                security = cmdgen.UsmUserData(username, authKey=authpass, authProtocol=cmdgen.usmHMACMD5AuthProtocol,
                                              privProtocol=cmdgen.usmNoPrivProtocol)
                return
        elif selection == '2':
            username = input('\nUsername  : ')
            authpass = input('SHA Pass  : ')
            if is_str_length(username, 1, 'Username') and is_str_length(authpass, 8, 'AuthPass'):
                security = cmdgen.UsmUserData(username, authKey=authpass, authProtocol=cmdgen.usmHMACSHAAuthProtocol,
                                              privProtocol=cmdgen.usmNoPrivProtocol)
                return
        elif selection == '3':
            username = input('\nUsername  : ')
            authpass = input('MD5 Pass  : ')
            privpass = input('DES Pass  : ')
            if is_str_length(username, 1, 'Username') and is_str_length(authpass, 8, 'AuthPass') and is_str_length(
                    privpass, 8, 'PrivPass'):
                security = cmdgen.UsmUserData(username, authKey=authpass, authProtocol=cmdgen.usmHMACMD5AuthProtocol,
                                              privKey=privpass, privProtocol=cmdgen.usmDESPrivProtocol)
                return
        elif selection == '4':
            username = input('\nUsername  : ')
            authpass = input('MD5 Pass  : ')
            privpass = input('3DES Pass : ')
            if is_str_length(username, 1, 'Username') and is_str_length(authpass, 8, 'AuthPass') and is_str_length(
                    privpass, 8, 'PrivPass'):
                security = cmdgen.UsmUserData(username, authKey=authpass, authProtocol=cmdgen.usmHMACMD5AuthProtocol,
                                              privKey=privpass, privProtocol=cmdgen.usm3DESEDEPrivProtocol)
                return
        elif selection == '5':
            username = input('\nUsername  : ')
            authpass = input('MD5 Pass  : ')
            privpass = input('AES Pass : ')
            if is_str_length(username, 1, 'Username') and is_str_length(authpass, 8, 'AuthPass') and is_str_length(
                    privpass, 8, 'PrivPass'):
                security = cmdgen.UsmUserData(username, authKey=authpass, authProtocol=cmdgen.usmHMACMD5AuthProtocol,
                                              privKey=privpass, privProtocol=cmdgen.usmAesCfb128Protocol)
                return
        elif selection == '6':
            username = input('\nUsername  : ')
            authpass = input('SHA Pass  : ')
            privpass = input('DES Pass  : ')
            if is_str_length(username, 1, 'Username') and is_str_length(authpass, 8, 'AuthPass') and is_str_length(
                    privpass, 8, 'PrivPass'):
                security = cmdgen.UsmUserData(username, authKey=authpass, authProtocol=cmdgen.usmHMACSHAAuthProtocol,
                                              privKey=privpass, privProtocol=cmdgen.usmDESPrivProtocol)
                return
        elif selection == '7':
            username = input('\nUsername  : ')
            authpass = input('SHA Pass  : ')
            privpass = input('3DES Pass : ')
            if is_str_length(username, 1, 'Username') and is_str_length(authpass, 8, 'AuthPass') and is_str_length(
                    privpass, 8, 'PrivPass'):
                security = cmdgen.UsmUserData(username, authKey=authpass, authProtocol=cmdgen.usmHMACSHAAuthProtocol,
                                              privKey=privpass, privProtocol=cmdgen.usm3DESEDEPrivProtocol)
                return
        elif selection == '8':
            username = input('\nUsername  : ')
            authpass = input('SHA Pass  : ')
            privpass = input('AES Pass : ')
            if is_str_length(username, 1, 'Username') and is_str_length(authpass, 8, 'AuthPass') and is_str_length(
                    privpass, 8, 'PrivPass'):
                security = cmdgen.UsmUserData(username, authKey=authpass, authProtocol=cmdgen.usmHMACSHAAuthProtocol,
                                              privKey=privpass, privProtocol=cmdgen.usmAesCfb128Protocol)
                return
        elif selection == '0':
            return
    return


def show_menu():
    selection = '1'

    while selection:
        print('\n####################################################')
        print('\nTarget router:', target)
        print('\nSelect operation:')
        print('    1. Set target router')
        print('    2. Set SNMP Security')
        print('    3. Walk LI MIBs')
        print('    4. Add new IPv4 LI TAP')
        print('    5. Add new IPv6 LI TAP')
        print('    6. Remove LI TAP')
        print('    7. Show CCCid\'s')
        print('    8. Show Intercept Counters')
        print('    0. Exit')

        selection = input('\nSelect option: ')

        if selection == '1':
            set_target()
        elif selection == '2':
            set_snmp_security()
        elif selection == '3':
            walk_mibs()
        elif selection == '4':
            add_tap_v4()
        elif selection == '5':
            add_tap_v6()
        elif selection == '6':
            remove_tap()
        elif selection == '7':
            show_cccid()
        elif selection == '8':
            show_intercept_counters()
        elif selection == '0':
            exit()

def check_config():
    if target == '0.0.0.0' or security == '':
        print('\nEither "target" or "SNMPv3 credentials not set. Returning to menu.')
        return 0

    return 1

def main():
    show_menu()


# This is the boilerplate that calls the main() function
if __name__ == '__main__':
    main()
