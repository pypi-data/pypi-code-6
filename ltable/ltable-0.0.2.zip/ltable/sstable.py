import ssindex as SIdx
from ssresult import SSResultSet

class SSTable():
    def __init__(self, columns = []):
        self._storage = {}  # data store here
        self._indexs = {}   # index by columns
        self._columns = []  # column name 
        self._col_index = {}    # if row is only list, map name to column index
        self._next_ID = 0

    def __len__(self):
        return len(self._storage)

    @property
    def columns( self ):
        return self._solumns
    
    def addIndex( self, idx_col, name = None ):
        ''' idx_col could be index of column or list index of column
        '''
        import types
        idx = None
        if type( idx_col ) in (types.ListType, types.TupleType):
            idx = SIdx.SSIndex( idx_col, self, 0 )
        else:
            idx = SIdx.SSIndexM1( [idx_col], self, 0 )
        if name:
            self._indexs[name] = idx
        else:
            if not self._indexs.get(''):
                self._indexs[''] = []
            self._indexs[''].append( idx )
        return idx

    def onLog( self, p1, p2, p3 ):
        pass    
    
    def addRowByDict( self, row ):
        asList = [ None for i in xrange( self._columns ) ]
        for k,v in row.items():
            col = self._col_name.get( k )
            asList[col] = v
        self.addRow( row )

    def addRow( self, row ):
        import types
        rowIdx = self._next_ID
        if type( row ) == types.DictType:
            self._storage[rowIdx] = dict(row) # copy
        elif type( row ) in ( types.ListType, types.TupleType):
            self._storage[rowIdx] = list(row) # copy
        else:
            self.onLog( "addRow", "Not Support", type(row) )
            
        self._next_ID += 1

        self.onLog( rowIdx, row, "insert" )
        for k,v in self._indexs.items():
            v.registerRow( rowIdx, row )

    def findRowOne( self, idxName, keyValue, condition=None, format='dict' ):
        inRs = []
        self._findRow( idxName, keyValue, inRs )
                
        rs = SSResultSet( self, inRs )
        if  condition != None:
            rs = rs.filter( condition )
        if len( rs ) == 0:
            return rs

        if format  == 'dict':
            return rs.getRowDict(0)
        return rs[0]

    def findRow( self, idxName, keyValue ):
        inRs = []
        self._findRow( idxName, keyValue, inRs )
         
        rs = SSResultSet( self, inRs )
        return rs

    def findInSet( self, idxName, keyValueList ):        
        keepOne = set()
        for ks in keyValueList:
            inRs = []
            self._findRow( idxName, keyValue, inRs )
            for i in inRs:
                keepOne.add(i)
         
        rs = SSResultSet( self, list[keepOne] )
        return rs

    def removeRow( self, idxName, keyValue, condition = None):
        inRs = []
        self._findRow( idxName, keyValue, inRs )
        for i in inRs:
            row = self._storage.get( i )
            if (condition!=None) and not( condition( row ) ):
                continue
            for k, v in self._indexs.items():
                v.unregisterRow(i, row )
            del self._storage[i]

    def _findRow( self, idxName, keyValue, rs ):
        import types
        idx = idxName
        if type(idx) == types.StringType:
            idx = self._indexs.get( idxName )
            if not idx :
                return None
        
        if type( keyValue ) not in (types.ListType, types.TupleType ):
            keyValue = [keyValue]
        idx.getIndexRef( keyValue, rs )


    def update( self, idxName, keyValue, newData, condition=None ):
        rs = []
        self._findRow( idxName, keyValue, rs )
        for idx in rs:
            row = self._storage.get( idx )
            if not condition or _IsMatch( condition ):
                self._update( idx, newData )

    def _update( self, irow, values ):                
        row = self._storage.get( irow )
        for k, v in values.items():
            ## TY LD
            #idxCol = self._col_name.get( k )
            row[k] = v
    
    def _rs_to_Result( self, rs ):
        import ssresult
        pkg = ssresult.SSResultSet( self, rs )    
        return pkg

    def row( self, idx ):
        return self._storage.get( idx )

    def row_dict( self, idx ):
        if len(self._columns) == 0:
            return self._storage.get(idx) 
        return dict( zip(self._columns, self._storage.get(idx) ) )

    def all( self ):
        return SSResultSet( self, self._storage.keys() )
                

    def _getAllIndex( self, idxList ):
        for k, v in self._storage.items():
            idxList.insert( k )
        
       
