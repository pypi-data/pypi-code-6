from hyperdns.hapi.sysmgr.cli import SHAPICLI
import json

#
@SHAPICLI.command('Dump raw HAL')
def cmd_hal(arguments,hapi):
    """hal    
    """
    try:
        p=arguments.get('<relativeuri>')
        if p==None:
            p=''
            
        post_path=arguments.get('--post',None)
        if post_path==None:
            # we're just reading
            result=hapi.get(p)
        
            props_only=arguments.get('--props',False)
            if props_only:
                result={k:v for k,v in result.items() if k not in ['_embedded','_links']}
                
            print(json.dumps(result,sort_keys=True, indent=4, separators=(',', ': ')))
            
        else:
            with open(post_path,'r') as post_file:
                post_data=json.loads(post_file.read())
                result=hapi.post(p,data=post_data)
                print(json.dumps(result,sort_keys=True, indent=4, separators=(',', ': ')))
    except hapi.BadCall as E:
        print("Received %s reading %s" % (E.response.status_code,p))
    except FileNotFoundError:
        print("Failed to find '%s'" % (post_path))
    except ValueError:
        print("Failed to parse JSON in '%s'" % (post_path))
        raise
