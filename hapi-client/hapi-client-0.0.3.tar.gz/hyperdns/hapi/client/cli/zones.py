from hyperdns.hapi.client.cli import main
import click
from hyperdns.netdns import (
dotify,
ZoneData,RecordPool
)

def do_describe(account,zone):    
    all_r=list(r.name for r in zone.resources.values() )
    living_r=list(r.name for r in zone.resources.values() if r.status!='dead')
    print("Zone %s" % zone.fqdn)
    print("  Deleted :%s" % zone.deleted)
    print("  Ignored :%s" % zone.ignored)
    print("  Discovery:%s" % zone.discovery)
    print("  Scans: %s" % zone.lastScans)
    print("  Resources: (%d/%d)" % (len(all_r),len(living_r)))
    for rname in sorted(zone.resources.keys()):
        resource=zone.resources[rname]
        hasmaster=(resource.master!=None)
        vrecs=sorted(resource.vendor_targets.keys())
        status=resource.status
        print("    %12s: %4s master=%5s vrecs on %s" % (rname,status,hasmaster,vrecs))
        

def do_upload(account,fqdn,upload):
    try:
        zone=account.zones.get(fqdn)
        if zone==None:
            click.echo("Can not find zone %s" % fqdn)
            return
        #zone=account.processZoneFile(upload.read())
        zone=account.submitZoneFile(upload.read())
        click.echo("Zone uploaded")
    except account.BadCall as E:
        click.echo("Failed with code: %s" % (E.response.status_code))

def do_download(account,fqdn,output,output_style):
    """Download a zone zone file or output as json
    """
    try:
        zone=account.zones.get(fqdn)
        if zone==None:
            click.echo("Zone not found")
        else:
            info={
                'fqdn':fqdn,
                'resources':[]
            }
            for r in zone.resources.values():
                resource={
                    'name':r.name,
                    'records':[]
                }
                info['resources'].append(resource)
                pool=RecordPool.from_dict(r.master.pool)
                for rec in pool.records:
                    resource['records'].append(rec)
                    
            zonedata=ZoneData.fromDict(info)
            click.echo("Copy zone data into ZoneData structure")
            if output_style!='json':
                output.write(zonedata.zonefile)
            else:
                output.write(zonedata._as_json())
    except account.BadCall as E:
        click.echo("Failed to download zone file, received HTTP status: %s" % E.response.status_code)
    
def do_list(account):
    """Describe all of the zones in this account
    """
    z=account.zones
    if len(z)==0:
        print("No zones in this account")
    else:
        click.echo("%25s %3s: %7s %s" % (
            'Zone','R#','M s/c','vendors res/rec miss/over'))
        
        count=0
        dcount=0
        for fqdn in sorted(account.zones.keys()):
            zone=account.zones.get(fqdn)
            vcount={}
            for vendor in account.active_vendors:
                vcount[vendor.vkey]=(0,0,0,0)
            mcount_res=0
            mcount_rec=0
            for r in zone.resources.values():
                if r.master!=None:
                    mcount_rec=mcount_rec+r.master.present_record_count()
                    mcount_res=mcount_res+1
                for vendor in account.active_vendors:
                    vkey=vendor.vkey
                    t=vcount[vkey]
                    vrrp=r.vendor_targets.get(vkey)
                    if vrrp!=None:
                        vcount[vkey]=(t[0]+1,t[1]+vrrp.present_record_count(),t[2],t[3])
                    miss=len(list(r.missing_for_vendor(vendor)))
                    over=len(list(r.overpresent_for_vendor(vendor)))
                    vcount[vkey]=(t[0],t[1],t[2]+miss,t[3]+over)
                        
            vcount_msg=""
            zone_has_trouble=False
            for vkey in sorted(account.vendors.keys()):
                vendor=account.vendors.get(vkey)
                if vendor.active:
                    t=vcount[vkey]
                    miss_msg="%3d" % t[2]
                    if t[2]>0:
                        miss_msg=click.style(miss_msg, fg='red')
                        zone_has_trouble=True
                    over_msg="%3d" % t[3]
                    if t[3]>0:
                        over_msg=click.style(over_msg, fg='blue')
                        zone_has_trouble=True
                    vcount_msg="%s%6s:%3d/%3d:%s/%s" % (vcount_msg,vkey,t[0],t[1],miss_msg,over_msg)
            if not zone.deleted:
                zone_title='%25s' % fqdn
                if zone_has_trouble:
                    zone_title=click.style(zone_title, fg='red')
                else:
                    zone_title=click.style(zone_title, fg='green')
                click.echo("%s %3d: %3d/%3d %s" % (
                    zone_title,len(zone.resources),mcount_res,mcount_rec,vcount_msg))
                count=count+1
            else:
                dcount=dcount+1
        if dcount>0:
            click.echo("%d deleted zones" % dcount)
        else:
            click.echo("And no deleted zones")

def do_summarize_changes(account):
    """Summarize all the changes on this account
    """
    z=account.zones
    if len(z)==0:
        print("No zones in this account")
    else:
        click.echo("%25s %3s: %7s %s" % (
            'Zone','R#','M s/c','vendors overpresent/missng'))
        
        count=0
        dcount=0
        for fqdn in sorted(account.zones.keys()):
            zone=account.zones.get(fqdn)
            vcount={}
            for vkey in account.vendors.keys():
                vcount[vkey]=(0,0)
            mcount_res=0
            mcount_rec=0
            for r in zone.resources.values():
                if r.master!=None:
                    mcount_rec=mcount_rec+r.master.present_record_count()
                    mcount_res=mcount_res+1
                for vendor in account.vendors.values():
                    t=vcount[vendor.vkey]
                    vcount[vendor.vkey]=(
                        t[0]+len(list(r.overpresent_for_vendor(vendor))),
                        t[1]+len(list(r.missing_for_vendor(vendor)))
                    )
                        
            vcount_msg=""
            for vkey in sorted(account.vendors.keys()):
                t=vcount[vkey]
                vcount_msg="%s%6s:%3d/%3d " % (vcount_msg,vkey,t[0],t[1])
            if not zone.deleted:
                click.echo("%25s %3d: %3d/%3d %s" % (
                    fqdn,len(zone.resources),mcount_res,mcount_rec,vcount_msg))
                count=count+1
            else:
                dcount=dcount+1
        if dcount>0:
            click.echo("%d deleted zones" % dcount)
        else:
            click.echo("And no deleted zones")
  
def do_report_changes(account,zone):
    """Report changes on a single zone
    """  
    # display the 'Changes' section
    click.echo("Changes")
    count=0
    
    for changes in zone.changes.values():
        rname=changes.rname
        pool=changes.delete_pool()
        for vkey,rmap in pool.sourcemap.items():
            for rdtype,rset in rmap.items():
                for rec in rset:
                    click.echo("  %10s DELETE from %s, %s=%s, %s" %
                            (rname,vkey,rec.rdtype.name,rec.rdata,rec.ttl))
                    count=count+1
        pool=changes.create_pool()
        for vkey,rmap in pool.sourcemap.items():
            for rdtype,rset in rmap.items():
                for rec in rset:
                    click.echo("  %10s CREATE on %s, %s=%s, %s" %
                             (rname,vkey,rec.rdtype.name,rec.rdata,rec.ttl))
                    count=count+1
    if count==0:
        click.echo("  No Changes")
  
        

        

    
def do_push(account,zone,vkey):
    if vkey==None:
        for vendor in account.active_vendors:
            zone.pushMissing(vendor.vkey)
            click.echo("Vendor push kicked off against %s for zone %s" % (vendor.title(),zone.fqdn))
    else:
        vendor=account.require_vendor(vkey)
        zone.pushMissing(vendor.vkey)
        click.echo("Vendor push kicked off against %s for zone %s" % (vendor.title(),zone.fqdn))

def do_pull(account,zone,vkey):
    zone.pullOverpresent(vkey)
    click.echo("Vendor pull kicked off")

def do_create(account,fqdn):
    """Create a zone
    """
    account.ensureZone(fqdn)
    click.echo("Created %s" % fqdn)
    
def do_reset(account,zone,vkey):
    """Reset a zone to a master from a vendor
    """
    vendor=account.vendors.get(vkey)
    if vendor==None:
        click.echo("Vendor not found")
    else:
        if not vendor.active:
            click.echo("Vendor is not active")
        else:
            zone.resetMasterFromVendor(vkey)
    
@main.command()
@click.argument('fqdn',default=None,required=False)
@click.option('--unignore','action',flag_value='unignore',help="Un-ignore this zone")
@click.option('--undelete','action',flag_value='undelete',help="Un-delete this zone")
@click.option('--ignore','action',flag_value='ignore',help="Ignore this zone")
@click.option('--delete','action',flag_value='delete',help="Delete this zone")
@click.option('--scan','action',flag_value='scan',help="Scan this zone")
@click.option('--changes','action',flag_value='changes',help="Display the changes")
@click.option('--adjust','action',flag_value='adjust',help="Update this zone")
@click.option('--create','action',flag_value='create',help="Create an empty zone")
@click.option('--push','action',flag_value='push',help="Push missing records")
@click.option('--pull','action',flag_value='pull',help="Pull overpresent records")
@click.option('--reset','action',flag_value='reset',help="Reset master from a specific vendor")
@click.option('--upload',type=click.File('r'),default=None,help="file to load")
@click.option('--download',type=click.File('w'),default=None,help="file to save")
@click.option('--format','output_style',default='json',type=click.Choice(['json', 'bind']),help='For download, what format should we return')
@click.option('--vendor','vkey',default=None,help="Restrict action to a specific vendor")
@click.pass_obj
def zones(account,fqdn,action,upload,download,output_style,vkey):
    """Manage zones.
    
    Notes:
      - without a fqdn and no actions, we list information about all zones
      - Downloading takes the --format option
      - you can restrict many options with --vendor <vkey>
    
    Examples::
      hapi zones <fqdn> --<action>
      
     
      
    """
    zone=None
    if fqdn!=None:
        fqdn=dotify(fqdn)
        if action!='create':
            zone=account.zones.get(fqdn)
            if zone==None:
                click.echo("Zone not found")
                return
                
    if zone==None:
        zones=account.active_zones
    else:
        zones=[zone]
    
    vendor=None
    if vkey!=None:
        if action in ['unignore','undelete','ignore','delete','upload','download']:
            click.echi("--vendor does not make sense in this contact")
            return
        vendor=account.require_vendor(vkey)
          
    if upload!=None and download!=None:
        click.echo("You can either upload or download, not both")
        return
    
    if (upload!=None or download!=None) and action!=None:
        click.echo("You can not delete, scan, or create while uploading or downloading")
        return
    
    if download!=None and fqdn==None:
        click.echo("Sorry, you must provide a zone FQDN")
        return
    
    if action==None:
        if upload!=None:
            do_upload(account,fqdn,upload)
        elif download!=None:
            do_download(account,fqdn,download,output_style)
        else:
            if fqdn==None:
                do_list(account)
            else:
                do_describe(account,zone)
    elif action=="push":
        for z in zones:
            do_push(account,z,vkey)
    elif action=="pull":
        do_pull(account,zone,vkey)
    elif action=="undelete":
        zone.undelete()
    elif action=="unignore":
        zone.unignore()
    elif action=="ignore":
        zone.ignore()
    elif action=="delete":
        zone.delete()
    elif action=="scan":
        zone.scan()
    elif action=="adjust":
        zone.adjust()
    elif action=="reset":
        do_reset(account,zone,reset)
    elif action=="create":
        do_create(account,fqdn)
    elif action=="changes":
        if zone==None:
            do_summarize_changes(account)
        else:
            do_report_changes(account,zone)
        return
    else:
        raise Exception("Invalid action - click should protect against this")
        
    if zone!=None:
        zone._refresh_from_server()
        do_describe(account,zone)
