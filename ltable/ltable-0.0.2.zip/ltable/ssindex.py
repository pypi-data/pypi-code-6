

class SSIndexBase( object ):
    def __init__(self, col, source):
        self._col = col
        self._src = source

    def getIndexRef( self, key, outRslt, index_level = 0):
        pass

class SSIndexM1( SSIndexBase ):
    def __init__(self, col, source, useIdx ):
        super(SSIndexM1, self).__init__( col[useIdx], source)
        self._keyMap = {}

    def registerRow( self, idxRow, row ):
        row_value = row[self._col]
        v = self._keyMap.get( row_value )
        if not v:
            self._keyMap[ row_value ] = set()
            v = self._keyMap[ row_value ]
        v.add( idxRow )
        
    def getIndexRef( self, keys, outRslt, index_level = 0):
        if index_level >= len(keys):
            self.getAllItem( outRslt )
            return

        #row_value = set()
        row_value = self._keyMap.get( keys[ index_level ] )
        if not row_value:
            return

        for v in row_value:
            outRslt.append( v )
        
    def unregisterRow( self, rowIdx, row ):
        v = row[self._col]
        
        try:
            self._keyMap[v].remove( rowIdx )
        except KeyError as e:
            return True
        
        if len( self._keyMap[v] ) == 0:
            del self._keyMap[v] 
            return True
        return False
        
    def getAllItem( self, outRslt ):
        for k, v in self._keyMap.items():
            for y in v:
                outRslt.append( y )

    def getColumnIndex( self, vIndex ):
        super( SSIndexM1, self).getColumnIndex( vIndex )


class SSIndex( SSIndexBase ):
    def __init__(self, cols, source, iUseIdx=0):
        super(SSIndex, self).__init__(  cols[iUseIdx], source )
        self._colIndex = cols
        self._ref_Value = {}
        self._next_index = iUseIdx +1

    def _clearIndex( self ):
        self._ref_Value = {}

    def registerRow( self, idxRow, row ):
        refIndex = None
        try:
            refIndex = self._ref_Value.get( row[ self._col ] )
        except Exception as e:
            pass

        if not refIndex:
            if( self._next_index +1 ) >= len(self._colIndex):
                refIndex = SSIndexM1( self._colIndex, self._src, self._next_index )
            else:
                refIndex = SSIndex( self._colIndex, self._src, self._next_index )
        self._ref_Value[ row[ self._col ] ] = refIndex
        refIndex.registerRow( idxRow, row )

    def getIndexRef( self, keys, outRslt, index_level =0 ):
        if( index_level >= len(keys) ):
            getAll( outRslt )
            return 
        nextIndex = self._ref_Value.get( keys[index_level] )
        if not nextIndex:
            return
        nextIndex.getIndexRef( keys, outRslt, index_level +1 )

    def unregisterRow( self, idxRow, row ):
        ''' return true if empty
        '''
#        for k, y in self._ref_Value.items():                
        v = row[self._col]
        y = self._ref_Value.get( v )
        if not y:
            return True

        if y.unregisterRow( idxRow, row ):    
            del self._ref_Value[ v ]

        if len(self._ref_Value) == 0:
            return True
        return False

    def getAllItem( self, outRs ):
        for k,v in self._ref_Value.items():
            v.getAllItem( outRs )

    def isIndex( self, col ):
        if super( SSIndex, self).isIndex( col ):
            return True
        for i in xrange(0, len(self._colIndex) ):
            if col == i :
                return True
        return False


