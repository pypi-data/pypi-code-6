import os,shutil,ast,json,subprocess
import click
import pkg_resources

def _filter_copy(src,dst,filtermap):
    try:
        with open(src, "r") as src_file:
            lines = src_file.readlines()
        with open(dst, "w") as dst_file:
            for line in lines:
                for match,replacement in filtermap.items():
                    line=line.replace(match, replacement)
                dst_file.write(line)
    except:
        return False
    return True
    
def _copy_seed_directory(source_dir,driver_repo_directory,filtermap):
    for name in os.listdir(source_dir):
        srcname = os.path.join(source_dir, name)
        dstname = os.path.join(driver_repo_directory, name)
        if os.path.isdir(srcname):
            os.mkdir(dstname)
            if not _copy_seed_directory(srcname, dstname, filtermap):
                return False
        else:
            _filter_copy(srcname, dstname,filtermap)
    return True
    
def _create_directory(path,force=False):
    print("PATH:",path)
    if os.path.exists(path):
        if not force:
            return False
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)
    os.mkdir(path)
    return True
    
@click.argument('vkey')
@click.argument('driver_repo_directory',type=click.Path(exists=False, file_okay=False,
                                        resolve_path=True))
@click.option('--force',is_flag=True,default=False,help="Force destruction of existing directory")
@click.pass_obj
def new_vendor(ctx,vkey,driver_repo_directory,force):
    """Initialize a project dir with the skeleton for a new driver.
    
    Implementation is as follows:
        - create the directory, make sure it is clear and writeable, if it
          already exists, bork the request - we want a fresh, clear directory
          for this.
    """
    try:
        source_dir=pkg_resources.resource_filename('hyperdns.vendor.cli','seed')
    except NotImplementedError as e:
        source_dir=os.path.join(os.path.dirname(__file__),'seed')
    
    # create the directory
    if not _create_directory(driver_repo_directory,force):
        click.echo("I am sorry, but I can not create '%s'" % driver_repo_directory)
        return
        
    # query the user for some additional input
    vname=click.prompt("What is the full name of '%s'" % vkey)
    vinfo=None
    click.echo("We need to know what properties your driver requires")
    click.echo("Please provide an array, like this ['one','two','three']")
    while vinfo==None:
        vin=click.prompt("What properties are required?")
        try:
            vinfo=ast.literal_eval(vin)
        except Exception as E:
            click.echo("I'm sorry, I could not parse that,",E)
    
    # copy the seed over, filtering against a dict
    filter_props={
        'VKEY':vkey,
        'VENDOR_NAME':vname,
        'VENDOR_SETTINGS':json.dumps(vinfo)
    }
    print(filter_props)
    if not _copy_seed_directory(source_dir,driver_repo_directory,filter_props):
        click.echo("I am sorry, but I was unable to copy everything into to seed directory.")
        return
        
    dbase=os.path.join(driver_repo_directory,'hyperdns/vendor/drivers')
    srcpath=os.path.join(dbase,'driver.py')
    pkgpath=os.path.join(dbase,vkey)
    filepath=os.path.join(pkgpath,'__init__.py')
    os.mkdir(pkgpath)
    os.rename(srcpath,filepath)
    
    # install it locally if desired
    if click.confirm("Would you like to install %s locally, for testing?" % vkey):
        subprocess.call(['pip','install','-e',driver_repo_directory])
    
