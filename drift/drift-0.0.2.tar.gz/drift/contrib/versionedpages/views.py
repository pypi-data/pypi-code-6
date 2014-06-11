from django.shortcuts import render, get_object_or_404, redirect
from django.utils.safestring import mark_safe
from django.template import loader
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from drift.content import make_content

from .models import Page, Version


def page(request, url, version_id=None, template="versionedpages/default.html"):
    # do permissions checks if not published

    page = get_object_or_404(Page, url=url)

    if version_id is not None:
        version = get_object_or_404(Version, pk=version_id)
        # check to see if version goes with content
    else:
        if request.user.is_authenticated() and page.published_version is None:
            version = page.get_most_recent_version(request.user)
        else:
            version = page.published_version

    return render(
        request,
        page.template_name or template,
        dict(
            content=make_content(page),
            version=version,
        ),
    )


@login_required
def edit_page(request, url=None, template="versionedpages/edit.html"):
    if url is None:
        page = Page()
        create = True
    else:
        page = get_object_or_404(Page, url=url)
        create = False

    content = make_content(page, request, 'create' if create else 'edit')

    if request.method == "POST":
        form = content.get_form(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.save()
            html = request.POST.get('content')

            if request.POST.get('version_id', '') == '':
                version = page.edit(request.user)
            else:
                version = get_object_or_404(
                    Version,
                    pk=request.POST.get('version_id', ''),
                )
            edit_version = version    
            if html is not None:
                version.html = html
                version.save_version()
            return redirect('versioned_page_version', page.url, version.id)
        else:
            if page.pk is not None:
                edit_version = page.edit(request.user)
            else:
                edit_version = None
    else:
        if page.pk is not None:
            edit_version = page.edit(request.user)
        else:
            edit_version = None

    return render(
        request,
        template,
        dict(
            edit=True,
            content=content,
            version=edit_version,
        ),
    )


@require_POST
@login_required
def auto_save(request, url):
    page = get_object_or_404(Page, url=url)
    content = make_content(page, request, 'edit')
    edit_version = page.edit(request.user)
    edit_version.html = urlunquote(request.POST['content'])
    edit_version.save()
    return HttpResponse('OK')


@require_POST
@login_required
def publish(request, url):
    content = get_object_or_404(Page, url=url)
    version = get_object_or_404(Version, pk=request.POST.get('version_id'))
    version.publish()
    return redirect('versioned_page', content.url)

