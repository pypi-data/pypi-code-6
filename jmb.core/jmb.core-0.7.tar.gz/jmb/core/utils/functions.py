import os
import re
import sys
import unicodedata
import unicodecsv as csv

from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode
from htmlentitydefs import name2codepoint

def render_csv(rows, filename=None):
    from django.http import HttpResponse
    response = HttpResponse(mimetype='text/csv')
    if not filename:
        filename = 'file.csv'
    response['Content-Disposition'] = 'attachment; filename= %s' % filename
    writer = csv.writer(response, delimiter=';',
                        quotechar='"', quoting=csv.QUOTE_ALL )
    writer.writerows(rows)
    return response

def render_xls(list_of_lists, filename=None, sheetname=None):
    """
    renderizza una l'input come documento MS Excel e lo restituisce come
    allegato di un oggetto HttpResponse
    :param list_of_lists: una lista di liste
    :param filename: (opzionale) nome file
    :param sheetname: (opzionale) nome foglio excel
    :return: oggetto HttpResponse
    """
    try:
        import cStringIO as StringIO
    except ImportError:
        import StringIO
    from django.http import HttpResponse
    import xlwt

    response = HttpResponse(mimetype='application/vnd.ms-excel')
    if not filename:
        filename = 'file.xls'
    if not sheetname:
        sheetname = _("Sheet 1")
    response['Content-Disposition'] = 'attachment; filename= %s' % filename

    workbook = xlwt.Workbook()             # initializing the workbook object
    sheet = workbook.add_sheet(sheetname)  # adding a worksheet to workbook

    for row_index, row_content in enumerate(list_of_lists):
        for column_index, cell_value in enumerate(row_content):
            sheet.write(row_index, column_index, cell_value)

    # scrivo temporaneamente il file in un buffer per il salvataggio
    buffer = StringIO.StringIO()
    workbook.save(buffer)

    response.write(buffer.getvalue())
    response['Content-Disposition'] = 'attachment; filename= %s' % filename
    return response

def zerofill(x, width=6):
    return "%0*d" % (width, x)

def get_formatted_time(ms, seconds=True):
    if not ms:
        return ''
    ftime= ""
    if seconds:
        ftime= "0s"
    s=ms/1000
    m,s=divmod(s,60)
    h,m=divmod(m,60)
    d,h=divmod(h,24)
    if seconds and s > 0:
        ftime = "%ss" % s
    if m > 0:
        ftime = "%sm %s" % (m, ftime)
    if h > 0:
        ftime = "%sh %s" % (h, ftime)
    if d > 0:
        ftime = "%sg %s" % (d, ftime)

    return ftime

def get_random_string(self, length=10):
    import random, string
    return ''.join(random.sample(string.digits+string.letters, length))

def get_settings(model, val):
    from django.conf import settings
    from django.db.models.loading import get_model, get_app
    from django.utils.importlib import import_module

    use_db_settings = getattr(settings, "USE_DB_SETTINGS", True)
    value_settings = None

    full_app_name = None
    app_label = None
    model_name = None

    m = model.split(".")
    try:
        full_app_name = '.'.join(m[0:-1])
        app_label = m[-2]
        model_name = m[-1]
    except:
        pass

    try:
        model = get_model(app_label, model_name)
    except:
        model = None

    value_settings = "$value_not_found$"
    # CERCO LA PROPRIETA' PRIMA NEL DB
    if use_db_settings:
        if model:
            try:
                dbsettings = model.objects.get(name=val)
                value_settings = get_correct_type_settings(dbsettings)
            except:
                value_settings = "$value_not_found$"

    # SE NON LA TROVO LA VADO A CERCARE NEI SETTINGS DELL'APPLICAZIONE
    # PRIMA CERCO SE IL FILE DEI SETTTINGS DELL'APPLICAZIONE ESISTE
    if full_app_name and value_settings == "$value_not_found$":
        try:
            app_settings = import_module('.settings', full_app_name)
            value_settings = getattr(app_settings, val, "$value_not_found$")
        except Exception, e:
            value_settings = "$value_not_found$"

    # SE NON LA TROVO LA VADO A CERCARE NEI SETTINGS GENERALI
    if value_settings == "$value_not_found$":
        value_settings = getattr(settings, val, "$value_not_found$")

    # SE NON LA TROVO NEANCHE QUA GENERO UN'ECCEZIONE
    if value_settings == "$value_not_found$":
        raise Exception("The properties %s does not exists." % val)

    return value_settings

def get_correct_type_settings(dbsettings):
    if dbsettings.type == "BOOLEAN":
        if dbsettings.value in ('1', 'True'):
            return True
        else:
            return False

    if dbsettings.type == "INTEGER":
        if dbsettings.value.isdigit():
            return int(dbsettings.value)
        else:
            return None

    if dbsettings.type == "LIST":
        v = dbsettings.value.split(',')
        return [ x.strip() for x in v ]

    if dbsettings.type == "STRING":
        return str(dbsettings.value)

def get_groups_w_perm(perm_app, perm_model, perm_name):
    ## restituisce i gruppi che hanno il permesso passato #
    from django.contrib.auth.models import User, Group, Permission
    from jmb.core.middleware.thread_local import get_current_user
    user = get_current_user()
    if user.is_staff:
        valid_groups = Group.objects.all()
    elif not user.is_active:
        valid_groups = Group.objects.none()
    else:
        valid_groups = Group.objects.filter(user__id = user.id).filter(permissions__codename = perm_name).filter(permissions__content_type__app_label = perm_app).filter(permissions__content_type__model = perm_model).distinct()
    return valid_groups

from django.conf import settings

def add_group_with_app_permissions(group_name, app_name):
    """ This function is useful to create and return a Group having all
    permissions relatives to an application when a post_syncdb is called  """

    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import Permission, Group

    cts = ContentType.objects.filter(app_label__exact = app_name)

    pms = Permission.objects.filter(content_type__in = cts)

    try: # group has already been created
        Group.objects.get(name = group_name)
    except:
        g = Group()
        g.name = group_name
        g.save()
        g.permissions = pms
        g.save()

# From http://www.djangosnippets.org/snippets/369/
def slugify(s, entities=True, decimal=True, hexadecimal=True,
   instance=None, slug_field='slug', filter_dict=None):
    s = smart_unicode(s)

    #character entity reference
    if entities:
        s = re.sub('&(%s);' % '|'.join(name2codepoint), lambda m: unichr(name2codepoint[m.group(1)]), s)

    #decimal character reference
    if decimal:
        try:
            s = re.sub('&#(\d+);', lambda m: unichr(int(m.group(1))), s)
        except:
            pass

    #hexadecimal character reference
    if hexadecimal:
        try:
            s = re.sub('&#x([\da-fA-F]+);', lambda m: unichr(int(m.group(1), 16)), s)
        except:
            pass

    #translate
    s = unicodedata.normalize('NFKD', s).encode('ascii', 'ignore')

    #replace unwanted characters
    s = re.sub(r'[^-a-z0-9]+', '-', s.lower())

    #remove redundant -
    s = re.sub('-{2,}', '-', s).strip('-')

    slug = s
    if instance:
        def get_query():
            query = instance.__class__.objects.filter(**{slug_field: slug})
            if filter_dict:
                query = query.filter(**filter_dict)
            if instance.pk:
                query = query.exclude(pk=instance.pk)
            return query
        counter = 1
        while get_query():
            slug = "%s-%s" % (s, counter)
            counter += 1
    return slug


def get_template_abspath(template):
    from django.template.loaders.app_directories import Loader
    from django.template import TemplateDoesNotExist

    for filepath in Loader().get_template_sources(template):
        if os.path.exists(filepath):
            return filepath
    raise TemplateDoesNotExist(template)

def clean_phone_number(number):
    return re.sub('\D', "", number)



def import_class(class_string):
    """Returns class object specified by a string.

    Args:
        class_string: The string representing a class.

    Raises:
        ValueError if module part of the class is not specified.
    """
    module_name, _, class_name = class_string.rpartition('.')
    if module_name == '':
        raise ValueError('Class name must contain module part.')
    return getattr(
        __import__(module_name, globals(), locals(), [class_name], -1),
        class_name)


def int_format(value, decimal_points=3, separator=u'.'):
    """
    return a string representing the value formatted with specified separator and
    every decimal points
    :param value: a string/float/integer representing value
    :param decimal_points: char interval on which separator has to be displayed
    :param separator: char to be used as separator
    :return: the string formatted
    """
    value = str(value)
    if len(value) <= decimal_points:
        return value
        # say here we have value = '12345' and the default params above
    parts = []
    while value:
        parts.append(value[-decimal_points:])
        value = value[:-decimal_points]
        # now we should have parts = ['345', '12']
    parts.reverse()
    # and the return value should be u'12.345'
    return separator.join(parts)
