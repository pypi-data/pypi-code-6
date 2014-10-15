from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider

class EventLogger:
    level_critical = 5
    level_error = 4
    level_warning = 3
    level_info = 2
    level_debug = 1

    def __init__(self, nodes, username, password, component, component_name):
        self.component = component
        self.component_name = component_name
        auth_provider = PlainTextAuthProvider(username=username, password=password)
        cluster = Cluster(nodes, protocol_version=2, auth_provider=auth_provider)
        self.con = cluster.connect()
    
    def __del__(self):
        self.con.cluster.shutdown()
        self.con.shutdown()

    def log_event(self, eid, event_data):        
        query = "INSERT INTO sot.events(id, event_data, component, component_name, created_date) VALUES (%s, %s, '%s', '%s', dateof(now()))" %(eid, event_data, self.component, self.component_name)
        self.con.execute(query)
    
    def critical(self, event_id, message):
        query = "INSERT INTO sot.eventlogs (event_id, message, component, component_name, log_level, created_date) VALUES (%s, %s, '%s', '%s', %s, dateof(now()))" %(event_id, message, self.component, self.component_name, self.level_critical)
        self.con.execute(query)

    def error(self, event_id, message):
        query = "INSERT INTO sot.eventlogs (event_id, message, component, component_name, log_level, created_date) VALUES (%s, %s, '%s', '%s', %s, dateof(now()))" %(event_id, message, self.component, self.component_name, self.level_error)
        self.con.execute(query)

    def warning(self, event_id, message):
        query = "INSERT INTO sot.eventlogs (event_id, message, component, component_name, log_level, created_date) VALUES (%s, %s, '%s', '%s', %s, dateof(now()))" %(event_id, message, self.component, self.component_name, self.level_warning)
        self.con.execute(query)

    def info(self, event_id, message):
        query = "INSERT INTO sot.eventlogs (event_id, message, component, component_name, log_level, created_date) VALUES (%s, %s, '%s', '%s', %s, dateof(now()))" %(event_id, message, self.component, self.component_name, self.level_info)
        self.con.execute(query)

    def debug(self, event_id, message):
        query = "INSERT INTO sot.eventlogs (event_id, message, component, component_name, log_level, created_date) VALUES (%s, %s, '%s', '%s', %s, dateof(now()))" %(event_id, message, self.component, self.component_name, self.level_debug)
        self.con.execute(query)

def start():
    pass