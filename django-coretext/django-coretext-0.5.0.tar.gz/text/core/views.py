from django.core.management import setup_environ
from django.conf import settings
from models import *
from django.shortcuts import get_object_or_404, render_to_response
from django.http import Http404, HttpResponse
import datetime
from django.template import RequestContext

def index(request, chapter_slug='home', page_slug=''): 
    """Returns requested chapter and page"""
    today = datetime.datetime.today() # Get today's date
    def slug(obj): return obj.filter(number=0) if page_slug == '' else obj.filter(slug=page_slug,publish_date__lte=today).order_by('number')
    print page_slug
    try:
        chapter = Chapter.objects.get(slug=chapter_slug, pages__slug=page_slug)
        return render_to_response('%s.html' % chapter.kind, {'user': request.user, 'chapter': chapter, }, context_instance=RequestContext(request))
    except Chapter.DoesNotExist:
        raise Http404

def menu(request, chapter_slug ): return HttpResponse(chapter_slug)

def page(request, page_slug, page_id):
    today = datetime.datetime.today() # Get today's date
    try:
        page = Page.objects.get(id=page_id,publish_date__lte=today)
        return render_to_response('%s.html' % page.kind, {'user': request.user, 'page': page, }, context_instance=RequestContext(request))
    except Page.DoesNotExist:
        raise Http404