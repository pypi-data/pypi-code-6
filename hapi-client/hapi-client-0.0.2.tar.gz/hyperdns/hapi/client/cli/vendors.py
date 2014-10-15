from hyperdns.hapi.client.cli import (
    main,nonsense,
    require_zone,
    require_vendor
    )
import json,sys,click


def do_available(account):
    """List the available vendors
    """
    vendordefs=account.get('/vendors/available')
    vd={}
    for vendordef in vendordefs:
        vd[vendordef['vkey']]=vendordef
    
    click.echo("%-6s %-20s %s" % ('vkey','Vendor','Service'))
    click.echo("------ -------------------- --------------------")
    for vname in sorted(vd):
        vendordef=vd.get(vname)
        print("%(vkey)-6s %(vendor)-20s %(service)s" % vendordef)


def do_describe(account,vendor):
    """Display descriptive information about a vendor
    """
    if vendor==None:
        nonsense("I was asked to describe a vendor, but given no vendor")
    else:
        click.echo("Vendor: %s" % (vendor.title()))
        click.echo("  --Policy : %s" % vendor.policy)
        click.echo("  --Active : %s" % vendor.active)
        if vendor.active:
            click.echo("Settings")
            for key in sorted(vendor.settings.keys()):
                value=vendor.settings[key]
                click.echo("  %-20s:%s" % (key,value))
            if vendor.scan!=None:
                print("Scan: Running")
                print(" start time:",vendor.scan.start_time)
                print(" zone list:",vendor.scan.zonelist)
                print(" zone list time:",vendor.scan.zonelist_time)
                print(" status:",vendor.scan.status)
            else:
                click.echo("Scan: None")
        #print("History:",vendor.history)
        #print(json.dumps(vendor,sort_keys=True, indent=4, separators=(',', ': ')))



def do_setup(account,vkey,setup):
    """update or create or adjust the setup of the vendor.
    """
    if vkey==None:
        click.echo("Please specify a vendor when setting up a vendor")
        return None
    else:
        try:
            data=json.loads(setup.read())
        except Exception as e:
            click.echo('Problem parsing json file %s, message=%s' % (setup.name,e))
            return
    
        account.update_vendor(vkey,data)
        
        return account.vendors.get(vkey)
        
def do_list(account):
    """List the currently available vendors
    """
    if len(account.vendors)==0:
        click.echo("No vendors are configured")
        do_available(account)
    else:
        click.echo("The following vendors are configured")
        message="%-8s %-15s %-20s %s" % ("policy","vkey","Vendor","Service")
        click.echo(message)
        click.echo("-------- --------------- -------------------- ---------------------")
        for vkey in sorted(account.vendors.keys()):
            vendor=account.vendors.get(vkey)
            policy=vendor.policy
            vname=vendor.company_name()
            vserv=vendor.service_name()
            message="%-8s %-15s %-20s %s" % (policy,vkey,vname,vserv)
            click.echo(message)
            

#
@main.command()
@click.argument('vkey',default=None,required=False)
@click.option('--available','action',flag_value='available',help="List available")
@click.option('--deactivate','action',flag_value='deactivate',help="Deactivate this vendor")
@click.option('--scan','action',flag_value='scan',help="Scan this vendor")
@click.option('--reset','action',flag_value='reset',help="Reset the master record to this vendor")
@click.option('--adjust','action',flag_value='adjust',help='Update records on a single vendor')
@click.option('--push','action',flag_value='push',help='Push missing records on a single vendor')
@click.option('--pull','action',flag_value='pull',help='Pull overpresent on a single vendor')
@click.option('--setup',type=click.File('r'),default=None,help="Update vendor configuration from file")
@click.option('--policy',default=None,type=click.Choice(['master', 'peer', 'replica']),help='Update vendor policy')
@click.pass_obj
def vendors(account,vkey,action,setup,policy):
    """Activate, Deactivate, and Manage vendors
    """
    vendor=None
    if action=='available':
        if vkey!=None:
            click.echo("Sorry, i'm confused, try using --available alone without a vendor key")
        do_available(account)
    elif setup!=None:
        if policy!=None:
            click.echo("Please include the policy in the setup file, not on the command")
        vendor=do_setup(account,vkey,setup)
        if policy!=None:
            vendor.changePolicy(policy)
    elif vkey==None:
        if action!=None:
            click.echo("Please specify a vendor for %s" % action)
        else:
            do_list(account)
    else:
        vendor=require_vendor(account,vkey)
        title=vendor.title()
        if policy!=None:
            action='policy'
            
        if action=='deactivate':
            if vendor.active:
                vendor.deactivate()
        elif action=='adjust':
            vendor.adjust()
            click.echo("Vendor Adjustment Initiated for %s" % title)
        elif action=='scan':
            vendor.runScan()
            click.echo("Vendor Scan Initiated for %s" % title)
        elif action=='reset':
            vendor.resetMaster()
        elif action=='push':
            vendor.pushMissing()
        elif action=='pull':
            vendor.pullOverpresent()
        elif action=='policy':
            vendor.changePolicy(policy)
            click.echo("Vendor policy changed to %s" % policy)
    if vendor!=None:
        vendor._refresh_from_server()
        do_describe(account,vendor)




