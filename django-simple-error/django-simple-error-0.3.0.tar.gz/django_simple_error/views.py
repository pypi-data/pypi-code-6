from django.shortcuts import render
from django.conf import settings

try:
    error_page_css = settings.DJANGO_SIMPLE_ERROR_CSS
except AttributeError:
    error_page_css = 'index.css'

try:
    five_hundo_template = settings.DJANGO_SIMPLE_ERROR_500
except AttributeError:
    five_hundo_template = '500.html'

try:
    four_hundo_four_template = settings.DJANGO_SIMPLE_ERROR_404
except AttributeError:
    four_hundo_four_template = '404.html'

try:
    four_hundo_three_template = settings.DJANGO_SIMPLE_ERROR_403
except AttributeError:
    four_hundo_three_template = '403.html'

try:
    four_hundo_template = settings.DJANGO_SIMPLE_ERROR_400
except AttributeError:
    four_hundo_template = '400.html'

context = {'css': error_page_css}

def project_error(request):
    return render(request, five_hundo_template, context)

def page_not_found(request):
    return render(request, four_hundo_four_template, context)

def permission_denied(request):
    return render(request, four_hundo_three_template, context)

def bad_request(request):
    return render(request, four_hundo_template, context)
