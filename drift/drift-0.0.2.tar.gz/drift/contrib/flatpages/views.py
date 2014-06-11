from django.shortcuts import render, get_object_or_404, redirect
from django.conf import settings
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.utils.safestring import mark_safe
from django.template import loader
from django.views.decorators.csrf import csrf_protect

from .models import Flatpage
from drift.content import make_content


def resolve(url):
    if not url.startswith('/'):
        url = '/' + url
    try:
        f = get_object_or_404(
            Flatpage,
            url__exact=url
        )
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'
            f = get_object_or_404(
                Flatpage,
                url__exact=url,
            )
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise

    return f


def flatpage(request, url, template='flatpages/default.html'):
    """
    Public interface to the flat page view.

    Models: `flatpages.flatpages`
    Templates: Uses the template defined by the ``template_name`` field,
        or :template:`flatpages/default.html` if template_name is not defined.
    Context:
        flatpage
            `flatpages.flatpages` object
    """

    f = resolve(url)
    if isinstance(f, HttpResponsePermanentRedirect):
        return f

    return render_flatpage(request, f, template)


@csrf_protect
def render_flatpage(request, f, template):
    """
    Internal interface to the flat page view.
    """
    if f.template_name:
        t = loader.select_template((f.template_name, template))
    else:
        t = loader.get_template(template)

    # To avoid having to always use the "|safe" filter in flatpage templates,
    # mark the title and content as already safe (since they are raw HTML
    # content in the first place).
    f.title = mark_safe(f.title)
    f.content = mark_safe(f.content)

    content = make_content(f)

    return render(
        request,
        template,
        dict(
            content=content,
            flatpage=f,
        )
    )


def edit(request, url=None, template="flatpages/default_edit.html"):
    if url is not None:
        f = resolve(url)
        if isinstance(f, HttpResponsePermanentRedirect):
            return f
        create = False
    else:
        f = Flatpage()
        create = True

    content = make_content(f, request, 'create' if create else 'edit')


    if request.method == "POST":
        form = content.get_form(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            f.save()
            return redirect('flatpage', f.url)



    return render(
        request,
        template,
        dict(
            edit=True,
            content=content,
            flatpage=f,
        ),
    )
