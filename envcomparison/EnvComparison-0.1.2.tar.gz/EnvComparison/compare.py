#!/usr/bin/env python

from env import connection, ssh_hosts, server, differ
import sys
import tornado.httpserver
import tornado.ioloop
import tornado.web
import os

def compare_servers(opt_1, opt_2, host_list, ssh_config):

    connection_pool = [
        connection.Connection(ssh_config, host_list[int(opt_1)]),
        connection.Connection(ssh_config, host_list[int(opt_2)])
        ]


    for conn in connection_pool:
        conn.get_platform_details()
        conn.get_platform_family()
        conn.get_system_packages()
        conn.get_system_arch()
        conn.get_fqdn()
        conn.get_php_packages()
        conn.get_ruby_packages()
        conn.get_pip_packages()


    global server1_dict
    global server2_dict

    server1_dict, server2_dict = connection_pool[0].system, connection_pool[1].system


    global samekeysandvalues
    global samekeysdiffvalues
    global missingkeys
    global extrakeys

    samekeysandvalues, samekeysdiffvalues, missingkeys, extrakeys = differ.diffdict(connection_pool[0].system, connection_pool[1].system)




def main():

    if len(sys.argv) != 2:
        print "Please provide the location of your ssh config file"
        sys.exit()
    ssh_config = sys.argv[1]
    host_list = ssh_hosts.get_host_list(ssh_config)

    for key, value in host_list.items():
        print "[",key,"] ",value
    opt_1 = raw_input('Please select the first server:')
    opt_2 = raw_input('Please select the second server:')

    compare_servers(int(opt_1), int(opt_2), host_list, ssh_config)
    


class MainHandler(tornado.web.RequestHandler):

    def get(self):
        samekeysandvalues
        self.render("main.html", 
             server1_dict=server1_dict,
             server2_dict=server2_dict,
             samekeysandvalues=samekeysandvalues,
             samekeysdiffvalues=samekeysdiffvalues,
             missingkeys=missingkeys, 
             extrakeys=extrakeys,
             )



class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
           (r"/", MainHandler),
        ]
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
        )
        tornado.web.Application.__init__(self, handlers, **settings)


def server():
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(8888)
    print "Please browse to http://127.0.0.1:8888/"
    tornado.ioloop.IOLoop.instance().start()




if __name__ == "__main__":
    main()
    server()







