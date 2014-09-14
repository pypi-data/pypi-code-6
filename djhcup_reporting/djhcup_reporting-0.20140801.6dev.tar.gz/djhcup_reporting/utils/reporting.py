import json
import logging
import string
from random import choice


# django imports
from django.core.exceptions import ObjectDoesNotExist


# sister app imports
from djhcup_integration.models import Column as IntegrationColumn, Edition as IntegrationEdition
from djhcup_reporting.models import Filter, FilterGroup, Universe, Column as ReportingColumn, DataSet


# start a logger
logger = logging.getLogger('default')

def filterbundle_from_json(filter_json):
    """
    Creates a bundle of filters based on the JSON content in
    filter_json. Expects the JSON string to be structured
    according to form in rpt_new_choose_filters template.
    
    Returns the top-level FilterGroup object.
    
    Example:
    filter_json has key filtergroup
        filtergoup has keys any, filters, and subfiltergroups
            all is boolean ("true" implies filters should be
                joined with AND)
            filters is a list
                each member has keys field, operator, and values
            subfiltergroups is a list, with zero or more
                filtergroups structured exactly like this one
    
    Due to the parent-child structure possible here, some
    recursion is required.
    
    However!
    
    Sub filters are not implemented at the html input level,
    so they may be (but aren't) omitted as of 2014-07-16.
    """
    try:
        filter_dict = json.loads(filter_json)
        #print filter_dict
    except:
        raise Exception("Unable to load JSON string from supplied filter_json")
    
    try:
        fg_entry = filter_dict['filtergroup']
    except:
        raise Exception("Unable to access value for key filtergroup in decoded JSON")

    fg = process_filtergroup(fg_entry)
    return fg


def process_filtergroup(fg_entry, parent=None):
    try:
        any_val = fg_entry['any']
    except:
        any_val = False
    
    try:
        fg_obj = FilterGroup(any=any_val, parent=parent)
        fg_obj.save()
    except:
        raise Exception("Unable to create FilterGroup object from " +\
            "{fg_entry}".format(fg_entry=fg_entry))
    
    for f_entry in fg_entry['filters']:
        try:
            col = ReportingColumn.objects.get(pk=f_entry['field'])
            op = f_entry['operator']
            val = f_entry['values']
            
            f = Filter(
                filtergroup=fg_obj,
                column=col,
                operator=op,
                value=val
            )
            # TODO: consider putting a check in here to see if valid
            # SQL can be generated from the constructed Filter object
            f.save()
        except:
            logger.error("Unable to create Filter object " +\
                "from {f_entry}".format(f_entry=f_entry))
    
    for sub_fg in fg_entry['subfiltergroups']:
        try:
            process_filtergroup(sub_fg, parent=fg_obj)
        except:
            logger.error("Unable to create sub FilterGroup from " +\
                "{sub_fg}".format(sub_fg=sub_fg))
    return fg_obj
