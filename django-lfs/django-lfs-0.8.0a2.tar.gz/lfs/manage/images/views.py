# python imports
import re
import urlparse

# django imports
from django.contrib.auth.decorators import permission_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext as _, ungettext

# lfs imports
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from lfs.catalog.models import Image
from lfs.catalog.settings import THUMBNAIL_SIZES
from lfs.core.utils import LazyEncoder, lfs_pagination

# Load logger
import logging
logger = logging.getLogger("default")

# views
@permission_required("core.manage_shop")
def images(request, template_name="manage/images/images.html"):
    """
    Display images management.
    """
    start = request.REQUEST.get('start')
    # Calculates parameters for display.
    try:
        start = int(start)
    except (ValueError, TypeError):
        start = 1

    # filter
    query = request.REQUEST.get('q', '')

    # prepare paginator
    if query:
        images_qs = Image.objects.filter(title__istartswith=query)
    else:
        images_qs = Image.objects.all()
    paginator = Paginator(images_qs, 50)

    try:
        current_page = paginator.page(start)
    except (EmptyPage, InvalidPage):
        current_page = paginator.page(paginator.num_pages)

    amount_of_images = images_qs.count()

    # Calculate urls
    pagination_data = lfs_pagination(request, current_page, url=request.path)

    pagination_data['total_text'] = ungettext('%(count)d image',
                                              '%(count)d images',
                                              amount_of_images) % {'count': amount_of_images}

    return render(request, template_name, {
        "images": current_page.object_list,
        "pagination": pagination_data,
        "query": query
    })


@permission_required("core.manage_shop")
@require_POST
def delete_images(request):
    """
    Deletes images which are passed via HTTP query.
    """
    Image.objects.filter(pk__in=request.POST.getlist("images")).delete()
    return HttpResponseRedirect(reverse("lfs_manage_global_images"))


@permission_required("core.manage_shop")
def add_images(request):
    """
    Adds a global images.
    """
    if request.method == "POST":
        for file_content in request.FILES.getlist("file"):
            image = Image(title=file_content.name)
            try:
                image.image.save(file_content.name, file_content, save=True)
            except Exception, e:
                image.delete()
                logger.info("Upload of image failed: %s %s" % (file_content.name, e))
                continue

    result = simplejson.dumps({"name": file_content.name, "type": "image/jpeg", "size": "123456789"})
    return HttpResponse(result, mimetype='application/json')


@permission_required("core.manage_shop")
def imagebrowser(request, template_name="manage/images/filebrowser_images.html"):
    """
    Displays a browser for images.
    """
    selected_size = None
    selected_image = None
    selected_class = request.GET.get("class")
    url = request.GET.get("url")
    start = request.GET.get('start', 1)

    if url:
        parsed_url = urlparse.urlparse(url)
        try:
            temp_url = "/".join(parsed_url.path.split("/")[2:])
            result = re.search("(.*)(\.)(\d+x\d+)(.*)", temp_url)
            if result:
                temp_url = result.groups()[0] + result.groups()[3]
                selected_image = Image.objects.get(image=temp_url)
                selected_size = result.groups()[2]
            else:
                value = None
                title = None
                selected_size = None

        except (IndexError, Image.DoesNotExist):
            pass

    sizes = []
    for size in THUMBNAIL_SIZES:
        size = "%sx%s" % (size[0], size[1])
        sizes.append({
            "value": size,
            "title": size,
            "selected": size == selected_size,
        })

    classes = [{"value": 'inline',
                "title": _(u'inline'),
                "selected": 'inline' == selected_class},
               {"value": 'left',
                "title": _(u'left'),
                "selected": 'left' == selected_class},
               {"value": 'right',
                "title": _(u'right'),
                "selected": 'right' == selected_class}]

    # Calculates parameters for display.
    try:
        start = int(start)
    except (ValueError, TypeError):
        start = 1

    # filter
    query = request.REQUEST.get('q', '')

    # prepare paginator
    if query:
        images_qs = Image.objects.filter(title__istartswith=query)
    else:
        images_qs = Image.objects.all()

    paginator = Paginator(images_qs, 25)

    try:
        current_page = paginator.page(start)
    except (EmptyPage, InvalidPage):
        current_page = paginator.page(paginator.num_pages)

    amount_of_images = images_qs.count()

    # Calculate urls
    pagination_data = lfs_pagination(request, current_page, url=request.path)

    pagination_data['total_text'] = ungettext('%(count)d image',
                                              '%(count)d images',
                                              amount_of_images) % {'count': amount_of_images}

    images = []
    for i, image in enumerate(current_page.object_list):
        images.append({
            "id": image.id,
            "title": image.title,
            "checked": image == selected_image,
            "url": image.image.url_100x100,
        })

    html = render_to_string(template_name, RequestContext(request, {
        "sizes": sizes,
        "classes": classes,
        "images": images,
        "query": query,
        "pagination": pagination_data
    }))

    result = simplejson.dumps({
        "html": html,
        "message": "msg",
    }, cls=LazyEncoder)

    return HttpResponse(result, mimetype='application/json')
