from hyperdns.hapi.client.cli import main
import click,json,time
from hyperdns.netdns import (
dotify,RecordSpec
)

def do_report(resource,report):
    """Upload a vendor observation file
    """
    data=json.loads(report.read())
    for vkey,info in data.items():
        resource.reportVendorObservations(vkey,info)

def do_scan(hapi,resource):
    """
    """
    #for vendors in hapi.vendors.values():
    #    vendor.
    resource.scan()
        
def do_delete(resource):
    """Delete a resource
    """
    resource.delete()
    click.echo("Resource deleted")
    
def do_describe(resource):
    click.echo("Resource Status:%s" % resource.status)
    if resource.master==None:
        click.echo("No master records")
    else:
        click.echo("Master Records")
        for rec in resource.master.records():
            click.echo("  %s %s %s" % (rec.rdtype.name,rec.rdata,rec.ttl))

    if len(resource.vendor_targets.keys())==0:
        click.echo("No vendor targets")
    else:
        click.echo("Vendor Target Records")
        for vkey,vset in resource.vendor_targets.items():
            print("  %s" % vkey)
            for rec in vset.records():
                click.echo("    %s: %s %s %s" % (rec.presence,rec.rdtype.name,rec.rdata,rec.ttl))
    
    click.echo("Assessment")
    click.echo("  Stable: %s" % resource.stable)
    click.echo("  Last Assessment:%s" % resource.last_assessment)
    click.echo("  Overpresent")
    for vkey,recs in resource.delta['overpresent'].items():
        click.echo("  %s" % vkey)
        for op in recs:
            op=RecordSpec(json=op)
            click.echo("    (%s %s %s)" % (op.rdtype.name,op.rdata,op.ttl))
    click.echo("  Missing")
    for vkey,recs in resource.delta['missing'].items():
        click.echo("  %s" % vkey)
        for op in recs:
            op=RecordSpec(json=op)
            click.echo("    (%s %s %s)" % (op.rdtype.name,op.rdata,op.ttl))
            
    # display the 'Changes' section
    click.echo("Changes")
    count=0
    pool=resource.changes.delete_pool()
    for vkey,rmap in pool.sourcemap.items():
        for rdtype,rset in rmap.items():
            for rec in rset:
                click.echo("  DELETE from %s, %s=%s, %s" % (vkey,rec.rdtype.name,rec.rdata,rec.ttl))
                count=count+1
    pool=resource.changes.create_pool()
    for vkey,rmap in pool.sourcemap.items():
        for rdtype,rset in rmap.items():
            for rec in rset:
                click.echo("  CREATE on %s, %s=%s, %s" % (vkey,rec.rdtype.name,rec.rdata,rec.ttl))
                count=count+1
    if count==0:
        click.echo("  No Changes")

def do_adjust(resource):
    resource.adjust()
    click.echo("Resource adjustment kicked off")

def do_push(resource,vendor):
    resource.pushMissing(vendor)
    click.echo("Resource adjustment kicked off")
    
def do_pull(resource,vendor):
    resource.pushMissing(vendor)
    click.echo("Resource adjustment kicked off")


@main.command()
@click.argument('fqdn')
@click.option('--adjust','action',flag_value='adjust',help="Update this resource")
@click.option('--delete','action',flag_value='delete',help="Delete this resource")
@click.option('--scan','action',flag_value='scan',help="Scan this zone on all vendors")
@click.option('--report',type=click.File('r'),default=None,help="file to upload")
@click.option('--push',default=None,help="Push missing records to a vendor")
@click.option('--pull',default=None,help="Pull overpresent records from a vendor")
@click.pass_obj
def resources(hapi,fqdn,action,report,push,pull):
    """Manage a resource
    """
    fqdn=dotify(fqdn)

    if push!=None:
        action="push"
        vendor=hapi.vendors.get(push)
        if vendor==None:
            click.echo("Sorry, I can not find vendor %s" % push)
            return
    if pull!=None:
        action="pull"
        vendor=hapi.vendors.get(pull)
        if vendor==None:
            click.echo("Sorry, I can not find vendor %s" % pull)
            return
    
    if report!=None and action!=None:
        click.echo("You can not delete, or scan while report")
        return
    
    zone=None
    for zname,_zone in hapi.zones.items():
        if fqdn.endswith(zname):
            zone=_zone
    
    if zone==None:
        click.echo("No zone found")
        return
        
    rname=fqdn[:-(len(zone.fqdn)+1)]
            
    resource=zone.resources.get(rname)
    if resource==None:
        click.echo("Resource %s not found" % fqdn)
        return
    
    if report!=None:
        do_report(resource,report)
        resource._refresh_from_server()
        do_describe(resource)
    elif action=='push':
        do_push(resource,vendor)
    elif action=='pull':
        do_pull(resource,vendor)
    elif action=='adjust':
        do_adjust(resource)
    elif action=='delete':
        do_delete(resource)
    elif action=='scan':
        do_scan(hapi,resource)
        click.echo("Sleeping 5 seconds")
        time.sleep(5)
        resource._refresh_from_server()
        do_describe(resource)
    else:
        do_describe(resource)