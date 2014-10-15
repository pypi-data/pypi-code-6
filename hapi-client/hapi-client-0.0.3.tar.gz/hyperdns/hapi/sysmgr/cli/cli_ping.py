from hyperdns.hapi.sysmgr.cli import SHAPICLI

#
@SHAPICLI.command('Check the server and see if the current configuration can log in')
def cmd_ping(arguments,hapi):
    """ping
    
    Check to see if the current credentials allow us to access the server.
    
    This will #print one of either:

    Example Invocations
        ping
            Check to see if we can connect to the server as configured.
            The output should be
                OK - "The server is alive and your credentials work"
                NOT - OK "Could not connect"
            
    """
    try:
        result=hapi.get('/auth/ping')
        if result.get('status')=='ok':
            print("The server is alive and your credentials work")
            return
        else:
            print("Received unexpected result:",result)
            return
    except Exception as E:
        print("Could not connect")
        raise
        #print "Error:",E

