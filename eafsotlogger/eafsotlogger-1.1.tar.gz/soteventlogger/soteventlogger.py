## Database schema ##
# Please change text to => blob
#CREATE KEYSPACE sot WITH replication = {'class':'SimpleStrategy', 'replication_factor':3};
#CREATE TABLE sot.events (id bigint, event_data text, component varchar, component_name varchar, log_level int, date_added timestamp, PRIMARY KEY (id, date_added));
#CREATE TABLE sot.eventlogs (event_id bigint, msg text, component varchar, component_name varchar, log_level int, date_added timestamp, PRIMARY KEY (event_id, date_added));

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

class EventLogger:
    con = None

    def __init__(self,nodes, username, password):
        auth_provider = PlainTextAuthProvider(username=username, password=password)
        cluster = Cluster(nodes, protocol_version=2, auth_provider=auth_provider)
        self.con = cluster.connect()
	
    def close(self):
        self.con.cluster.shutdown()
        self.con.shutdown()

    def eventlog(self, eid, event_data, component=None, component_name=None, log_level=None):
    	query1= "INSERT INTO sot.events (id, event_data, component, component_name, log_level, date_added) VALUES (%s, '%s', '%s', '%s', %s, dateof(now()))" %(eid, event_data, component, component_name, log_level) 
    	#print query1
        self.con.execute(query1)
    
    def log(self, event_id, msg, component=None, component_name=None, log_level=None):
    	query2= "INSERT INTO sot.eventlogs (event_id, msg, component, component_name, log_level, date_added) VALUES (%s, '%s', '%s', '%s', %s, dateof(now()))" %(event_id, msg, component, component_name, log_level) 
    	#print query2
        self.con.execute(query2)

def start ():
    print "module is running"

if __name__ == "__main__":
    print "Decide what to do"    