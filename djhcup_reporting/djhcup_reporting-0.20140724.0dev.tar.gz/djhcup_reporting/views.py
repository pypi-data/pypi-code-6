# core Python packages
import logging
import json


# third party packages


# django packages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.utils.timezone import utc


# local imports
from djhcup_reporting.models import ReportingTable, LookupTable, Universe, FILTER_OPERATOR_CHOICES, Query, DataSet
from djhcup_reporting.utils.reporting import filterbundle_from_json

# start a logger
logger = logging.getLogger('default')


"""
Create your views here.
"""
def index(request):
    logger.debug('Reporting index requested')
    
    context = {
        'title': 'The Django-HCUP Hachoir: Reporting Index',
    }
    
    template = 'djhcup_base.html'
    return render(request, template, context)


def query_builder(request):

    if 'universe_pk' in request.GET:
        #print request.GET
        u_pk = request.GET['universe_pk']
        #print u_pk
        #print request.GET['universe_pk'][0]
        if 'filter_json' in request.POST:
            return query_builder_save(request, u_pk)
        else:
            return query_builder_filters(request, u_pk)
    
    logger.debug('New query builder page requested')
    
    universes = Universe.objects.all()
    
    context = {
        'title': 'Query Builder: Choose Reporting Universe',
        'universes': universes,
    }
    
    template = 'rpt_new.html'
    return render(request, template, context)


def query_builder_filters(request, universe_pk):
    logger.debug('Query builder filter page requested')
    
    try:
        u = Universe.objects.get(pk=universe_pk)
    except ObjectDoesNotExist:
        raise # eventually, return a 404
    
    fields = u.filters_for_display()
    
    operators = [{"display": f[1], "value": f[0]} for f in FILTER_OPERATOR_CHOICES]
    
    context = {
        'title': 'Query Builder: Choose Filters',
        'json_fields': json.dumps(fields),
        'json_operators': json.dumps(operators),
        'universe': u
    }
    
    template = 'rpt_new_choose_filters.html'
    return render(request, template, context)


def query_builder_save(request, universe_pk):
    """Saves objects associated with the query builder process,
    and then opens them for further editing (assign a name, etc).
    """
    
    logger.debug('Query builder save view requested')
    
    try:
        u = Universe.objects.get(pk=universe_pk)
        #print u
    except:
        # return render(no universe error)
        pass
    
    try:
        fg = filterbundle_from_json(request.POST['filter_json'])
    except:
        # return render(unable to process filter bundle error)
        # ask people to use their back button to make changes
        pass
    
    q = Query(filtergroup=fg, universe=u)
    q.save()
    
    d = DataSet(query=q)
    # TODO: tack on an owner from current user here as well
    d.gen_dbo(overwrite=True)
    d.save()
    #print d
    #print d.pk
    pass_through_messages = [
        dict(level="info", content="Your query has been saved."),
        dict(level="info", content="You may wish to enter a name for .")
    ]

    # TODO: submit the dataset for processing
    
    return dataset_details(request, d.dbo_name)

# TODO: a view showing details of a query to admins and its owner(s)
# TODO: a view showing requested queries w/their completion states
def dataset_details(request, dataset_dbo_name):
    #print "d_pk is %s" % d_pk
    try:
        d = DataSet.objects.get(dbo_name=dataset_dbo_name)
        #print d
    except ObjectDoesNotExist:
        raise #404

    context = {
        'title': 'DataSet #{pk} Details'.format(pk=d.pk),
        'universe': d.query.universe,
        'query': d.query,
        'dataset': d
    }
    template = 'rpt_dataset_details.html'
    return render(request, template, context)
