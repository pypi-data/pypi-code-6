from hyperdns.hapi.sysmgr.cli import SHAPICLI

#
@SHAPICLI.command('Login Again')
def cmd_login(arguments,hapi):
    if not hapi.relogin():
        print("Login failed")

