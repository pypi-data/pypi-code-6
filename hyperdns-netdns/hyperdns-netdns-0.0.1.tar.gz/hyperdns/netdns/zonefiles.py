import io
import dns.zone
import hyperdns.netdns
from hyperdns.netdns import rd_type_as_int,dotify

#
def translate_zonefiletext_to_json(zone_text):
    """Convert a zonefile into a json representation of the zone data.  The
    data has the form:
    
    {
        'fqdn':'example.com.',
        'resources':{
            'resource1':[....],
            'resource2':[....]
        }
    }
    
    where
    
    @param zone_text: zone file as string
    @return: zone data as JSON
    """
    pyzone = dns.zone.from_text(zone_text);
    zonename=dotify(pyzone.origin.to_text()).lower()
    resources={}
    for key, r in pyzone.items():
        resourcename=key.to_text().lower()
        if resourcename not in resources.keys():
            resources[resourcename]=[]
        recs=resources[resourcename]
        for rdataset in r:
            rdtype = rdataset.rdtype
            rdclass = rdataset.rdclass
            ttl = rdataset.ttl
            if rdtype in [hyperdns.netdns.A, hyperdns.netdns.CNAME, hyperdns.netdns.NS]:
                for record in rdataset:
                    if rdtype == hyperdns.netdns.A:
                        value = record.address
                    elif rdtype == hyperdns.netdns.CNAME:
                        value = record.target.to_text()
                    elif rdtype == hyperdns.netdns.NS:
                        value = str(record) #dotify("%s.%s" % (record,pyzone.origin))
                    else:
                        value = record.target.to_text()
                    
                    recs.append({
                            "type": rdtype,
                            "class": rdclass,
                            "ttl": ttl,
                            "rdata": value
                        })
    return {
        "fqdn":zonename,
        "resources":resources
    }

#
def translate_json_to_zonefiletext(zonedata):
    """Generate a zonefile from a JSON representation
    """
    assert zonedata.get('fqdn')!=None
    origin=dns.name.Name(zonedata['fqdn'].split('.')[:-1])
    pyzone = dns.zone.Zone(origin)
    
    for name,records in zonedata.get('resources',{}).items():
        for r in records:
            #rdtype = dns.rdatatype.from_text(r['type'])
            rdtype = r['type'] #rd_type_as_int(r['type'])
            #stuff = ' '.join([str(x) for x in r[]])
            rdata = dns.rdata.from_text(dns.rdataclass.IN, rdtype, r['rdata'])
            n = pyzone.get_rdataset(name, rdtype, create=True)
            n.ttl=r['ttl']
            n.add(rdata)
    
    output=io.StringIO()
    pyzone.to_file(output)
    return output.getvalue()



