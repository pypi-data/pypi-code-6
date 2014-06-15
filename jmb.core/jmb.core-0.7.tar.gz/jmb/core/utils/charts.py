#! -*- coding: utf-8 -*-

highlights_chart =  """
        <script type="text/javascript">
            var chart;
            $(document).ready(function() {
                chart = new Highcharts.Chart({
                    %(chart_type)s%(properties)s%(series)s
                })
            });
        </script>
        <div id="%(render_to)s"></div>
        """

class Chart:
    def __init__(self, render_to, **kwargs):
        self.render_to = render_to

        extra_args = self.get_extra_args(**kwargs)
        self.chart_type = """credits: {enabled:false}, chart: {
                        renderTo: '%(render_to)s'%(extra_args)s
                    }""" % {'render_to':render_to,
                            'extra_args': extra_args}

        self.series = []
        self.properties = []


    def get_extra_args(self, add_first_comma=True, strip_list=False, **kwargs):
        extra_args = ''
        for i, ex_arg in enumerate(kwargs.keys()):
            comma = """,
                        """
            if i == 0 and not add_first_comma:
                comma = ""
            if type(kwargs[ex_arg]) == type(True) and kwargs[ex_arg] == True:
                extra_args += """%s%s : true""" % (comma, ex_arg)
            elif type(kwargs[ex_arg]) == type(False) and kwargs[ex_arg] == False:
                extra_args += """%s%s : false""" % (comma, ex_arg)
            elif type(kwargs[ex_arg]) == type(None):
                extra_args += """%s%s : null""" % (comma, ex_arg)
            elif type(kwargs[ex_arg]) == type(''):
                extra_args += """%s%s : '%s'""" % (comma, ex_arg, str(kwargs[ex_arg]))
            elif type(kwargs[ex_arg]) == type([]) and strip_list:
                extra_args += """%s%s : %s""" % (comma, ex_arg, str(kwargs[ex_arg]).replace("'", ""))
            else:
                extra_args += """%s%s : %s""" % (comma, ex_arg, kwargs[ex_arg])
        return extra_args


    def add_property(self, name, **kwargs):
        extra_args = self.get_extra_args(add_first_comma=False, **kwargs)
        property = """%s: {
                            %s
                    }""" % (name, extra_args)
        self.properties.append(property)


    def add_series(self, strip_list=False, **kwargs):
        extra_args = self.get_extra_args(add_first_comma=False, strip_list=strip_list, **kwargs)
        self.series.append(extra_args)

    def print_series(self):
        s = """,
                    series: [
                        %s
                    ]"""
        ss = ""
        for serie in self.series:
            ss += """{%s},
                        """ % serie
        return s % ss

    def print_properties(self):
        s = ''
        for p in self.properties:
            s += """,
                    %s""" % p
        return s

    def set_colors(self, colors=[]):
        if colors:
            property = """colors: %s""" % (colors,)
            self.properties.append(property)


    def __unicode__(self):
        return highlights_chart % {'render_to': self.render_to,
                                   'chart_type':self.chart_type,
                                   'properties': self.print_properties(),
                                   'series':self.print_series()
                                   }


class SubProperty(Chart):
    def __init__(self, **kwargs):
        extra_args = self.get_extra_args(add_first_comma=False, **kwargs)
        self.s = """{
                            %s
                        }""" % extra_args

    def __str__(self, **kwargs):
        return self.s

    def __unicode__(self, **kwargs):
        return self.s


class Property:
    def __init__(self, value):
        self.value = value

    def __str__(self, **kwargs):
        return self.value

    def __unicode__(self, **kwargs):
        return self.value
