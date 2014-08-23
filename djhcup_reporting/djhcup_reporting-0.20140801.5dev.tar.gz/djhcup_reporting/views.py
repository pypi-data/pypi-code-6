# core Python packages
import os
import logging
import json
import zipfile
from io import StringIO


# third party packages


# django packages
from django.core.exceptions import ObjectDoesNotExist
from django.core.servers.basehttp import FileWrapper
from django.core.urlresolvers import reverse
from django.http import HttpResponse, StreamingHttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.timezone import utc
from django.contrib.auth.decorators import login_required


# local imports
from djhcup_reporting.models import ReportingTable, LookupTable, Universe, FILTER_OPERATOR_CHOICES, Query, DataSet, Column
from djhcup_reporting.utils.reporting import filterbundle_from_json
from djhcup_reporting.forms import PublicDataSetForm
from djhcup_reporting.tasks import process_dataset

# start a logger
logger = logging.getLogger('default')


"""
Create your views here.
"""
@login_required(login_url='/login/')
def index(request):
    logger.debug('Reporting index requested')
    
    context = {
        'title': 'The Django-HCUP Hachoir: Reporting Index'
    }
    
    template = 'djhcup_base.html'
    return render(request, template, context)


@login_required(login_url='/login/')
def query_builder(request):
    if 'universe_pk' in request.GET:
        u_pk = request.GET['universe_pk']
        
        if 'filter_json' in request.POST:
            return query_builder_save(request, u_pk)
        else:
            return query_builder_filters(request, u_pk)
    
    logger.debug('New query builder page requested')
    
    universes = Universe.objects.all()
    
    if len(universes) == 1:
        # there is only one Universe.
        # go ahead and get started with it.
        u = universes[0]
        return query_builder_filters(request, u.pk)
    
    context = {
        'title': 'Query Builder: Choose Reporting Universe',
        'universes': universes
    }
    
    template = 'rpt_new.html'
    return render(request, template, context)


@login_required(login_url='/login/')
def query_builder_filters(request, universe_pk):
    logger.debug('Query builder filter page requested')
    
    try:
        u = Universe.objects.get(pk=universe_pk)
    except ObjectDoesNotExist:
        raise # eventually, return a 404
    
    filter_fields = u.filters_for_display()
    filter_operators = [{"display": f[1], "value": f[0]} for f in FILTER_OPERATOR_CHOICES]
    try:
        available_columns = u.data.column_set.all().order_by('category', 'int_column__field_out', 'label')
    except:
        available_columns = None
    
    context = {
        'title': 'DataSet Builder',
        'json_filter_fields': json.dumps(filter_fields),
        'json_filter_operators': json.dumps(filter_operators),
        'universe': u,
        'form': PublicDataSetForm(),
        'available_columns': available_columns
    }
    
    template = 'rpt_builder.html'
    return render(request, template, context)


@login_required(login_url='/login/')
def query_builder_save(request, universe_pk):
    """Saves objects associated with the query builder process,
    and then opens them for further editing (assign a name, etc).
    """
    
    logger.debug('Query builder save view requested')
    
    #print request.POST
    
    try:
        u = Universe.objects.get(pk=universe_pk)
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
    
    # add all dem columns
    try:
        col_lst = request.POST.getlist('columns[]', [])
        for c_pk in col_lst:
            try:
                c = Column.objects.get(pk=int(c_pk))
                try:
                    q.columns.add(c)
                except:
                    logger.warning("Unable to add Column %s to Query.columns" % c)
            except:
                logger.warning("Unable to find Column with pk %s" % c_pk)
    except:
        logger.warning("Unable to pull column list from request.POST.getlist['columns'].")
    d = DataSet(query=q)
    try:
        form = PublicDataSetForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            d.name = cleaned['name']
            d.description = cleaned['description']
    except:
        logger.warning("Unable to make form using request.POST. Name and description will not be saved.")
    
    # check for pre- and post-visit requests
    d.bundle_previsit_file = request.POST.get('bundle_previsit_file', False)
    d.bundle_postvisit_file = request.POST.get('bundle_postvisit_file', False)
    
    #form = PublicDataSetForm(request.POST)
    
    # TODO: tack on an owner from current user here as well
    d.gen_dbo(overwrite=True)
    d.save()

    # call the extraction as an asynchronous task
    result = process_dataset.delay(d.pk)
    
    # meanwhile proceed to show the details page
    return HttpResponseRedirect(reverse('dataset_details', kwargs={'dataset_dbo_name': d.dbo_name}))


# TODO: limit to appropriate DataSet objects only
@login_required(login_url='/login/')
def datasets_browse(request):
    d_qs = DataSet.objects.all()

    context = {
        'title': 'My DataSets',
        'datasets': d_qs
    }
    template = 'rpt_datasets.html'
    return render(request, template, context)



# TODO: decorate with something that limits access based on associated database_dbo_name
@login_required(login_url='/login/')
def dataset_details(request, dataset_dbo_name):
    messages = []
    try:
        d = DataSet.objects.get(dbo_name=dataset_dbo_name)
        #print d
    except ObjectDoesNotExist:
        raise #404

    if request.POST:
        # form has been submitted
        # process and update as appropriate
        form = PublicDataSetForm(request.POST)
        if form.is_valid():
            cleaned = form.cleaned_data
            d.name = cleaned['name']
            d.description = cleaned['description']
            d.void = cleaned['void']
            d.save()
    
    if d.status == 'NEW':
        messages.append(dict(
            type="info",
            content="Your query has been placed in the queue. Once it has finished, you will be able to download the result from this page."))
    
    
    if not d.name or len(d.name) == 0:
        messages.append(dict(
            type='info',
            content='Your DataSet does not have a name. Please enter one below.'))
    
        
    context = {
        'title': 'DataSet #{pk} Details'.format(pk=d.pk),
        'universe': d.query.universe,
        'query': d.query,
        'dataset': d,
        'form': PublicDataSetForm(instance=d),
        'response_messages': messages
    }
    template = 'rpt_dataset_details.html'
    return render(request, template, context)


# TODO: decorate with something that limits access based on associated database_dbo_name
@login_required(login_url='/login/')
def universe_details(request, universe_pk):
    #print "d_pk is %s" % d_pk
    try:
        u = Universe.objects.get(pk=universe_pk)
        #print d
    except ObjectDoesNotExist:
        raise #404

    context = {
        'title': 'Universe #{pk} Details'.format(pk=u.pk),
        'universe': u
    }
    template = 'rpt_universe_details.html'
    return render(request, template, context)


# decorate with something that limits access based on associated database_dbo_name
@login_required(login_url='/login/')
def download_archive(request, dataset_dbo_name):
    """Returns a data stream for a zip archive associated
    with the requested dataset_dbo_name.
    """
    try:
        d = DataSet.objects.get(dbo_name=dataset_dbo_name)
    except ObjectDoesNotExist:
        raise #404 #though, to be honest, how did you get here without auth?
    
    print d.archive_path
    h = open(d.archive_path, 'r')
    wrapper = FileWrapper(h)
    response = StreamingHttpResponse(wrapper, content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(d.archive_path)
    
    return response

# TODO: a view showing requested queries w/their completion states