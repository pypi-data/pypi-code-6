import pickle, pprint, json

with open("BetlL3dic.pickle",'rb') as f : 
    L3dic = pickle.load(f)
    
with open("l3dic.json",'w') as f :
    f.write( "{\n" )
    
    l3l = []
    
    for k in sorted(L3dic.keys()) : 
    #for k , v in L3dic.items() : 
        v = L3dic[k]
        k = '"{}"'.format(k)
        l3l.append('{:>15}:{:>35}'.format( k, v ) )
    f.write( ",\n".join(l3l) )
    
    f.write( "}" )
    
    
