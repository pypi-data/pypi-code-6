#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE":
# <utn_kdd@googlegroups.com> wrote this file. As long as you retain this notice
# you can do whatever you want with this stuff. If we meet some day, and you
# think this stuff is worth it, you can buy us a WISKEY us return.


#===============================================================================
# DOCS
#===============================================================================

"""Database abstraction layer.

"""

#===============================================================================
# DEVELOPER NOTES
#===============================================================================

# first see this video https://www.youtube.com/watch?v=woKYyhLCcnU
# then: http://docs.sqlalchemy.org/en/latest/core/tutorial.html
# and then: http://docs.sqlalchemy.org/en/latest/core/connections.html


#===============================================================================
# IMPORTS
#===============================================================================

import uuid
import datetime
import string
import decimal

import sqlalchemy as sa
from sqlalchemy import sql
from sqlalchemy.engine import url

from yatel import dom


#===============================================================================
# CONSTANTS
#===============================================================================

#: Available engines
ENGINES = (
    'sqlite',
    'memory',
    'mysql',
    'postgres',
)


#: Connection uris for the existing engines
ENGINE_URIS = {
    'sqlite': "sqlite:///${database}",
    'memory': "sqlite://",
    'mysql': "mysql://${user}:${password}@${host}:${port}/${database}",
    'postgres': "postgres://${user}:${password}@${host}:${port}/${database}"
}


#: Variables of the uris
ENGINE_VARS = {}
for engine in ENGINES:
    tpl = string.Template(ENGINE_URIS[engine])
    variables = []
    for e, n, b, i in tpl.pattern.findall(tpl.template):
        if n or b:
            variables.append(n or b)
    ENGINE_VARS[engine] = variables


#: This dictionary maps Python types to functions, converts the given type
#: instance to a correct sqlalchemy column type.
#: To retrieve all suported types use db.SQL_ALCHEMY_TYPES.keys()
SQL_ALCHEMY_TYPES = {
    datetime.datetime: lambda x: sa.DateTime(),
    datetime.time: lambda x: sa.Time(),
    datetime.date: lambda x: sa.Date(),
    bool: lambda x: sa.Boolean(),
    int: lambda x: sa.Integer(),
    long: lambda x: sa.BigInteger(),
    float: lambda x: sa.Float(),
    str: lambda x: sa.String(500) if len(x) < 500 else sa.Text(),
    unicode: lambda x: sa.String(500) if len(x) < 500 else sa.Text(),
    decimal.Decimal: lambda x: sa.Numeric()
}


#: This dictionary maps sqlalchemy Column types to functions, converts the
#: given Column class to python type.
#: To retrieve all suported columns use db.PYTHON_TYPES.keys()
PYTHON_TYPES = {
    sa.DateTime: lambda x: datetime.datetime,
    sa.Time: lambda x: datetime.time,
    sa.Date: lambda x: datetime.date,
    sa.Boolean: lambda x: bool,
    sa.BigInteger: lambda x: long,
    sa.Integer: lambda x: int,
    sa.Float: lambda x: float,
    sa.String: lambda x: str,
    sa.Text: lambda x: unicode,
    sa.Numeric: lambda x: decimal.Decimal,
}

# TABLE NAMES

#: The name of the haplotypes table
HAPLOTYPES = "haplotypes"

#: The name of the facts table
FACTS = "facts"

#: The name of the edges table
EDGES = "edges"

#: A collection with the 3 table names
TABLES = (HAPLOTYPES, FACTS, EDGES)

# MODES

#: Constant of read-only mode
MODE_READ = "r"

#: Constant of write mode (Destroy the existing database)
MODE_WRITE = "w"

#: Constant of append mode
MODE_APPEND = "a"

#: The 3 modes to open the databases
MODES = (MODE_READ, MODE_WRITE, MODE_APPEND)


#===============================================================================
# ERROR
#===============================================================================

class YatelNetworkError(Exception):
    """Error to use when some Yatel logic fails in the database."""
    pass


#===============================================================================
# NETWORK
#===============================================================================


class YatelNetwork(object):
    """Abstraction layer for yatel network databases.
    
    """
    
    def __init__(self, engine, mode=MODE_READ, log=None, **kwargs):
        """Creates a new instance.

        Parameters
        ----------
        engine : str
            pick one of the :py:data:`yatel.db.ENGINES`
        mode : str
            The mode to open the database.
                - If mode is **r** the network will reflect all the
                existing yatel collections in the database.
                - If mode is **w** yatell will destroy all the
                collections.
                - If mode is **a** all the elements are copied to a temporal
                table and the network is ready to accept more elements
        log : None or bool
            Print the log of the backend to the standar output
        kwargs : a dict of arguments for the ``engine``.
                Extra arguments for a given ``engine`` (see :py:data:`yatel.db.ENGINE_VARS`)

        Examples
        --------
        **Log enabled**

        >>> from yatel import db, dom
        >>> nw = db.YatelNetwork("memory", mode="w", log=True)
        [ ... LOGS ... ]


        **Write mode**

        >>> nw = db.YatelNetwork("sqlite", mode="w", log=False, database="nw.db")
        >>> nw.add_element(dom.Haplotype(1))
        >>> nw.confirm_changes() # change read mode
        >>> len(tuple(nw.haplotypes_iterator()))
        1


        **Append to previous network**

        >>> nw = db.YatelNetwork("sqlite", mode="a", log=False, database="nw.db")
        >>> nw.add_element(dom.Haplotype(2))
        >>> nw.confirm_changes() # change read mode
        >>> len(tuple(nw.haplotypes_iterator()))
        2


        **Destroy previous data**

        >>> nw = db.YatelNetwork("sqlite", mode="w", log=False, database="nw.db")
        >>> nw.add_element(dom.Haplotype(3))
        >>> nw.confirm_changes() # change read mode
        >>> len(tuple(nw.haplotypes_iterator()))
        1

        """
        self._uri = to_uri(engine, **kwargs)

        self._engine_name = engine

        self._engine = sa.create_engine(self._uri, echo=bool(log))
        self._metadata = sa.MetaData(self._engine)

        self._mode = mode
        self._descriptor = None

        if mode == MODE_READ:
            try:
                self._metadata.reflect(only=TABLES)
            except sa.exc.InvalidRequestError:
                raise YatelNetworkError("Invalid database")
            self.haplotypes_table = self._metadata.tables[HAPLOTYPES]
            self.facts_table = self._metadata.tables[FACTS]
            self.edges_table = self._metadata.tables[EDGES]
        else:

            if mode == MODE_WRITE:
                self._metadata.reflect()
                self._metadata.drop_all()
                self._metadata.clear()

            self._column_buff = {HAPLOTYPES: [], FACTS: [], EDGES: 0}
            self._create_objects = sa.Table(
                "_tmp_yatel_objs_{}".format(uuid.uuid4()), self._metadata,
                sa.Column("id", sa.Integer(), primary_key=True),
                sa.Column("tname", sa.String(length=15), nullable=False),
                sa.Column("data", sa.PickleType(), nullable=False),
                prefixes=['TEMPORARY'],
            )
            self._create_conn = self._metadata.bind.connect()
            self._create_objects.create(self._create_conn)
            self._create_trans = self._create_conn.begin()

            if mode == MODE_APPEND:
                self._creation_append = True
                try:
                    self._metadata.reflect(only=TABLES)
                except sa.exc.InvalidRequestError:
                    raise YatelNetworkError("Invalid database")
                self.haplotypes_table = self._metadata.tables[HAPLOTYPES]
                self.facts_table = self._metadata.tables[FACTS]
                self.edges_table = self._metadata.tables[EDGES]
                self.add_elements(self.haplotypes())
                self.add_elements(self.facts())
                self.add_elements(self.edges())
                self._metadata.drop_all(
                    self._create_conn,
                    tables=[self.haplotypes_table,
                            self.facts_table,
                            self.edges_table]
                )
                self._metadata.remove(self.haplotypes_table)
                self._metadata.remove(self.facts_table)
                self._metadata.remove(self.edges_table)
                del self.haplotypes_table
                del self.facts_table
                del self.edges_table
                del self._creation_append


    #===========================================================================
    # PRIVATE
    #===========================================================================

    def _new_attrs(self, attnames, table):
        columns = [c.name for c in self._column_buff[table]]
        return set(attnames).difference(columns)

    def _row2hap(self, row):
        attrs = dict([
            (k, v) for k, v in row.items()
            if k != "hap_id" and v != None
        ])
        hap_id = row["hap_id"]
        return dom.Haplotype(hap_id, **attrs)

    def _row2fact(self, row):
        attrs = dict([
            (k, v) for k, v in row.items()
            if k not in ("id", "hap_id") and v != None
        ])
        hap_id = row["hap_id"]
        return dom.Fact(hap_id, **attrs)

    def _row2edge(self, row):
        haps = [v for k, v in row.items()
                if k not in ("id", "weight") and v != None]
        weight = row["weight"]
        return dom.Edge(weight, haps)

    #===========================================================================
    # DDL METHODS
    #===========================================================================

    def add_elements(self, elems):
        """Add multiple instaces of :py:class:`yatel.dom.Haplotype` or 
        :py:class:`yatel.dom.Fact` or :py:class:`yatel.dom.Edge` instance. 
        The network must be in **w** or **a** mode.

        Parameters
        ----------
        elems : iterable of :py:class:`yatel.dom.Haplotype` or \
        :py:class:`yatel.dom.Fact` or :py:class:`yatel.dom.Edge` instances.
            Elements to be added in the network.

        Examples
        --------
        >>> nw = db.YatelNetwork("sqlite", mode="w", log=False, database="nw.db")
        >>> nw.add_element([dom.Haplotype(3), dom.Fact(3, att0="foo")])

        """
        map(self.add_element, elems)

    def add_element(self, elem):
        """Add single instance of :py:class:`yatel.dom.Haplotype` or 
        :py:class:`yatel.dom.Fact` or :py:class:`yatel.dom.Edge`.
        The network must be in **w** or **a** mode.

        **REQUIRE MODE:** w|a

        Parameters
        ----------
        elems : instance of :py:class:`yatel.dom.Haplotype` or \
        :py:class:`yatel.dom.Fact` or :py:class:`yatel.dom.Edge`.
            Element to add.

        Examples
        --------
        >>> nw = db.YatelNetwork("sqlite", mode="w", log=False, database="nw.db")
        >>> nw.add_element(dom.Fact(3, att0="foo"))

        """

        if self.mode == MODE_READ:
            raise YatelNetworkError("Network in read-only mode")

        data = None
        tname = None

        # determine the hap_id columns
        if isinstance(elem, (dom.Haplotype, dom.Fact)) \
           and not self._column_buff[HAPLOTYPES]:
                avalue = elem.hap_id
                atype = type(avalue)
                ctype = SQL_ALCHEMY_TYPES[atype](avalue)
                if isinstance(ctype, sa.Text):
                    ctype = sa.String(500)
                extra_params = {}
                if isinstance(ctype, sa.Integer):
                    extra_params["autoincrement"] = False
                self._column_buff[HAPLOTYPES].append(
                    sa.Column("hap_id", ctype,
                              index=True, primary_key=True, **extra_params)
                )
                self._column_buff[FACTS].append(
                    sa.Column("hap_id", ctype,
                              sa.ForeignKey('{}.hap_id'.format(HAPLOTYPES)),
                              index=True, nullable=False)
                )

        if isinstance(elem, dom.Haplotype):
            new_attrs_names = self._new_attrs(elem.keys(), HAPLOTYPES)
            for aname in new_attrs_names:
                avalue = elem[aname]
                atype = type(avalue)
                ctype = SQL_ALCHEMY_TYPES[atype](avalue)
                column = sa.Column(aname, ctype, index=True, nullable=True)
                self._column_buff[HAPLOTYPES].append(column)
            data = dict(elem)
            tname = HAPLOTYPES

        elif isinstance(elem, dom.Fact):
            new_attrs_names = self._new_attrs(elem.keys(), FACTS)
            for aname in new_attrs_names:
                avalue = elem[aname]
                atype = type(avalue)
                ctype = SQL_ALCHEMY_TYPES[atype](avalue)
                column = sa.Column(aname, ctype, index=True, nullable=True)
                self._column_buff[FACTS].append(column)
            data = dict(elem)
            tname = FACTS

        elif isinstance(elem, dom.Edge):
            if len(elem.haps_id) > self._column_buff[EDGES]:
                self._column_buff[EDGES] = len(elem.haps_id)
            data = {}
            for idx, hap_id in enumerate(elem.haps_id):
                data["hap_{}".format(idx)] = hap_id
            data["weight"] = elem.weight
            tname = EDGES

        # if is trash
        else:
            msg = "Object '{}' is not yatel.dom type".format(str(elem))
            raise TypeError(msg)
        self._create_conn.execute(self._create_objects.insert(),
                                  tname=tname, data=data)

    def confirm_changes(self):
        """Creates the subjacent structures to store the elements added
        and changes to read mode.

        Examples
        --------
        >>> from yatel import db, dom
        >>> nw = db.YatelNetwork("sqlite", mode="w", log=False, database="nw.db")
        >>> nw.add_element(dom.Haplotype(3, att0="foo"))
        >>> nw.confirm_changes()
        >>> nw.haplotype_by_id(3)
        <Haplotype '3' at 0x37a9890>

        """
        if self.mode == MODE_READ:
            raise YatelNetworkError("Network in read-only mode")

        # create te tables
        self.haplotypes_table = sa.Table(
            HAPLOTYPES, self._metadata, *self._column_buff[HAPLOTYPES]
        )

        self.facts_table = sa.Table(
            FACTS, self._metadata,
            sa.Column("id", sa.Integer(), primary_key=True),
            *self._column_buff[FACTS]
        )

        edges_columns = [
            sa.Column("hap_{}".format(idx),
                      self.haplotypes_table.c.hap_id.type,
                      sa.ForeignKey(HAPLOTYPES + '.hap_id'),
                      index=True, nullable=True)
            for idx in range(self._column_buff[EDGES])
        ]
        self.edges_table = sa.Table(
            EDGES, self._metadata,
            sa.Column("id", sa.Integer(), primary_key=True),
            sa.Column("weight", sa.Float(), nullable=False),
            *edges_columns
        )

        self._metadata.create_all(self._create_conn)

        try:
            query = sql.select([self._create_objects])
            for row in self._create_conn.execute(query):
                table = None
                if row.tname == HAPLOTYPES:
                    table = self.haplotypes_table
                elif row.tname == FACTS:
                    table = self.facts_table
                elif row.tname == EDGES:
                    table = self.edges_table
                else:
                    msg = "Invalid tname '{}'".format(row.tname)
                    raise YatelNetworkError(msg)
                self._create_conn.execute(table.insert(), **row.data)
        except Exception as err:
            self._create_trans.rollback()
            raise err
        else:
            self._create_trans.commit()

        # close all tmp references
        self._create_trans.close()
        self._create_conn.close()

        self._metadata.remove(self._create_objects)

        # destroys the buffers
        del self._column_buff
        del self._create_objects
        del self._create_conn
        del self._create_trans

        self._mode = MODE_READ

    #===========================================================================
    # QUERIES # use execute here
    #===========================================================================

    def validate_read(self):
        """Raise a ``YatelNetworkError`` if the network is not in read mode.

        Raises
        ------
        YatelNetworkError
            if the network is not in read mode.

        """
        if not getattr(self, "_creation_append", None):
            if self.mode != MODE_READ:
                raise YatelNetworkError("Network in {} mode".format(self.mode))

    def execute(self, query):
        """Execute a given ``query`` to the backend.

        **REQUIRE MODE:** r

        Parameters
        ----------
        query : a query for the backend
            A valid query for the backend.

        """
        self.validate_read()
        return self._engine.execute(query)

    def environments(self, facts_attrs=None):
        """Iterates over all combinations of environments of the given attrs.

        **REQUIRE MODE:** r

        Parameters
        ----------
        fact_attrs : iterable
            Collection of existing fact attribute names.

        Returns
        -------
        iterator
            Iterator of dictionaries with all valid combinations of
            values of a given ``fact_attrs`` names

        Examples
        --------
        >>> for env in nw.enviroments(["native", "place"]):
        ···     print env
        {u'place': None, u'native': True}
        {u'place': u'Hogwarts', u'native': False}
        {u'place': None, u'native': False}
        {u'place': u'Mordor', u'native': True}
        {u'place': None, u'native': None}
        ...

        """
        facts_attrs = facts_attrs or ()
        if "hap_id" in facts_attrs:
            raise ValueError("Invalid fact attr: 'hap_id'")
        if "id" in facts_attrs:
            raise ValueError("Invalid fact attr: 'id'")
        attrs = None
        if facts_attrs:
            attrs = facts_attrs
        else:
            attrs = tuple(
                k for k in self.describe()["fact_attributes"].keys()
                if k != "hap_id"
            )
        query = sql.select(
            [self.facts_table.c[k] for k in attrs]
        ).distinct()
        for row in self.execute(query):
            yield dom.Environment(**row)

    #===========================================================================
    # HAPLOTYPE QUERIES
    #===========================================================================

    def haplotypes(self):
        """Iterates over all :py:class:`yatel.dom.Haplotype` instances stored 
        in the database.

        **REQUIRE MODE:** r

        Returns
        -------
        iterator
            iterator of :py:class:`yatel.dom.Haplotypes` instances.

        """
        query = sql.select([self.haplotypes_table])
        for row in self.execute(query):
            yield self._row2hap(row)

    def haplotype_by_id(self, hap_id):
        """Return a :py:class:`dom.Haplotype` instace stored in the dabase 
        with the given ``hap_id``.

        **REQUIRE MODE:** r

        Parameters
        ----------
        hap_id : ``id`` of the haplotypes type table.

        Returns
        -------
        :py:class:`yatel.dom.Haplotype`
            :py:class:`yatel.dom.Haplotype` instance.

        """
        query = sql.select([self.haplotypes_table]).where(
            self.haplotypes_table.c.hap_id == hap_id
        ).limit(1)
        row = self.execute(query).fetchone()
        return self._row2hap(row)

    def haplotypes_by_environment(self, env=None, **kwargs):
        """Return an iterator of :py:class:`yatel.dom.Haplotype` related to a 
        :py:class:`yatel.dom.Fact` with attribute and value specified in 
        ``env`` and ``kwargs``.

        **REQUIRE MODE:** r

        Parameters
        ----------
        env : dict
            Keys are :py:class:`yatel.dom.Fact` attributes name, and value is 
            a possible value of the given attribute.
        kwargs : a dict of keywords arguments
            Keys are :py:class:`yatel.dom.Fact` attributes name, and value is 
            a possible value of the given attribute.

        Returns
        -------
        iterator
            Iterator of :py:class:`yatel.dom.Haplotype`.

        Examples
        --------
        >>> from yatel import db, dom
        >>> nw = db.YatelNetwork("sqlite", mode=db.MODE_WRITE, database="nw.db")
        >>> nw.add_elements([dom.Haplotype("hap1"),
        ···                  dom.Haplotype("hap2"),
        ···                  dom.Fact("hap1", a=1, c="foo"),
        ···                  dom.Fact("hap2", a=1, b=2),
        ···                  dom.Edge(1, ("hap1", "hap2"))])
        >>> nw.confirm_changes()
        >>> tuple(nw.haplotypes_enviroment(a=1))
        (<Haplotype 'hap1' at 0x2463250>, <Haplotype 'hap2' at 0x2463390>)
        >>> tuple(nw.haplotypes_enviroment({"c": "foo"}))
        (<Haplotype 'hap1' at 0x2463250>, )
        >>> tuple(nw.haplotypes_enviroment({"a": 1}, b=2))
        (<Haplotype 'hap2' at 0x2463390>, )

        """
        env = dict(env) if env else {}
        env.update(kwargs)
        where = sql.and_(*[self.facts_table.c[k] == v
                           for k, v in env.items()])
        query = sql.select([self.haplotypes_table]).select_from(
            self.haplotypes_table.join(
                self.facts_table,
                self.facts_table.c.hap_id == self.haplotypes_table.c.hap_id
            )
        ).where(where).distinct()
        for row in self.execute(query):
            yield self._row2hap(row)

    #===========================================================================
    # EDGES QUERIES
    #===========================================================================

    def edges(self):
        """Iterates over all :py:class:`yatel.dom.Edge` instances stored in 
        the database.

        **REQUIRE MODE:** r

        Returns
        -------
        iterator
            Iterator of :py:class:`yatel.dom.Edge` instances.

        """
        query = sql.select([self.edges_table])
        for row in self.execute(query):
            yield self._row2edge(row)

    def edges_by_environment(self, env=None, **kwargs):
        """Iterates over all :py:class:`yatel.dom.Edge` instances of a given 
        environment please see `yatel.db.YatelNetwork.haplotypes_enviroment` for more
        documentation about environment.

        **REQUIRE MODE:** r

        Parameters
        ----------
        env : dict
            Keys are :py:class:`yatel.dom.Fact` attributes name, and value is 
            a possible value of the given attribute.
        kwargs : dict
            Keys are :py:class:`yatel.dom.Fact` attributes name, and value is 
            a possible value of the given attribte.

        Returns
        -------
        iterator
            Iterator of :py:class:`yatel.dom.Edge`.

        """
        env = dict(env) if env else {}
        env.update(kwargs)

        subquery = sql.select([self.facts_table.c.hap_id]).where(
            sql.and_(
                *[self.facts_table.c[k] == v for k, v in env.items()]
            )
        ).distinct()
        query = sql.select([self.edges_table]).distinct()
        for cnt in range(self.describe().edge_attributes["max_nodes"]):
            alias = subquery.alias("sub_{}".format(cnt))
            attr = "hap_{}".format(cnt)
            query = query.select_from(alias).where(
                self.edges_table.c[attr] == alias.c.hap_id
            )
        for row in self.execute(query):
            yield self._row2edge(row)

    def edges_by_haplotype(self, hap):
        """Iterates over all the edges of a given 
        :py:class:`yatel.dom.Haplotype`.

        **REQUIRE MODE:** r

        Parameters
        ----------
        hap : :py:class:`yatel.dom.Haplotype`
            Haplotype to search with.

        Returns
        -------
        iterator
            Iterator of :py:class:`yatel.dom.Edge`.


        """
        where = sql.or_(*[v == hap.hap_id
                          for k, v in self.edges_table.c.items()
                          if k.startswith("hap_")])
        query = sql.select([self.edges_table]).where(where).distinct()
        for row in self.execute(query):
            yield self._row2edge(row)

    #===========================================================================
    # FACTS QUERIES
    #===========================================================================

    def facts(self):
        """Iterates over all :py:class:`yatel.dom.Fact` instances stored in 
        the database.
        
        """
        query = sql.select([self.facts_table])
        for row in self.execute(query):
            yield self._row2fact(row)

    def facts_by_haplotype(self, hap):
        """Return a iterator of all facts of a given 
        :py:class:`yatel.dom.Haplotype`.

        Parameters
        ----------
        hap : :py:class:`yatel.dom.Haplotype`
            Haplotype to search with.

        Returns
        -------
        iterator
            Iterator of :py:class:`yatel.dom.Fact`.

        """
        query = sql.select([self.facts_table]).where(
            self.facts_table.c.hap_id == hap.hap_id
        ).distinct()
        for row in self.execute(query):
            yield self._row2fact(row)

    def facts_by_environment(self, env=None, **kwargs):
        """Iterates over all :py:class:`yatel.dom.Fact` instances of a given 
        environment please see `yatel.db.YatelNetwork.haplotypes_environment` 
        for more documentation about environment.

        **REQUIRE MODE:** r

        Parameters
        ----------
        env : dict
            Keys are :py:class:`yatel.dom.Fact` attributes name, and value is 
            a possible value of the given attribute.
        kwargs : dict of keywords arguments
            Keys are :py:class:`yatel.dom.Fact` attributes name, and value is 
            a possible value of the given attribute.

        Returns
        -------
        iterator
            Iteratorterator of :py:class:`yatel.dom.Fact`.

        """
        env = dict(env) if env else {}
        env.update(kwargs)
        where = sql.and_(*[self.facts_table.c[k] == v
                           for k, v in env.items()])
        query = sql.select([self.facts_table]).where(where).distinct()
        for row in self.execute(query):
            yield self._row2fact(row)

    #===========================================================================
    # DESCRIPTOR
    #===========================================================================

    def describe(self):
        """Returns a :py:class:`yatel.dom.Descriptor` object with all the 
        information about the network.

        The descriptor object is a dictionary like with keys:

        edges_attributes : dict
            Dictionary contains always 2 keys : ``max_nodes`` How many nodes
            connect the edge with maximun number of connections. And ``weight``
            the time of weight attribute
        fact_attributes : dict
            Contains an arbitrary number of keys, with keys as attributes
            name, and value as attribute type.
        haplotype_atributes : dict
            Contains an arbitrary number of keys, with keys as attributes
            name, and value as attribute type.
        mode : str
            Actual mode of the network
        size : dict
            Has the number of elements in the network discrimined by type
            haplotypes, facts and edges.

        Examples
        --------

        >>> nw = db.YatelNetwork(...)
        >>> nw.describe()
        ... {
        ...     u'edge_attributes': {
        ...         u'max_nodes': 2,
        ...         u'weight': <type 'float'>
        ...     },
        ...     u'fact_attributes': {
        ...         u'align': <type 'int'>,
        ...         u'category': <type 'str'>,
        ...         u'coso': <type 'str'>,
        ...         u'hap_id': <type 'int'>,
        ...     }
        ...     u'haplotype_attributes': {
        ...         u'color': <type 'str'>,
        ...         u'description': <type 'str'>,
        ...         u'hap_id': <type 'int'>,
        ...     }
        ...     u'mode': 'r',
        ...     u'size': {u'edges': 10, u'facts': 20, u'haplotypes': 5}
        ... }


        """
        if self._descriptor:
            return self._descriptor

        descriptor_data = {}

        def hap_attributes():
            types = {}
            for att_name, column in self.haplotypes_table.c.items():
                pptype = None
                for satype in type(column.type).__mro__:
                    if satype in PYTHON_TYPES:
                        pptype = PYTHON_TYPES[satype](satype)
                        break
                if pptype:
                    types[att_name] = pptype
                else:
                    msg = "{} Column type '{}' unsuported".format(
                        att_name, str(column.type)
                    )
                    raise YatelNetworkError(msg)
            return types

        def fact_attributes():
            types = {}
            for att_name, column in self.facts_table.c.items():
                if att_name == "id":
                    continue
                pptype = None
                for satype in type(column.type).__mro__:
                    if satype in PYTHON_TYPES:
                        pptype = PYTHON_TYPES[satype](satype)
                        break
                if pptype:
                    types[att_name] = pptype
                else:
                    msg = "{} Column type '{}' unsuported".format(
                        att_name, str(column.type)
                    )
                    raise YatelNetworkError(msg)
            return types

        def edge_attributes():
            max_nodes = len(self.edges_table.c) - 2
            return {u"weight": float, u"max_nodes": max_nodes}

        def sizes():
            hapn = self.execute(
                sql.select([self.haplotypes_table]).alias("hapn").count()
            ).scalar()

            factn = self.execute(
                sql.select([self.facts_table]).alias("factn").count()
            ).scalar()

            edgen = self.execute(
                sql.select([self.edges_table]).alias("edgen").count()
            ).scalar()
            return  {u"haplotypes": hapn, u"facts": factn, u"edges": edgen}

        descriptor_data[u"mode"] = self.mode
        descriptor_data[u"haplotype_attributes"] = hap_attributes()
        descriptor_data[u"fact_attributes"] = fact_attributes()
        descriptor_data[u"edge_attributes"] = edge_attributes()
        descriptor_data[u"size"] = sizes()

        self._descriptor = dom.Descriptor(**descriptor_data)
        return self._descriptor

    #===========================================================================
    # PROPERTIES
    #===========================================================================

    @property
    def mode(self):
        """Returns mode of the database."""
        return self._mode

    @property
    def uri(self):
        """Returns uri of the database."""
        return self._uri


#===============================================================================
# FUNCTIONS
#===============================================================================

def qfilter(query, flt):
    """Filters a Yatel query by a given filter.

    Parameters
    ----------
    query : iterator of Yatel DOM
        Data to apply filter on.
    flt : Lambda expression
        Filter expression.

    """
    for elem in query:
        if flt(elem):
            yield elem


def parse_uri(uri, mode=MODE_READ, log=None):
    """Creates a dictionary to use in creation of a YatelNetwork.

    ::

        parsed = db.parse_uri("mysql://tito:pass@localhost:2525/mydb",
                               mode=db.MODE_READ, log=None)
        nw = db.YatelNetwork(**parsed)

    is equivalent to

    ::
        nw = db.YatelNetwork("mysql", database="mydb", user="tito",
                             password="pass", host="localhost", port=2525,
                             mode=db.MODE_READ, log=None)

    """
    urlo = url.make_url(uri)
    return {"mode": mode, "log": log,
            "engine": urlo.drivername, "database": urlo.database,
            "user": urlo.username, "password": urlo.password,
            "host": urlo.host, "port": urlo.port}


def to_uri(engine, **kwargs):
    """Create a correct uri for a given engine ignoring all unused parameters.

    Parameters
    ----------
    engine: str
        The engine name.
    kwargs : dict
         Variables for the engine.

    Examples
    --------
    >>> from yatel import db
    >>> db.to_uri("sqlite", database="nw.db")
    'sqlite:///nw.db'
    >>> db.to_uri("mysql", database="nw", host="localhost", port=3306,
    ···           user="root", password="secret")
    'mysql://root:secret@localhost:3306/nw'

    """
    tpl = string.Template(ENGINE_URIS[engine])
    engine_vars = ENGINE_VARS[engine]
    kwargs = dict((k, v) for k, v in kwargs.items() if k in engine_vars)
    return tpl.substitute(kwargs)


def exists(engine, **kwargs):
    """Returns ``True`` if exists a :py:class:`yatel.db.YatelNetwork` database 
    in that connection.

    Parameters
    ----------
    engine : str
        A value of the current engine used (see valid 
        :py:data:`yatel.db.ENGINES`)
    kwargs : a dict of variables for the engine.

    Returns
    -------
    existsdb : bool
        This function return ``False`` if:
            - The database does not exists.
            - The hap_id column has diferent types in ``haplotypes``, ``facts``
              or ``edges`` tables.
            - The ``edges`` table hasn't a column ``weight`` with type float.

    Examples
    --------
    >>> from yatel import db, dom
    >>> db.exists("sqlite", mode="r", database="nw.db")
    False
    >>> from_nw = db.YatelNetwork("memory", mode=db.MODE_WRITE)
    >>> from_nw.add_elements([dom.Haplotype("hap1"),
    ···                       dom.Haplotype("hap2"),
    ···                       dom.Fact("hap1", a=1, c="foo"),
    ···                       dom.Fact("hap2", a=1, b=2),
    ···                       dom.Edge(1, ("hap1", "hap2"))])
    >>> from_nw.confirm_changes()
    >>> db.exists("sqlite", mode="r", database="nw.db")
    True

    """
    kwargs.pop("mode", None)
    try:
        nw = YatelNetwork(engine, mode=MODE_READ, **kwargs)
        desc = nw.describe()
        hap_types = desc["haplotype_attributes"]
        fact_types = desc["fact_attributes"]
        edges_types = desc["edge_attributes"]
        if hap_types["hap_id"] != fact_types["hap_id"]:
            raise Exception()
    except Exception as err:
        return False
    else:
        return True


def copy(from_nw, to_nw):
    """Copy all the network in ``from_nw`` to the network ``to_nw``.

    ``from_nw`` must be in  read-only mode and ``to_nw`` in write or append 
    mode. Is your responsability to call ``to_nw.confirm_changes()`` after 
    the copy.

    Parameters
    ----------
    from_nw : :py:class:`yatel.db.YatelNetwork`
        Network in **r** mode.
    to_nw : :py:class:`yatel.db.YatelNetwork`
        Network in **w** or **a** mode.

    Examples
    --------
    >>> from yatel import db, dom
    >>> from_nw = db.YatelNetwork("memory", mode=db.MODE_WRITE)
    >>> from_nw.add_elements([dom.Haplotype("hap1"),
    ···                       dom.Haplotype("hap2"),
    ···                       dom.Fact("hap1", a=1, c="foo"),
    ···                       dom.Fact("hap2", a=1, b=2),
    ···                       dom.Edge(1, ("hap1", "hap2"))])
    >>> from_nw.confirm_changes()
    >>> to_nw = db.YatelNetwork("sqlite", mode=db.MODE_WRITE, database="nw.db")
    >>> db.copy(from_nw, to_nw)
    >>> to_nw.confirm_changes()
    >>> list(from_nw.haplotypes()) == list(to_nw.haplotypes())
    True

    """
    to_nw.add_elements(from_nw.haplotypes())
    to_nw.add_elements(from_nw.facts())
    to_nw.add_elements(from_nw.edges())


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    print(__doc__)
