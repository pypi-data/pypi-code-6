'''
Created on May 7, 2014

@author: sshuster
'''
import sys
import ConfigParser
import os
import subprocess
from optparse import OptionParser

PATHS = "RemotePaths"

class TableFile(object):
    '''
    classdocs
    '''
    def __init__(self, file_path, table_prefix):
        '''
        Constructor
        '''
        self.table_prefix = table_prefix
        self.set_file_path(file_path)
        self.table_name = self.file_name_to_table_name(file_path)
        self.sql_name = "sql_"+self.table_name
        self.headers = None
        self.typelist = None
        self.sql_path = None
        
    def file_name_to_table_name(self, file_name):
        '''Returns the table name based off of a file name'''
        return self.table_prefix + os.path.basename(file_name).split('.')[0]
    
    def set_file_path(self, file_path):
        self.file_path = file_path
        self.file_name = os.path.basename(file_path)
    
    def add_headers(self, headers):
        self.headers = headers
        
    def add_typelist(self, typelist):
        self.typelist = typelist
    
    def set_sql_path(self, sql_path):
        self.sql_path = sql_path

class CygwinSSH(object):
    ssh_root = "ssh {0}@{1} "
    scp_root = "scp {0} {1}:{2}"
    mkdir_command = "mkdir {0}"
    
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.ssh_rootf = self.ssh_root.format(user,host)
    
    def make_ssh_command(self, command):
        return self.ssh_rootf + "'" + command + "'"
    
    def mkdir(self, dest_folder):
        os.system(self.make_ssh_command(self.mkdir_command.format(dest_folder)))
        
    def put(self, src, dest):
        os.system(self.scp_root.format(src,self.host,dest))
        
    def exec_command(self, command):
        out = ""
        try:
            out = subprocess.check_output(self.make_ssh_command(command), shell=True)
        except subprocess.CalledProcessError:
            pass
        return out

class FileLoaderException(Exception):
    pass

class FileLoader(object):
    
    def __init__(self, tablefile_list, ssh_client):
        self.src_tablefiles = tablefile_list
        self.ssh_client = ssh_client
    
    def load_config_and_run(self, config, config_destination_folder):
        config_file_location = create_unix_path(config_destination_folder,config.file_name)
        self.ssh_client.put(config.file_path, config_file_location)
        print "Running remote Hive Table Creation Script..."
        print self.ssh_client.exec_command("python /misc/sshuster/scripts/server_logic/create_hive_tables.py {0}".format(config_file_location))
        
    def load_files_to_cluster(self, destination_folder, processed_destination_folder, sql_destination_folder, config_destination_folder):
        self.reset_path(destination_folder)
        self.reset_path(sql_destination_folder)
        self.reset_path(processed_destination_folder)
        self.reset_path(config_destination_folder)
        for src_file in self.src_tablefiles:
            self.ssh_client.put(src_file.file_path, create_unix_path(destination_folder, src_file.file_name))
    
    def reset_path(self, path):
        print "Resetting Remote Path: {0}".format(path)
        try:
            self.ssh_client.mkdir(path)
        except Exception as e:
            print e
            pass
        print "tmp directory already exists... removing files"
        try:
            command = "rm {0}/*".format(path)
            self.ssh_client.exec_command(command)
        except Exception as e:
            print "error in cleaning out temporary directory. This is a hard error, program is exiting"
            print e
            raise FileLoaderException

def create_unix_path(first, second):
    first = first.rstrip('/')
    second = second.lstrip('/')
    return first + '/' + second            
    
def parse_config(config_file):
    config = ConfigParser.ConfigParser()
    config.readfp(open(config_file,'r'))
    return config

def create_tablefile_list(tables):
    ret = []
    for f in tables:
        ret.append(TableFile(f, ""))
    return ret

def parseCLI():
    usage = 'usage: python %prog [options] <path_to_config_file> path/to/table1.csv path/to/table2.csv ... path/to/tablen.csv'
    if len(sys.argv) <= 1:
        print usage
        exit(0)
    elif len(sys.argv) == 2:
        print 'No tables specified! Please specify at least one path to a table.csv'
        exit(0)
    parser = OptionParser(usage)
    (options, args) = parser.parse_args()
    return options, args

def main():
    options, args = parseCLI()
    config_file = args[0]
    config = parse_config(config_file)
    src_path = config.get(PATHS, "preprocessed_path")
    processed_path = config.get(PATHS, "processed_path")
    sql_path = config.get(PATHS, "sql_path")
    config_path = config.get(PATHS, "config_path")
    
    server = config.get(PATHS,"server")
    username = config.get(PATHS,"username")
    password = config.get(PATHS,"password")
    
    fl = FileLoader(create_tablefile_list(args[1:]), CygwinSSH(server,username,password))
    fl.load_files_to_cluster(src_path, processed_path, sql_path, config_path)
    fl.load_config_and_run(TableFile(config_file, ""), config_path)

if __name__ == '__main__':
    main()