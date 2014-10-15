from hyperdns.hal.navigator import Navigator
from hyperdns.netdns import (
RecordSpec,RecordPool
)

@Navigator.attach_class()
class MasterResourceRecordPool(object):
    
    def records(mrrp):
        """Get records out of a master resource record pool
        """
        if 'null' not in mrrp.pool.keys():
            return None
        for rdtype,recs in mrrp.pool['null'].items():
            for r in recs['records']:
                yield RecordSpec(json=r)

    def present_record_count(mrrp):
        """Get records out of a master resource record pool
        """
        if 'null' not in mrrp.pool.keys():
            return 0
        count=0
        for rdtype,recs in mrrp.pool['null'].items():
            for r in recs['records']:
                rec=RecordSpec(json=r)
                if rec.presence=='present':
                    count=count+1
        return count

@Navigator.attach_class()
class VendorResourceRecordSet(object):
    
    def records(vrrp):
        """Get records out of a master resource record pool
        """
        for rdtype,recs in vrrp.pool[vrrp.vkey].items():
            for r in recs['records']:
                yield RecordSpec(json=r)

    def present_record_count(vrrp):
        """Get records out of a master resource record pool
        """
        if vrrp.vkey not in vrrp.pool.keys():
            print("OUT",vrrp.vkey,vrrp.pool)
            return 0
        count=0
        for rdtype,recs in vrrp.pool[vrrp.vkey].items():
            for r in recs['records']:
                rec=RecordSpec(json=r)
                if rec.presence=='present':
                    count=count+1
        return count

@Navigator.attach_class()
class ChangeSet(object):            
    def delete_pool(cs):
        """Get records out of a master resource record pool
        """
        return RecordPool.from_dict(cs.to_delete)
    
    def create_pool(cs):
        """Get records out of a master resource record pool
        """
        return RecordPool.from_dict(cs.to_create)
    
