# -*- coding: utf-8 -*-

"""
Generation des diagrammes
"""

import logging
from datetime import date
from time import mktime
import os.path as osp

from simplejson import dumps

from pycompta import Date, RelativeDateTime, absjoin

def mk_courbes(compta, dates):
    """
    retourne courbes à tracer
    """
    # prépare données
    courbe_resultat = []
    courbe_produits = []
    courbe_charges = []
    courbe_immo = []
    courbe_tres = []
    courbes = [ courbe_resultat, courbe_produits, courbe_charges,
                courbe_immo, courbe_tres]
    # construit courbes
    for etat in [compta.get_etat(date) for date in dates]:
        charges, produits = etat['resultat']
        courbe_resultat.append( (produits-charges)/100 )
        courbe_produits.append(etat['produits']/100)
        courbe_charges.append(etat['charges']/100)
        courbe_immo.append( etat['immobilisations']/100 )
        #courbe_tres.append( etat['tresorerie']/100 )

    return courbes

def mk_courbes_tres(compta, ldates):
    """
    retourne courbes à tracer
    """
    # prépare données
    dates = []
    courbe = []
    debut = ldates[0]
    fin = ldates[-1]+RelativeDateTime(day=-1)
    historique = compta.glivre.get_historique_comptes(debut, fin, '5')
    if historique:
        idate = historique[0][0]
        for date, debit, credit, solde, ecr in historique:
            if date != idate :
                dates.append( idate )
                courbe.append( -solde/100 )
                idate = date
    else:
        logging.warning("warning: no historique available")
    return dates, courbe

def _format(money, pos=None):
    digits = list('%.0f' % money)
    digits.reverse()
    i = 3
    while i < len(digits):
        digits.insert(i, ' ')
        i += 4
    digits.reverse()
    return ''.join(digits)


def _flot_dump_timeplot(plot):
    plot = [(datetime2ticks(x), y, datetime2ticks(x), "%Y-%m-%d")
            for x,y in plot]
    return dumps(plot)

def datetime2ticks(date):
    return mktime(date.timetuple()) * 1000

FLOT_HTML_BASE = """<html>
  <head>
    <script type="text/javascript" src="%(baseurl)s/jquery.js"/></script>
    <script type="text/javascript" src="%(baseurl)s/jquery.flot.js"></script>
    <script language="javascript">
%(pycomptajs)s
function onload() {
    %(plotdefs)s
    jQuery.plot(jQuery("#comptaplot"), [%(plotdata)s],
        {points: {show: true},
         lines: {show: true},
         grid: {hoverable: true},
         xaxis: {mode: %(mode)s}});
    jQuery("#comptaplot").bind("plothover", onPlotHover);
}

jQuery(document).ready(onload);
    </script>
  </head>
  <body>
    <div id="comptaplot" style="width: 500px; height: 400px;"></div>
  </body>
</html>
"""
# FIXME make the width/height configurable via css

JSDIR = absjoin(osp.dirname(__file__), '../js')
if not osp.exists(JSDIR):
    JSDIR = '/usr/share/pycompta/js'

def diagram_flot(filename, compta, dates,
                 baseurl='http://intranet.logilab.fr/crm/data'):
    """
    courbes des charges, produits, immobilisations et résultat.

    utilise jquery/flot pour dessiner les courbes
    """
    labels = ['resultat', 'produits', 'charges', 'immob.']
    plotdefs = []
    plotdata = []
    colors = ('red','green','blue','yellow')
    for idx, (label, ydata, color) in enumerate(zip(labels, mk_courbes(compta, dates), colors)):
        plotid = 'comptaplot_%s' % idx
        plot = zip(dates, ydata)
        plotdefs.append('var %s = %s;' % (plotid, _flot_dump_timeplot(plot)))
        plotdata.append("{label: '%s', color: '%s', data: %s}" % (label, color, plotid))
    jslib = file(osp.join(JSDIR,'pycompta.js')).read()
    file(filename, 'w').write(FLOT_HTML_BASE %
                              {'plotdefs': '\n'.join(plotdefs),
                               'plotdata': ','.join(plotdata),
                               'mode': "'time'",
                               'pycomptajs': jslib,
                               'baseurl': baseurl})

def diagram_tres_flot(filename, compta, dates,
                      baseurl='http://intranet.logilab.fr/crm/data'):
    """
    courbes des charges, produits, immobilisations et résultat.
    """
    label = 'tresorerie'
    dates, courbe = mk_courbes_tres(compta, dates)
    color = 'red'
    plotid = 'comptaplot_tres'
    plot = zip(dates, courbe)
    plotdefs = 'var %s = %s;' % (plotid, _flot_dump_timeplot(plot))
    plotdata = "{label: '%s', color: '%s', data: %s}" % (label, color, plotid)
    jslib = file(osp.join(JSDIR,'pycompta.js')).read()
    file(filename, 'w').write(FLOT_HTML_BASE %
                              {'plotdefs': plotdefs,
                               'plotdata': plotdata,
                               'mode': "'time'",
                               'pycomptajs': jslib,
                               'baseurl': baseurl})

def diagram_matplot(filename, compta, dates) :
    """
    courbes des charges, produits, immobilisations et résultat.
    """
    from matplotlib import rcParams
    rcParams['xtick.labelsize'] = 10
    rcParams['ytick.labelsize'] = 10
    rcParams['legend.fontsize'] = 8
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.dates import DateFormatter, DayLocator
    from matplotlib.ticker import FuncFormatter

    fig = Figure(figsize=(12,6))
    ax = fig.add_subplot(111)

    ax.set_ylabel("Euros")

    xdates = [date(d.year,d.month,d.day).toordinal() for d in dates]
    labels = ['resultat',
              'produits',
              'charges',
              'immob.',
              ]
    styles = ('r-', 'g-', 'b-', 'y-',)
    for courbe, style, label  in zip(mk_courbes(compta, dates), styles, labels):
        ax.plot(xdates, courbe, style, label=label)
    ax.set_xlim(xmin=min(xdates)-1, xmax=max(xdates)+1)

    locator = DayLocator((1,))
    formatter = DateFormatter('%y-%m')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(FuncFormatter(_format))

    ax.legend(loc='upper left')
    ax.yaxis.grid(True)
    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(filename, dpi=100)


def diagram_tres_matplot(filename, compta, dates):
    """
    courbes des charges, produits, immobilisations et résultat.
    """
    from matplotlib import rcParams
    rcParams['xtick.labelsize'] = 10
    rcParams['ytick.labelsize'] = 10
    from matplotlib.figure import Figure
    from matplotlib.backends.backend_agg import FigureCanvasAgg
    from matplotlib.dates import DateFormatter, WeekdayLocator, MO, DayLocator
    from matplotlib.ticker import FuncFormatter

    dates, courbe = mk_courbes_tres(compta, dates)

    fig = Figure(figsize=(30,6))
    ax = fig.add_subplot(111)

    ax.set_ylabel("Euros")
    if dates:
        xdates = [date(d.year,d.month,d.day).toordinal() for d in dates]
        ax.plot(xdates, courbe, 'r-', label="tresorerie")
        ax.set_xlim(xmin=min(xdates)-1, xmax=max(xdates)+1)
    locator = WeekdayLocator((MO,))
    formatter = DateFormatter('%d/%m')
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_minor_locator(DayLocator())
    ax.xaxis.set_major_formatter(formatter)
    ax.yaxis.set_major_formatter(FuncFormatter(_format))
    ax.yaxis.grid(True)
    canvas = FigureCanvasAgg(fig)
    canvas.print_figure(filename, dpi=75)


diagram = diagram_matplot
diagram_tres = diagram_tres_matplot
