import types
from pprint import pprint

class SSResultSet():
    def __init__(self, src, idxList ):
        self._res = idxList
        self._src = src
        self._idx = 0

    def __getitem__(self, idx):
        return self._src.row( self._res[idx] )

    def clear( self ):
        self._res = []

    def __iter__(self):        
        return SSResultSet._Iter(self)

    def __len__(self):
        return len(self._res)

    def getRowDict(self, irow ):
        if irow >= len( self._res ):
            return None
        return self._src.row_dict( self._res[ irow ] )

    def to_list( self ):
        rs = []
        for r in self:
            rs.append( tuple(r.values()) )

            #if type(r) == types.DictType:
            #    rs.append( tuple(r.values()) )
            #elif type(r) == types.ListType:
            #    rs.append( tuple( r ) )
        return rs        

    def filter( self, condition ):
        tempRs = []
        for irow in self._res:
            row = self._src.row( irow )
            if condition( row ):
                tempRs.append( irow )
        return SSResultSet( self._src, tempRs )

    def top( self, cnt ):
        newlist = self._res[0: cnt]
        return SSResultSet( self._src, newlist )

    def tail( self, cnt ):
        newlist = self._res[ len(self._res) -cnt : ]
        return SSResultSet( self._src, newlist )

    def any( self ):
        import random
        if len( self._res ) == 0:
            return SSResultSet( self._src, [] )
        return SSResultSet( self._src, [ random.choice( self._res) ] )

    def _append_row_index( self, idx ):
        self._res.append( idx )

    def group( self, group_columns = () ):
        group_rs = SSResultGroup( group_columns, self._src )
        for i in self._res:
            row = self._src.row(i)
            if type(group_columns) in ( types.ListType, types.TupleType):
                g_name = []
###TY LD
                for gcol in group_columns:
                    g_name.append( row[ gcol ] )
                t_gname = tuple( g_name )

                if not group_rs.get( t_gname ):
                    group_rs[ t_gname ] = SSResultSet( self._src, [] )
                group_rs[ t_gname ]._append_row_index( i ) 
            else:
                g_name = row.get( group_columns )
                if not group_rs.get( g_name ):
                    group_rs[ g_name ] = SSResultSet( self._src, [] )
                group_rs[ g_name ]._append_row_index( i )  # make copy
                

        return group_rs

    def sort( self, sortList, reverse = False ):      # sort
        class _sort():
            def __init__(self, src ):
                self._sortlist = sortList
                self._src = src
            def _make( self, lhs, rhs ):
                rowL = self._src._storage.get( lhs )
                rowR = self._src._storage.get( rhs )
                
                pairs = self._sortlist
                last = len(pairs)-1
                for i in xrange( len(pairs) ):
                    k, v = pairs[i]
                    col = k
                    colL = rowL[col]
                    colR = rowR[col]
                    if i == last:
                        return v( colL, colR )
                    if v( colL, colR ) < 0:
                        return -1;
                    return 1                        
                return -1

        newList = sorted( self._res, _sort( self._src )._make, reverse=reverse )
        return SSResultSet( self._src, newList )

    class _Iter():
        def __init__(self, rs ):
            self._rs = rs
            self._idx = 0
        def next( self ):
            if len(self._rs) <= self._idx:
                raise StopIteration
            self._idx +=1            
            return self._rs[ self._idx-1 ]


class SSResultGroup(dict):
    ''' { group_name: [ row,
                        row,...    ]
         }
    '''   
    def __init__(self, group, src ):
        self._group = group
        self._src = src
        super( SSResultGroup, self).__init__()

    @property
    def group_name(self):
        return self._group

    def head( self, icount ):
        ''' flat all items into a list
        '''
        if icount<=0:
            icount = None   # all 

        rs = SSResultSet( self._src, [] )
        for k, v in self.items():            
            rs._res.extend( v._res )
        return rs


