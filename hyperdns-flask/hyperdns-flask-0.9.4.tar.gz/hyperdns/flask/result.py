#
"""Utilities for returning flask.Response objects in various
semantically clear ways.
"""
import io
import json
import gzip
import datetime
import traceback
from flask import Response,make_response,request
from functools import wraps
import hyperdns.hal.render as HAL
from hyperdns.flask import hyperdns_context
import hyperdns.flask
from hyperdns.flask import ExceptionWithResponse,InputExpected
from hyperdns.hal.render import EnhancedJSONEncoder

def _json(data):
    """ internal convenience method to generate 'pretty print' JSON
    from an object.  Does not protect against any exceptions
    """
    return json.dumps(data,sort_keys=True,
        cls=EnhancedJSONEncoder,
         indent=4,separators=(',', ': '))
    

# function annotation - example: @compress, @returns_json, @returns_hal
def compress(f):
    """This will automatically compress the results if the request has
    provided gzip as an 'Accept-Encoding'
    
    Example::
        @web.result.compress
        def function(.....)
            .....
            return Response()
            
    """
    @wraps(f)
    def _compress(*args, **kwargs):
        response = f(*args, **kwargs)
        # pass through any responses that are already formed
        assert isinstance(response,Response)
        
        if len(response.data)>256:
            # check to see if we need to compress
            accept_encoding = request.headers.get('Accept-Encoding', '')
            
            if 'gzip' in accept_encoding.lower():
                response.direct_passthrough = False
                
                gzip_buffer = io.BytesIO()
                gzip_file = gzip.GzipFile(mode='wb',
                                          fileobj=gzip_buffer)
                gzip_file.write(response.data)
                gzip_file.close()
                
                response.data = gzip_buffer.getvalue()
                response.headers['Content-Encoding'] = 'gzip'
                response.headers['Vary'] = 'Accept-Encoding'
                response.headers['Content-Length'] = len(response.data)
            
        return response
    
    return _compress




        

class result(object):
    """
    HTTP status codes
    
    HTTP defines a bunch of meaningful status codes that can be returned from your API. These can be leveraged to help the API consumers route their responses accordingly. I've curated a short list of the ones that you definitely should be using:
    
    Response Code Reference::
        200 OK - Response to a successful GET, PUT, PATCH or DELETE. Can also be used for a POST that doesn't result in a creation.
        201 Created - Response to a POST that results in a creation. Should be combined with a Location header pointing to the location of the new resource
        204 No Content - Response to a successful request that won't be returning a body (like a DELETE request)
        304 Not Modified - Used when HTTP caching headers are in play
        400 Bad Request - The request is malformed, such as if the body does not parse
        401 Unauthorized - When no or invalid authentication details are provided. Also useful to trigger an auth popup if the API is used from a browser
        403 Forbidden - When authentication succeeded but authenticated user doesn't have access to the resource
        404 Not Found - When a non-existent resource is requested
        405 Method Not Allowed - When an HTTP method is being requested that isn't allowed for the authenticated user
        410 Gone - Indicates that the resource at this end point is no longer available. Useful as a blanket response for old API versions
        415 Unsupported Media Type - If incorrect content type was provided as part of the request
        422 Unprocessable Entity - Used for validation errors
        429 Too Many Requests - When a request is rejected due to rate limiting
    """
    
    @classmethod
    def catch_errors(cls,f):
        @wraps(f)
        def _catch_errors(*args,**kwargs):
            try:
                r = f(*args, **kwargs)
            except ExceptionWithResponse as E:
                r=E.resp
            except Exception as E:
                print("INTERNAL SERVER ERROR - LOGGING STACK TRACE for '%s'" % E)
                traceback.print_exc()
                r=cls.fail(E)
            return r
        return _catch_errors

    @classmethod
    def ok(cls,data=None):
        """
        Returns a 200 response with the message body::
            {
                'status':'ok'
            }
        unless a data parameter is provided, in which case the data is rendered as json
        using simple json encoding.  This is not intended for heavy returns, only simple
        acknowledgements of success.  Use the returns_json or returns_hal annotations
        for non-trivial JSON returns.  This response is not compressed.
        The content type is "application/json"
        """
        if data==None:
            body='{"status":"ok"}'
        else:
            body=_json(data)
        return Response(body,200,mimetype="application/json")
        
    @classmethod
    def fail(cls,e=''):
        """Returns a 500 response with the message body::
            {
                'status':'error',
                'message':''
            }
        """
        return Response('{"status":"error","message":"%s"}' % e,500,
                            mimetype="application/json")
        
    @classmethod
    @compress
    def plaintext(cls,txt):
        """Returns a 200 response, document with mimetype=text/plain,
        compressed if the client accepts gzip compression.
        """
        return Response(txt, mimetype='text/plain')
        
    @classmethod
    @compress
    def javascript(cls,txt):
        """Returns a 200 response, document with mimetype=application/javascript,
        compressed if the client accepts gzip compression.
        """
        return Response(txt, mimetype='application/javascript')
        
    @classmethod
    def json(cls,obj):
        """Return an object serialized as json
        """
        return Response(json.dumps(obj), mimetype='application/json')
        
    @classmethod
    def collection(cls,data,parent,c_name,c_index):
        """You know, I'd have to look this up - does some mild HAL encoding against
        a basic JSON structure
        """
        
        return HAL.hal_collection(
                           data=data,parent=parent,name=c_name,keyfield=c_index
                )
        
    @classmethod
    def created(cls,obj):
        """
        201 Created - Response to a POST that results in a creation. Should be combined with a Location header pointing to the location of the
        """
        return make_response('',201)
    
    @classmethod
    def noContent(cls):
        """ 
        204 No Content - Response to a successful request that won't be returning a body (like a DELETE request)
        """
        return make_response('',204)
    
    @classmethod
    def forbidden(cls,msg=None):
        """
        403 Forbidden - When authentication succeeded but authenticated user doesn't have access to the resource
        """
        if msg==None:
            body={}
        else:
            if isinstance(msg,str):
                body={'reason':msg}
            else:
                body=_json(data)
        
        return Response(json.dumps(body), 403,mimetype='application/json')
        
    @classmethod
    def unauthorized(cls,body=None):
        """
        401 Unauthorized - Authentication and authorization was not possible
        """
        if body==None:
            body=''
        else:
            body=_json(body)
        return Response(body,401,mimetype="application/json")
    
    @classmethod
    def bad_request(cls,msg="Bad Request"):
        return make_response('{"status":"error","message":"%s"}' % msg,400)
    
    @classmethod
    def validation_failed(cls,msg='Validation Failed'):
        return make_response('{"status":"error","message":"%s"}' % msg,422)
        
    @classmethod
    def input_expected(cls):
        return cls.validation_failed(msg="A request body was expected, but none was provided")
    
    @classmethod
    def not_found(cls):
        return make_response('',404)
    
    @classmethod
    def gone(cls,obj):
        """
        410 Gone - Indicates that the resource at this end point is no longer available. Useful as a blanket response for old API versions
        """
        return make_response('',410)
    
    @classmethod
    def unsupportedMediaType(cls):
        """
        415 Unsupported Media Type - If incorrect content type was provided as part of the request
        """
        return make_response('',415)
    
    @classmethod
    def tooManyRequests(cls,obj):
        """
        429 Too Many Requests - When a request is rejected due to rate limiting
        """
        return make_response('',429)

    @staticmethod
    def returns_json(f):
        """Indicates to flask that we're returning JSON.
        
        Design Decisions:
            Pretty Print By Default
                We choose to pretty print by default and apply compression to the response.
                We believe that this is an optimal balance between the ability for humans
                to rapidly and visually inspect response JSON against any increase in size
                or computing complexity.  Responses should be sent compressed via the
                standard accept-encoding mechanism.
        
            Compression
                We compress the resulting json if the client accepts gzip encoding.  The
                compression logic is only called when there is a data payload to return and
                when the data length is greater than 256 bytes.
            
                see: http://ramisayar.com/howto-automatically-enable-gzip-compression-on-aws-elastic-beanstalk/
    
        Example
        @web.returns_json
        def myMethod(...):
            return {}
        """
        @wraps(f)
        def _returns_json(*args, **kwargs):
            r = f(*args, **kwargs)
            # pass through any responses that are already formed
            if isinstance(r,Response):
                return r
            else:
                # pretty print the json and return a json object
                jsonResult=json.dumps(r,sort_keys=True, indent=4,
                    separators=(',', ': '))
                return Response(jsonResult, mimetype='application/json')
    
        return compress(_returns_json)

    
    @staticmethod
    def returns_hal(f):
        """Indicates to flask that we're returning HAL.
        
        We're using the HAL specification by Mike Kelley
            http://stateless.co/hal_specification.html
    
        Design Decisions:
            Pretty Print By Default
                We choose to pretty print by default and apply compression to the response.
                We believe that this is an optimal balance between the ability for humans
                to rapidly and visually inspect response JSON against any increase in size
                or computing complexity.  Responses should be sent compressed via the
                standard accept-encoding mechanism.
        
            Compression
                We compress the resulting json if the client accepts gzip encoding.  The
                compression logic is only called when there is a data payload to return and
                when the data length is greater than 256 bytes.
            
                see: http://ramisayar.com/howto-automatically-enable-gzip-compression-on-aws-elastic-beanstalk/
    
        Example
        @web.returns_json
        def myMethod(...):
            return {}
        """
        @wraps(f)
        def _returns_hal(*args, **kwargs):
            
            # invoke the function we wrap and collect the response, if that function
            # throws an exception it'll be propagated out to the outer catcher layers
            r = f(*args, **kwargs)
            
            # pass through any responses that are already formed
            if isinstance(r,Response):
                return r
            # now, if we have a list, return that as a special case - HAL is about
            # objects, so how do you return just a list that has no context?  that
            # has to be handled specially
            elif isinstance(r,list):
                r=HAL.hal_array(data=r,name="data")
                
            # now, if r is none, return an empty dict
            if r==None:
                jsonResult="{}"
            else:
                if not hasattr(r,'_hal'):
                    raise Exception("Attempt to return non _hal enabled object")
                else:
                    # now, determine if we include embedded objects, and if so, how many
                    # levels deep, ideally
                    hrc=HAL.hal_render_control(
                        # note, we are defaulting to True here to support staging,
                        # pending the changes that are being done in the develop
                        # branch at this moment - it's a race between what we need
                        # to put out, and the develop work.
                        embed=request.args.get('embed',True),
                        links=request.args.get('links',True),
                        depth=request.args.get('depth',0),
                        strict=request.args.get('strict',False)
                        )
                        
                    url=request.url
                    
                    # Reverse Proxy URL generation
                    if request.headers.get('X-Forwarded-For')!=None:
                      # Determine URL paths
                      path1 = '/'+request.script_root if request.script_root!=None and request.script_root!='' and request.script_root!='/' else ''
                      if path1[0:2]=='//':
                        path1 = path1[1:]
                      path2 = '/'+request.path if request.path!=None and request.path!='' and request.path!='/' else ''
                      if path2[0:2]=='//':
                        path2 = path2[1:]
                      
                      # Explicit base URL provided in X-Forwarded-Url header
                      fwd_url=request.headers.get('X-Forwarded-Url')
                      if fwd_url!=None:
                        # trim trailing forward slash
                        if fwd_url[-1]=='/':
                          fwd_url=fwd_url[0:-1]
                        url="%s%s%s" % (
                            fwd_url,
                            path1,
                            path2)
                      
                      # Otherwise - construct URL from Host, X-Forwarded-Proto 
                      # and X-Forwarded-Port request headers
                      else:
                        fwd_port=request.headers.get('X-Forwarded-Port')
                        # Default http/https ports
                        fwd_port=None if fwd_port=='80' or fwd_port=='443' else fwd_port
                        fwd_port=':'+fwd_port if fwd_port!=None else ''
                        fwd_host=request.headers.get('Host')
                        url="//%s%s%s%s" % (
                            fwd_host,
                            fwd_port, 
                            path1,
                            path2)
                      
                    jsonResult=r._hal(url,hrc,0)

            # now, build the response and return it
            return Response(jsonResult, mimetype='application/hal+json;version=0')
    
        # optionally compress any HAL document.
        return compress(_returns_hal)
        
        

