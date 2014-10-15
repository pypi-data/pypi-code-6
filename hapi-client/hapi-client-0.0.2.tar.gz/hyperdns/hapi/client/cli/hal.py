from hyperdns.hapi.client.cli import main
import json
import click

@main.command()
@click.argument('relativeuri',default="")
@click.option('--data',type=click.File('r'),default=None,help="File to post")
@click.option('--delete','do_delete',default=False,is_flag=True,help="Delete")
@click.option('--post','do_post',default=False,is_flag=True,help="Post")
@click.option('--props','props_only',default=False,is_flag=True,help="Properties only")
@click.option('--links','links_only',default=False,is_flag=True,help="Links only")
@click.option('--embed','embed_only',default=False,is_flag=True,help="Embed only")
@click.pass_obj
def hal(hapi,relativeuri,data,do_delete,do_post,props_only,links_only,embed_only):
    """Interact directly with the HAL server
    """
    try:
        body_data=None
        if data!=None:
            body_data=json.loads(data.read())
        
        if do_delete:
            result=hapi.delete(relativeuri)
        elif do_post:
            result=hapi.post(relativeuri,data=body_data)
        else:
            result=hapi.get(relativeuri,data=body_data)
                
        
        def get_hrefs(v):
            if isinstance(v,dict):
                return v.get('href')
            else:
                return [l.get('href') for l in v]
        if links_only:
            result={k:get_hrefs(v)
                 for k,v in result.get('_links',{}).items() 
                 if k not in ['curies']}
                 
        def get_embed(v):
            if v==None:
                return None
            else:
                return v.get('_class_name',"Collection")
        if embed_only:
            result={k:get_embed(v) for k,v in result.get('_embedded',{}).items() }
        if props_only:
            result={k:v for k,v in result.items() if k not in ['_embedded','_links']}

        print(json.dumps(result,sort_keys=True, indent=4, separators=(',', ': ')))
        
    except hapi.BadCall as E:
        print("%s : Received %s reading %s" % (E.response.reason,E.response.status_code,relativeuri))
    except FileNotFoundError:
        print("Failed to find '%s'" % (post_path))
    except ValueError as E:
        print("Failed to parse JSON in '%s'" % (post_path))
        print(E)