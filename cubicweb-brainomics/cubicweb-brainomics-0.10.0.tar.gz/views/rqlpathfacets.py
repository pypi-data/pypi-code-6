"""
Backport from CW 3.19 (0509880fec01)
This should be removed once SuiviMP switch to 3.19 (currently 3.18)
"""

from rql import nodes
from cubicweb.web.facet import RQLPathFacet, DateRangeFacet, cleanup_select


class AbstractRangeRQLPathFacet(RQLPathFacet):
    """
    The :class:`AbstractRangeRQLPathFacet` is the base class for
    RQLPathFacet-type facets allowing the use of RangeWidgets-like
    widgets (such as (:class:`FacetRangeWidget`,
    class:`DateFacetRangeWidget`) on the parent :class:`RQLPathFacet`
    target attribute.
    """
    __abstract__ = True

    def vocabulary(self):
        """return vocabulary for this facet, eg a list of (label,
        value)"""
        select = self.select
        select.save_state()
        try:
            filtered_variable = self.filtered_variable
            cleanup_select(select, filtered_variable)
            varmap, restrvar = self.add_path_to_select()
            if self.label_variable:
                attrvar = varmap[self.label_variable]
            else:
                attrvar = restrvar
            # start RangeRQLPathFacet
            minf = nodes.Function('MIN')
            minf.append(nodes.VariableRef(restrvar))
            select.add_selected(minf)
            maxf = nodes.Function('MAX')
            maxf.append(nodes.VariableRef(restrvar))
            select.add_selected(maxf)
            # add is restriction if necessary
            if filtered_variable.stinfo['typerel'] is None:
                etypes = frozenset(sol[filtered_variable.name] for sol in select.solutions)
                select.add_type_restriction(filtered_variable, etypes)
            # end RangeRQLPathFacet
            try:
                rset = self.rqlexec(select.as_string(), self.cw_rset.args)
            except Exception:
                self.exception('error while getting vocabulary for %s, rql: %s',
                               self, select.as_string())
                return ()
        finally:
            select.recover()
        # don't call rset_vocabulary on empty result set, it may be an empty
        # *list* (see rqlexec implementation)
        if rset:
            minv, maxv = rset[0]
            return [(unicode(minv), minv), (unicode(maxv), maxv)]
        return []


    def possible_values(self):
        """return a list of possible values (as string since it's used to
        compare to a form value in javascript) for this facet
        """
        return [strval for strval, val in self.vocabulary()]

    def add_rql_restrictions(self):
        infvalue = self.infvalue()
        supvalue = self.supvalue()
        if infvalue is None or supvalue is None: # nothing sent
            return
        varmap, restrvar = self.add_path_to_select(
            skiplabel=True, skipattrfilter=True)
        restrel = None
        for part in self.path:
            if isinstance(part, basestring):
                part = part.split()
            subject, rtype, object = part
            if object == self.filter_variable:
                restrel = rtype
        assert restrel
        # when a value is equal to one of the limit, don't add the restriction,
        # else we filter out NULL values implicitly
        if infvalue != self.infvalue(min=True):

            self._add_restriction(infvalue, '>=', restrvar, restrel)
        if supvalue != self.supvalue(max=True):
            self._add_restriction(supvalue, '<=', restrvar, restrel)

    def _add_restriction(self, value, operator, restrvar, restrel):
        self.select.add_constant_restriction(restrvar,
                                             restrel,
                                             self.formatvalue(value),
                                             self.target_attr_type, operator)


class RangeRQLPathFacet(AbstractRangeRQLPathFacet, RQLPathFacet):
    """
    The :class:`RangeRQLPathFacet` uses the :class:`FacetRangeWidget`
    on the :class:`AbstractRangeRQLPathFacet` target attribute
    """
    pass


class DateRangeRQLPathFacet(AbstractRangeRQLPathFacet, DateRangeFacet):
    """
    The :class:`DateRangeRQLPathFacet` uses the
    :class:`DateFacetRangeWidget` on the
    :class:`AbstractRangeRQLPathFacet` target attribute
    """
    pass
