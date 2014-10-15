from hyperdns.hapi.client.cli import main
import click
from hyperdns.netdns import (
dotify
)

def print_zone(zone):
    r=list(zone.resources.keys())
    print(zone.fqdn,len(r),r)

def do_upload(hapi,upload,replace):
    try:
        #zone=hapi.processZoneFile(upload.read())
        zone=hapi.submitZoneFile(upload.read())
        click.echo("Zone uploaded")
    except hapi.BadCall as E:
        click.echo("Failed with code: %s" % (E.response.status_code))

def do_download(hapi,download):
    try:
        print(zone.downloadZonefile())
    except hapi.BadCall as E:
        print("Failed to download zone file, received HTTP status: %s" % E.response.status_code)
    
def do_list(hapi,fqdn):
    z=hapi.zones
    if len(z)==0:
        print("No zones in this account")
    else:
        if fqdn==None:
            count=0
            dcount=0
            for fqdn,zone in hapi.zones.items():
                if not zone.deleted:
                    print(fqdn,len(zone.resources))
                    count=count+1
                else:
                    dcount=dcount+1
            if dcount>0:
                click.echo("%d deleted zones" % dcount)
            return
        else:
            if not fqdn.endswith('.'):
                fqdn=fqdn+'.'
            zone=z.get(fqdn)
            if zone==None:
                if arguments['--create']:
                    zone=hapi.ensureZone(fqdn)
                else:
                    click.echo("No Such Zone:%s" % fqdn)
                    return
            print_zone(zone)
    
def do_delete(hapi,fqdn):
    """Delete a zone
    """
    zone=hapi.zones.get(dotify(fqdn))
    if zone==None:
        click.echo("Zone not found")
    else:
        zone.delete()
        click.echo("Zone deleted")
        
def do_scan(hapi,fqdn):
    pass
    
def do_create(hapi,fqdn):
    pass
    
@main.command()
@click.argument('fqdn',default=None,required=False)
@click.option('--delete','action',flag_value='delete',help="Delete this zone")
@click.option('--scan','action',flag_value='scan',help="Scan this zone on all vendors")
@click.option('--create','action',flag_value='create',help="Create an empty zone")
@click.option('--upload',type=click.File('r'),default=None,help="file to load")
@click.option('--download',type=click.File('r'),default=None,help="file to save")
@click.option('--replace',default=False,is_flag=True,help="delete an existing zone and replace it when uploading")
@click.pass_obj
def records(hapi,fqdn,action,upload,replace,download):
    """Upload, download, explore, and manage zones
    """
    
    if upload!=None and download!=None:
        click.echo("You can either upload or download, not both")
        return
    
    if (upload!=None or download!=None) and action!=None:
        click.echo("You can not delete, scan, or create while uploading or downloading")
        return
        
    if replace and download!=None:
        click.echo("Replace only makes sense with upload")
        return
        
    if (action!=None or download!=None) and fqdn==None:
        click.echo("Sorry, you must provide a zone FQDN")
        return
    
    if action==None:
        if upload!=None:
            do_upload(hapi,upload,replace)
        elif download!=None:
            do_download(hapi,download)
        else:
            do_list(hapi,fqdn)
    elif action=="delete":
        do_delete(hapi,fqdn)
    elif action=="scan":
        do_scan(hapi,fqdn)
    elif action=="create":
        do_create(hapi,fqdn)
    else:
        raise Exception("Invalid action - click should protect against this")
