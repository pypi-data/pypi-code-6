"""
Probe queries the database to get detailed information about its structure.

If the server type can be determined, the Connection object instantiates Probe,
or one of its subclasses, in the Connection.probe attribute.
"""

from .cursors import Record as _Record

class Probe(object):
    """
    Probe database schemata.

    There is no universal way to probe a database's structure. But Probe will work 
    with databases that provide information_schema views. Other database must 
    subclass Probe and return the same column names.
    """
    hasSchema = True
    def __init__(self, connection):
        if hasattr(connection, 'cursor') and callable(getattr(connection, 'cursor')):
            self._server = connection._server
            self._cursor = connection.cursor(None, logger=None)
            self._dbname = connection.dbname
        else:
            raise TypeError('First argument must be a dbms.Connection')
        
    def getServerVersion(self):
        """Get version of database engine"""
        query = 'SELECT version() AS version'
        return self._cursor.selectinto(query)
    
    def getDatabases(self):
        """Return list of databases."""
        raise NotImplementedError('No cross DBMS way to list databases.')
    
    def getSchemas(self):
        """Return list of schemas. [Record(name, is_connected_db, sys_ind)]."""
        query = '''SELECT LOWER(ss.schema_name) AS name, 
          CASE WHEN schema_name = %s THEN 1 ELSE 0 END is_connected_db,
          CASE WHEN schema_name = 'information_schema' THEN 1
            WHEN lower(substring(schema_name, 1, 3)) IN ('pg_', 'db_') THEN 2
            WHEN schema_name IN ('mysql', 'sys', 'dbo', 'guest') THEN 2
            ELSE 0 END sys_ind
        FROM information_schema.schemata ss 
        ORDER BY is_connected_db DESC, sys_ind, ss.schema_name''' % (
            self._cursor.placeholder)
        self._cursor.execute(query, (self._dbname,))
        return self._cursor.fetchall()
    
    def getTables(self, schema=None):
        """Return list of tables. [Record(name, schema_name, sys_ind)]"""
        query = '''SELECT table_name AS name, table_schema AS schema_name, 
          CASE WHEN table_schema IN ('information_schema', 'pg_catalog') 
          THEN 1 ELSE 0 END AS sys_ind
        FROM information_schema.tables t
        WHERE t.table_type = 'BASE TABLE'
          AND t.table_schema = COALESCE(LOWER(%s), t.table_schema)
        ORDER BY 3, 2, 1''' % self._cursor.placeholder
        self._cursor.execute(query, (schema,))
        return self._cursor.fetchall()
    
    def getViews(self, schema=None):
        """Return list of views. [Record(name, schema_name, sys_ind)]"""
        query = '''SELECT table_name  AS name, table_schema AS schema_name,
        CASE WHEN table_schema IN ('information_schema', 'pg_catalog')
        THEN 1 ELSE 0 END sys_ind
        FROM information_schema.views v
        WHERE v.table_schema = COALESCE(lower(%s), v.table_schema)
        ORDER BY 2, 1''' % self._cursor.placeholder
        self._cursor.execute(query, (schema,))
        return self._cursor.fetchall()
    
    def getFunctions(self, schema=None):
        """Return list of functions. [Record(name, schema_name, sys_ind)]"""
        query = '''SELECT DISTINCT r.routine_name AS name,
          r.routine_schema             AS schema_name,
          CASE WHEN r.routine_schema IN ('pg_catalog') 
            THEN 1 ELSE 0 END   sys_ind
        FROM information_schema.routines r
        WHERE r.routine_type = 'FUNCTION'
          AND r.routine_schema = COALESCE(%s, r.routine_schema)
          AND substring(routine_name, 1, 1) != '_'
        ORDER BY 3, 2, 1''' % self._cursor.placeholder
        self._cursor.execute(query, (schema,))
        return self._cursor.fetchall()
        
    def getProcedures(self, schema=None):
        """Return list of procedures. [Record(name, schema_name, sys_ind)]"""
        query = '''SELECT DISTINCT r.routine_name AS name,
          r.routine_schema                    AS schema_name,
          CASE WHEN r.routine_schema IN ('pg_catalog') 
            THEN 1 ELSE 0 END   sys_ind
        FROM information_schema.routines r
        WHERE r.routine_type = 'PROCEDURE'
          AND substring(routine_name, 1, 1) != '_'
          AND r.routine_schema = COALESCE(%s, r.routine_schema)
        ORDER BY 3, 2, 1''' % self._cursor.placeholder
        self._cursor.execute(query, (schema,))
        return self._cursor.fetchall()
    
    def getColumns(self, table, schema=None):
        """Return list of table/view columns. [Record(name, data_type, is_nullable, is_pk)]"""
        query = '''SELECT c.column_name AS name, c.data_type, 
          substring(c.is_nullable, 1, 1) is_nullable,
          CASE WHEN kc.column_name IS NOT NULL THEN 'Y' END is_pk
        FROM information_schema.columns c
        LEFT JOIN information_schema.table_constraints tc 
          ON c.table_schema = tc.table_schema
          AND c.table_name = tc.table_name
          AND tc.constraint_type = 'PRIMARY KEY'
        LEFT JOIN information_schema.key_column_usage kc
          ON c.table_schema = kc.table_schema
          AND c.table_name = kc.table_name
          AND tc.constraint_name = kc.constraint_name
          AND c.column_name = kc.column_name
        WHERE LOWER(c.table_name) = LOWER(%s)
          AND LOWER(c.table_schema) = COALESCE(LOWER(%s), c.table_schema)
        ORDER BY c.ordinal_position''' % (self._cursor.placeholder, 
                                          self._cursor.placeholder)
        self._cursor.execute(query, (table, schema))
        return self._cursor.fetchall()

class ProbeOracle(Probe):
    def getServerVersion(self):
        """Get version of database engine"""
        query = 'SELECT banner FROM v$version WHERE rownum = 1'
        return self._cursor.selectinto(query)
    
    def getDatabases(self):
        print('Oracle has only one database per instance')
        return []
    
    def getSchemas(self):
        """Return list of schemas. [Record(name, is_connected_db, sys_ind)]."""
        # just return schema that have objects
        query = '''SELECT username name, NULL AS is_connected_db,
          CASE WHEN username LIKE '%SYS%' THEN 1 ELSE 0 END sys_ind
        FROM all_users u
        WHERE EXISTS (SELECT 1 FROM all_objects o WHERE u.username = o.owner)
        ORDER BY 1'''
        self._cursor.execute(query)
        return self._cursor.fetchall()
    
    def getTables(self, schema=None):
        """Return list of tables. [Record(name, schema_name, sys_ind)]"""
        query = '''SELECT t.table_name AS name, t.owner schema_name, num_rows,
          CASE WHEN t.owner LIKE 'SYS%' THEN 1 ELSE 0 END AS sys_ind
        FROM all_tables t WHERE t.OWNER = COALESCE(UPPER(:0), t.owner)
        ORDER BY 2, 1'''
        self._cursor.execute(query, (schema,))
        return self._cursor.fetchall()
    
    def getViews(self, schema=None):
        """Return list of views. [Record(name, schema_name, sys_ind)]"""
        query = '''SELECT view_name AS name, owner schema_name,
        CASE WHEN owner LIKE 'SYS%' THEN 1 ELSE 0 END AS sys_ind
        FROM all_views v WHERE v.owner = COALESCE(UPPER(:0), v.owner)
        ORDER BY 2, 1'''
        self._cursor.execute(query, (schema,))
        return self._cursor.fetchall()
    
    def getFunctions(self, schema=None):
        """Return list of functions. [Record(name, schema_name, sys_ind)]"""
        query = '''SELECT p.object_name name,
          p.owner                   schema_name,
          CASE WHEN owner LIKE 'SYS%' THEN 1 ELSE 0 END sys_ind
        FROM all_procedures p
        WHERE p.object_type = 'FUNCTION'
          AND p.owner = COALESCE(UPPER(:0), p.owner)
          AND COALESCE(p.overload, '1') = '1'
        ORDER BY 3, 2, 1'''
        self._cursor.execute(query, (schema,))
        return self._cursor.fetchall()
    
    def getProcedures(self, schema=None):
        """Return list of procedures. [Record(name, schema_name, sys_ind)]"""
        query = '''SELECT p.object_name name,
          p.owner                   schema_name,
          CASE WHEN owner LIKE 'SYS%' THEN 1 ELSE 0 END sys_ind
        FROM all_procedures p
        WHERE p.object_type = 'PROCEDURE'
          AND p.owner = COALESCE(UPPER(:0), p.owner)
          AND COALESCE(p.overload, '1') = '1'
        ORDER BY 3, 2, 1'''
        self._cursor.execute(query, (schema,))
        return self._cursor.fetchall()
    
    def getPackages(self, schema=None):
        """Return list of packages. [Record(name, schema_name, sys_ind)]"""
        query = '''SELECT p.object_name name,
          p.owner                   schema_name,
          CASE WHEN owner LIKE 'SYS%' THEN 1 ELSE 0 END sys_ind
        FROM all_procedures p
        WHERE p.object_type = 'PACKAGE'
          AND p.owner = COALESCE(UPPER(:0), p.owner)
          AND p.subprogram_id = 0
        ORDER BY 3, 2, 1'''
        self._cursor.execute(query, (schema,))
        return self._cursor.fetchall()
    
    def getPackageProcedures(self, package, schema=None):
        """Return list of functions/procedures in a package. [Record(name, package_name, schema_name)]"""
        query = '''SELECT p.procedure_name name,
          p.object_name                package_name,
          p.owner                      schema_name
        FROM all_procedures p
        WHERE p.object_type = 'PACKAGE'
          AND p.object_name = UPPER(:0)
          AND p.owner = COALESCE(UPPER(:1), p.owner)
          AND p.subprogram_id > 0
          AND COALESCE(p.overload, '1') = '1'
        ORDER BY p.subprogram_id'''
        self._cursor.execute(query, (package, schema))
        return self._cursor.fetchall()
    
    def getColumns(self, table, schema=None):
        """Return list of table/view columns. [Record(name, data_type, is_nullable, is_pk)]"""
        query = '''SELECT c.column_name name, c.data_type, c.nullable is_nullable,
          CASE WHEN cc.column_name IS NOT NULL THEN 'Y' END is_pk
        FROM all_tab_columns c
        LEFT JOIN all_constraints tc ON c.owner = tc.owner
          AND c.table_name = tc.table_name
          AND tc.constraint_type = 'P'
        LEFT JOIN all_cons_columns cc ON tc.owner = cc.owner
          AND tc.table_name = cc.table_name 
          AND tc.constraint_name = cc.constraint_name 
          AND c.column_name = cc.column_name
        WHERE c.table_name = UPPER(:1)
          AND c.owner = COALESCE(UPPER(:2), c.owner)
        ORDER BY c.column_id'''
        self._cursor.execute(query, (table, schema))
        return self._cursor.fetchall()

class ProbeSQLite(Probe):
    hasSchema = False
    def getServerVersion(self):
        """Get version of database engine"""
        query = '''select 'SQLite ' ||  sqlite_version() AS version'''
        return self._cursor.selectinto(query)
    
    def getDatabases(self):
        """Return list of databases."""
        self._cursor.execute('PRAGMA database_list')
        return [(rec['name'], rec['file']) for rec in self._cursor]
    
    def getSchemas(self):
        """Return list of schemas. [Record(name, is_connected_db, sys_ind)]."""
        print('SQLite does not have schema.')
        return []
    
    def getTables(self, schema=None):
        """Return list of tables. [Record(name, schema_name, sys_ind)]"""
        query = '''SELECT name, NULL AS schema_name,
        CASE WHEN name LIKE 'sqlite$_' escape '$' 
          THEN 1 ELSE 0 END AS sys_ind 
        FROM sqlite_master WHERE type = 'table' 
        ORDER BY 1 '''
        self._cursor.execute(query)
        return self._cursor.fetchall()
    
    def getViews(self, schema=None):
        """Return list of views. [Record(name, schema_name, sys_ind)]"""
        query = '''SELECT name, NULL AS schema_name,
        CASE WHEN name LIKE 'sqlite$_' escape '$' 
          THEN 1 ELSE 0 END AS sys_ind 
        FROM sqlite_master WHERE type = 'view' 
        ORDER BY 1'''
        self._cursor.execute(query)
        return self._cursor.fetchall()
    
    def getFunctions(self, schema=None):
        """Return list of functions. [Record(name, schema_name, sys_ind)]"""
        print('SQLite does not support user defined functions.')
        return []
    
    def getProcedures(self, schema=None):
        """Return list of procedures. [Record(name, schema_name, sys_ind)]"""
        print('SQLite does not support user defined procedures')
        return []
    
    def getColumns(self, table, schema=None):
        """Return list of table/view columns. [Record(name, data_type, is_nullable, is_pk)]"""
        query = 'PRAGMA table_info(\'%s\')' % table
        self._cursor.execute(query)
        rowType = type('Record', (_Record,),
                   {'_fields': ['name', 'data_type', 'is_nullable', 'is_pk']})

        return [rowType(rec['name'], rec['type'], 'YN'[bool(rec['notnull'])], 'NY'[bool(rec['pk'])])
                for rec in self._cursor]
    
class ProbePostgres(Probe):
    def getDatabases(self):
        """Return list of databases/catalogs."""
        query = '''SELECT datname AS name FROM pg_database 
        WHERE datistemplate=false ORDER BY 1'''
        self._cursor.execute(query)
        return self._cursor.fetchall()
    
class ProbeMySQL(Probe):   
    def getDatabases(self):
        """Return list of databases/catalogs."""
        query = '''SELECT ss.schema_name AS name 
        FROM information_schema.schemata ss ORDER BY 1'''
        self._cursor.execute(query)
        return self._cursor.fetchall()
    
    def getSchemas(self):
        """Return list of schemas. [Record(name, is_connected_db, sys_ind)]."""
        # databases == schemas on mysql
        return self.getDatabases()
       
class ProbeMSSQL(Probe):
    def getServerVersion(self):
        """Get version of database engine."""
        query = 'SELECT @@version'
        return self._cursor.selectinto(query)
    
    def getDatabases(self):
        """Return list of databases/catalogs."""
        query = '''SELECT name
        FROM master..sysdatabases WHERE sid != 1
        ORDER BY CASE WHEN name = %s THEN 0
        ELSE 1 END, name'''
        self._cursor.execute(query, (self._cursor.connection.dbname,))
        return self._cursor.fetchall()
    
class ProbeFirebird(Probe):
    hasSchema = False
    def getServerVersion(self):
        """Get version of database engine"""
        query = '''SELECT 'Firebird ' || rdb$get_context('SYSTEM', 'ENGINE_VERSION') 
            AS version FROM rdb$database'''
        return self._cursor.selectinto(query)
    
    def getDatabases(self):
        """Return list of databases/catalogs."""
        print('Not supported on Firebird.')
        return []
    
    def getSchemas(self):
        """Return list of schemas. [Record(name, is_connected_db, sys_ind)]."""
        # Firebird doesn't have schema. Return a list of object owners instead. 
        query = '''SELECT DISTINCT TRIM(rdb$owner_name) name, NULL is_connected_db, 
          NULL sys_ind
        FROM rdb$relations ORDER BY 1'''
        self._cursor.execute(query)
        return self._cursor.fetchall()
    
    def getTables(self, schema=None):
        """Return list of tables. [Record(name, schema_name, sys_ind)]"""
        query = '''SELECT TRIM(rdb$relation_name) name,
              TRIM(rdb$owner_name) schema_name,
              rdb$system_flag sys_ind
            FROM rdb$relations 
            WHERE rdb$view_blr IS NULL
              AND rdb$owner_name  = COALESCE(?, rdb$owner_name)
            ORDER BY 3, 2, 1'''
        self._cursor.execute(query, (schema,))
        return self._cursor.fetchall()
    
    def getViews(self, schema=None):
        """Return list of views. [Record(name, schema_name, sys_ind)]"""
        query = '''SELECT TRIM(rdb$relation_name) name,
              TRIM(rdb$owner_name) schema_name,
              rdb$system_flag sys_ind
            FROM rdb$relations 
            WHERE rdb$view_blr IS NOT NULL
              AND rdb$owner_name  = COALESCE(?, rdb$owner_name)
            ORDER BY 3, 2, 1'''
        self._cursor.execute(query, (schema,))
        return self._cursor.fetchall()
    
    def getFunctions(self, schema=None):
        """Return list of functions. [Record(name, schema_name, sys_ind)]"""
        query = '''SELECT TRIM(rdb$function_name) name, 
              NULL                          schema_name,
              rdb$system_flag               sys_ind 
            FROM rdb$functions
            ORDER BY 3, 1'''
        self._cursor.execute(query)
        return self._cursor.fetchall()
    
    def getProcedures(self, schema=None):
        """Return list of procedures. [Record(name, schema_name, sys_ind)]"""
        query = '''SELECT TRIM(rdb$procedure_name) name, 
              NULL                           schema_name,
              rdb$system_flag                sys_ind 
            FROM rdb$procedures
            ORDER BY 3, 1'''
        self._cursor.execute(query)
        return self._cursor.fetchall()
    
    def getColumns(self, table, schema=None):
        """Return list of table/view columns. [Record(name, data_type, is_nullable, is_pk)]"""
        query = '''SELECT TRIM(rf.RDB$FIELD_NAME) AS name,
              TRIM(CASE f.RDB$FIELD_TYPE
                  WHEN 261 THEN 'BLOB'
                  WHEN 14 THEN 'CHAR'
                  WHEN 40 THEN 'C STRING'
                  WHEN 11 THEN 'D_FLOAT'
                  WHEN 27 THEN 'DOUBLE'
                  WHEN 10 THEN 'FLOAT'
                  WHEN 16 THEN 'INT64'
                  WHEN 8 THEN 'INTEGER'
                  WHEN 9 THEN 'QUAD'
                  WHEN 7 THEN 'SMALLINT'
                  WHEN 12 THEN 'DATE'
                  WHEN 13 THEN 'TIME'
                  WHEN 35 THEN 'TIMESTAMP'
                  WHEN 37 THEN 'VARCHAR'
                  ELSE 'UNKNOWN'
              END) AS data_type,
              CASE WHEN rf.RDB$NULL_FLAG = 1 THEN 0 ELSE 1 END is_nullable,
              CASE WHEN seg.RDB$FIELD_NAME IS NOT NULL THEN 1 END pk_ind
            FROM RDB$RELATION_FIELDS rf
            JOIN RDB$FIELDS f ON rf.RDB$FIELD_SOURCE = f.RDB$FIELD_NAME
            LEFT JOIN RDB$RELATION_CONSTRAINTS rc ON rf.RDB$RELATION_NAME = rc.RDB$RELATION_NAME
              AND rc.RDB$CONSTRAINT_TYPE = 'PRIMARY KEY'
            LEFT JOIN RDB$INDEX_SEGMENTS seg ON rc.RDB$INDEX_NAME = seg.RDB$INDEX_NAME
              AND rf.RDB$FIELD_NAME = seg.RDB$FIELD_NAME
            WHERE UPPER(rf.RDB$RELATION_NAME) = UPPER(?)
            ORDER BY rf.RDB$FIELD_POSITION '''
        self._cursor.execute(query, (table,))
        return self._cursor.fetchall()
    
class ProbeDB2(Probe):
    def getServerVersion(self):
        """Get version of database engine"""
        query = ''' SELECT service_level FROM TABLE(SYSPROC.ENV_GET_INST_INFO())'''
        return self._cursor.selectinto(query)
    
    def getDatabases(self):
        """Return list of databases/catalogs."""
        return []
    
    def getSchemas(self):
        """Return list of schemas. [Record(name, is_connected_db, sys_ind)]."""
        query = '''SELECT schemaname AS name,
          CASE WHEN schemaname LIKE 'SYS%' THEN 2
            WHEN definertype = 'U' THEN 0
            ELSE 2 END AS sys_ind 
        FROM syscat.schemata
        ORDER BY 2, 1'''
        self._cursor.execute(query)
        return self._cursor.fetchall()
    
    def getTables(self, schema=None):
        """Return list of tables. [Record(name, schema_name, sys_ind)]"""
        query = '''SELECT tabname AS name,
          TRIM(tabschema) AS schema_name, 
          CASE WHEN tabschema LIKE 'SYS%' THEN 1
          WHEN ownertype = 'U' THEN 0
          ELSE 1 END sys_ind
        FROM syscat.tables t
        WHERE type = 'T'
          AND tabschema = COALESCE(?, tabschema)
        ORDER BY 3,2,1'''
        self._cursor.execute(query, (schema,))
        return self._cursor.fetchall()
    
    def getViews(self, schema=None):
        """Return list of views. [Record(name, schema_name, sys_ind)]"""
        query = '''SELECT viewname AS name,
          TRIM(viewschema) AS schema_name,
          CASE WHEN ownertype = 'U' THEN 0 
          ELSE 1 END AS sys_ind
        FROM syscat.views
        WHERE viewschema = COALESCE(?, viewschema)
        ORDER BY 3, 2 , 1'''
        self._cursor.execute(query, (schema,))
        return self._cursor.fetchall()
        
    def getFunctions(self, schema=None):
        """Return list of functions. [Record(name, schema_name, sys_ind)]"""
        query = '''SELECT DISTINCT funcname AS name,
          TRIM(funcschema) AS schema_name,
          CASE WHEN funcschema LIKE 'SYS%' THEN 1 ELSE 0 END sys_ind
        FROM syscat.functions
        WHERE substr(funcname,1,1) NOT IN ('<', '>', '=')
          AND funcschema = COALESCE(?, funcschema)
        ORDER BY 2, 1'''
        self._cursor.execute(query, (schema,))
        return self._cursor.fetchall()
        
    def getProcedures(self, schema=None):
        """Return list of procedures. [Record(name, schema_name, sys_ind)]"""
        query = '''SELECT DISTINCT procname AS name,
          TRIM(procschema) AS schema_name, 
          CASE WHEN procschema LIKE 'SYS%' THEN 1 ELSE 0 END sys_ind
        FROM syscat.procedures
        WHERE procschema = COALESCE(?, procschema)
        ORDER BY 1, 2'''
        self._cursor.execute(query, (schema,))
        return self._cursor.fetchall()
    
    def getColumns(self, table, schema=None):
        """Return list of table/view columns. [Record(name, data_type, is_nullable, is_pk)]"""
        query = '''SELECT colname AS name,
          typename AS data_type,
          CASE WHEN c.nulls = 'Y' THEN 1 ELSE 0 END AS is_nullable,
          CASE WHEN keyseq IS NOT NULL THEN 1 ELSE 0 END AS is_pk
        FROM syscat.columns c
        WHERE tabname = ?
          AND tabschema = COALESCE(?, tabschema) 
        ORDER BY colno'''
        self._cursor.execute(query, (table, schema))
        return self._cursor.fetchall()