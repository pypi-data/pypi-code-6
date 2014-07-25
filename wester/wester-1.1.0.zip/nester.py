#处理多层嵌套的列表
movies=['The Holy Grail',1975,'Terry Jone & Terry Gilliam',91,
          ['Graham Chapman',['Michael Palin','John Cleese',
               'Terry Gilliam','Eric Idle','Terry' ]]]
def print_lol(the_list,level):
    for etch_movies in the_list:
       if isinstance(etch_movies,list):
          print_lol(etch_movies,level+1)
       else:
           for tab_stop in range(level):
               print("\t",end='')
           print(etch_movies)
print_lol(movies,0)
