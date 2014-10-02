import os, enum, pkg_resources, json

#class Che(enum.Enum) : 
class Che(enum.IntEnum) : 
    핵체 = 0 
    정체 = 1 
    
class Lo(enum.IntEnum) :
    Non = 0 
    가로 = 1
    세로 = 2
    
# Dir.우 | Dir.하 
# class Dir(enum.Enum) : 
class Dir(enum.IntEnum) : 
    좌 = 1
    우 = 2
    상 = 4
    하 = 8

def binkeul_file( *fname ):
    return pkg_resources.resource_filename( 'binkeul', os.path.join( *fname ) )
    
    
def binkeul_load_json( json_file ):
    with open(binkeul_file('_static',json_file)) as f :
        jdata = json.load(f)
    return jdata
        
