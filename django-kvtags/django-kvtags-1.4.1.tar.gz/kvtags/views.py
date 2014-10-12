from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.contrib import messages
from kvtags.forms import ImportTagsForm
from kvtags.utils import import_tags_csv


def import_tags(request):
    """Provides graphical interface to utils.import_tags_csv"""
    if request.method == 'POST':
        form = ImportTagsForm(request.POST, request.FILES)
        if form.is_valid():
            import_tags_csv(request.FILES['file'])
            messages.success(request, _("Yahoo! The csv is loaded!"))
        else:
            messages.error(request, _("File is invalid!"))
        return HttpResponseRedirect(reverse('kvtags_import_tags'))
    else:
        form = ImportTagsForm()
    return render(request,  'import_tags.html', {'form': form})
