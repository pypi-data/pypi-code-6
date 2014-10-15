import click,textwrap
import os,webbrowser,json,http.server,socketserver


def _driver_class(ctx):
    """Return the driver class for a given context.  The context will
    contain the name of the vendor to look up.
    
    :param click.Context ctx: this is the context object from click
    """
    try:
        vkey=ctx.parent.parent.invoked_subcommand
        return import_driver(vkey)
    except (DriverLoadFailureException) as E:
        click.echo(E)
        ctx.exit(-1)

class AngularCommands(click.MultiCommand):
    """click.Multicommand implementation for angular support
    
    angular dump
    
          <insert output of help here>
      
    angular test
    
          <insert output of help here>
      
    """
    def list_commands(self,ctx):
        return ['test','dump']
    def get_command(self,ctx,name):
        return getattr(self,name)


    @click.command()
    @click.option('--out',type=click.File('w'),default='-',help="file to save, or stdout")
    @click.pass_context
    def dump(ctx,out):
        """Dump the angular directive information to a file.
        """
        try:
            dclass=_driver_class(ctx.parent)
            out.write(dclass.returnAngularDirective())
        except Exception as E:
            click.echo("Angular Dump failed - unable to load driver")
            click.echo("Exception:%s" % E)
            return False

    @click.command()
    @click.option('--port',default=2112,help='port for run server')
    @click.pass_obj
    def test(ctx,port):
        """Test the driver-supplied angular directive for integration into web sites.
    
        This will open up a web browser to port localhost:2112 and provide a UI that
        allows you to test the UI configuration element of the browser, as well as
        provide simple zone scanning and management.
        """
        self=ctx['self']
        try:
            driver=self._driver(ctx)
        except Exception as E:
            click.echo("Angular Test failed - unable to configure driver")
            click.echo("Exception:%s" % E)
            return False
    
        class Handler(http.server.SimpleHTTPRequestHandler):
            def do_POST(self,*args,**kwargs):
                if self.path=='/testLogin':
                    length = int(self.headers['Content-Length'])
                    settings=json.loads(self.rfile.read(length).decode('utf-8'))
                    result=driver.checksettings(settings)
                    self.protocol_version='HTTP/1.1'
                    if result:
                        self.send_response(200, 'OK')
                    else:
                        self.send_response(401, '')
                    self.end_headers()
                elif self.path=='/scanZoneList':
                    length = int(self.headers['Content-Length'])
                    settings=json.loads(self.rfile.read(length).decode('utf-8'))
                    self.protocol_version='HTTP/1.1'
                    self.send_response(200, 'OK')
                    self.send_header('Content-type', 'application/javascript')
                    self.end_headers()
                    result=json.dumps(driver.scanZoneList())
                    self.wfile.write(bytes(result, 'UTF-8'))
                elif self.path=='/scanZone':
                    length = int(self.headers['Content-Length'])
                    data=json.loads(self.rfile.read(length).decode('utf-8'))
                    self.protocol_version='HTTP/1.1'
                    self.send_response(200, 'OK')
                    self.send_header('Content-type', 'application/javascript')
                    self.end_headers()
                    result=json.dumps(driver.scanZone(data['zonename']))
                    self.wfile.write(bytes(result, 'UTF-8'))
                else:
                    raise Exception('Unknown post')
            def do_GET(self,*args,**kwargs):
                # return the directives - this is the same process used by the
                # production application
                if self.path=='/directives':
                    self.protocol_version='HTTP/1.1'
                    self.send_response(200, 'OK')
                    self.send_header('Content-type', 'application/javascript')
                    self.end_headers()
                    self.wfile.write(bytes(driver.returnAngularDirective(), 'UTF-8'))
        
                # this returns a set of 
                elif self.path=='/info':
                    self.protocol_version='HTTP/1.1'
                    self.send_response(200, 'OK')
                    self.send_header('Content-type', 'application/javascript')
                    self.end_headers()                    
                    result="var vinfo=%s" % json.dumps({
                        'vkey':driver.vkey,
                        'name':driver.name,
                        'info':driver.info,
                        'settings':driver.settings
                        })
                    self.wfile.write(bytes(result, 'UTF-8'))
                else:
                    return super(Handler, self).do_GET(*args,**kwargs)
        httpd = socketserver.TCPServer(("", port), Handler)
        os.chdir(os.path.join(os.path.dirname(__file__), 'ui'))
        webbrowser.open('http://localhost:%d' % port)
        #print("Open a browser to http://localhost:2112")
        httpd.serve_forever()  
    
    def __init__(self,dclass):
        click.MultiCommand.__init__(self)
        self.dclass=dclass
        self.short_help="angular stuff for '%s'" % self.dclass.name
        self.help=textwrap.dedent('''
        angular stuff for %s
        ''' % self.dclass.name)
    
    
    