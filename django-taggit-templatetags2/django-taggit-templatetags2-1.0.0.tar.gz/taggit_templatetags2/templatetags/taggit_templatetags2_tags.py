from django import template
from django.db.models import Count
from django.db.models.loading import get_model
from django.core.exceptions import FieldError

from classytags.core import Options
from classytags.arguments import Argument
from classytags.helpers import AsTag

from taggit_templatetags2 import settings

T_MAX = getattr(settings, 'TAGCLOUD_MAX', 6.0)
T_MIN = getattr(settings, 'TAGCLOUD_MIN', 1.0)

LIMIT = 10

register = template.Library()


def get_queryset(forvar, taggeditem_model, tag_model):
    through_opts = taggeditem_model._meta
    count_field = (
        "%s_%s_items" % (
            through_opts.app_label,
            through_opts.object_name)).lower()

    if forvar is None:
        # get all tags
        queryset = tag_model.objects.all()
    else:
        # extract app label and model name
        beginning, applabel, model = None, None, None
        try:
            beginning, applabel, model = forvar.rsplit('.', 2)
        except ValueError:
            try:
                applabel, model = forvar.rsplit('.', 1)
            except ValueError:
                applabel = forvar
        applabel = applabel.lower()

        # filter tagged items
        if model is None:
            # Get tags for a whole app
            queryset = taggeditem_model.objects.filter(
                content_type__app_label=applabel)
            tag_ids = queryset.values_list('tag_id', flat=True)
            queryset = tag_model.objects.filter(id__in=tag_ids)
        else:
            # Get tags for a model
            model = model.lower()
            if ":" in model:
                model, manager_attr = model.split(":", 1)
            else:
                manager_attr = "tags"
            model_class = get_model(applabel, model)
            manager = getattr(model_class, manager_attr)
            queryset = manager.all()
            through_opts = manager.through._meta
            count_field = ("%s_%s_items" % (through_opts.app_label,
                                            through_opts.object_name)).lower()

    if count_field is None:
        # Retain compatibility with older versions of Django taggit
        # a version check (for example taggit.VERSION <= (0,8,0)) does NOT
        # work because of the version (0,8,0) of the current dev version of
        # django-taggit
        try:
            return queryset.annotate(
                num_times=Count(settings.TAG_FIELD_RELATED_NAME))
        except FieldError:
            return queryset.annotate(
                num_times=Count('taggit_taggeditem_items'))
    else:
        return queryset.annotate(num_times=Count(count_field))


def get_weight_fun(t_min, t_max, f_min, f_max):
    def weight_fun(f_i, t_min=t_min, t_max=t_max, f_min=f_min, f_max=f_max):
        # Prevent a division by zero here, found to occur under some
        # pathological but nevertheless actually occurring circumstances.
        if f_max == f_min:
            mult_fac = 1.0
        else:
            mult_fac = float(t_max - t_min) / float(f_max - f_min)
        return t_max - (f_max - f_i) * mult_fac
    return weight_fun


class TaggitBaseTag(AsTag):

    options = Options(
        'as',
        Argument('varname', resolve=False, required=False),
        'for',
        Argument('forvar', required=False),
        'limit',
        Argument('limit', required=False, default=LIMIT),
    )


@register.tag
class GetTagList(TaggitBaseTag):
    name = 'get_taglist'

    def get_value(self, context, varname, forvar, limit=LIMIT):
        # TODO: remove default value for limit, report a bug in the application
        # django-classy-tags, the default value does not work
        queryset = get_queryset(
            forvar,
            settings.TAGGED_ITEM_MODEL,
            settings.TAG_MODEL)
        queryset = queryset.order_by('-num_times')
        context[varname] = queryset
        if limit:
            queryset = queryset[:limit]
        return ''


@register.tag
class GetTagCloud(TaggitBaseTag):
    name = 'get_tagcloud'

    def get_value(self, context, varname, forvar, limit=LIMIT):
        queryset = get_queryset(
            forvar,
            settings.TAGGED_ITEM_MODEL,
            settings.TAG_MODEL)
        num_times = queryset.values_list('num_times', flat=True)
        if(len(num_times) == 0):
            context[varname] = queryset
            return ''
        weight_fun = get_weight_fun(
            T_MIN, T_MAX, min(num_times), max(num_times))
        queryset = queryset.order_by('name')
        if limit:
            queryset = queryset[:limit]
        for tag in queryset:
            tag.weight = weight_fun(tag.num_times)
        context[varname] = queryset
        return ''


@register.inclusion_tag('taggit_templatetags2/tagcloud_include.html')
def include_tagcloud(forvar=None):
    return {'forvar': forvar}


@register.inclusion_tag('taggit_templatetags2/taglist_include.html')
def include_taglist(forvar=None):
    return {'forvar': forvar}
