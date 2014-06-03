from django.shortcuts import render

from wagtail.wagtailadmin.userbar import EditPageItem, AddPageItem, ApproveModerationEditPageItem, RejectModerationEditPageItem
from wagtail.wagtailadmin import hooks
from wagtail.wagtailcore.models import Page, PageRevision

def for_frontend(request, page_id):
    items = [
        EditPageItem(Page.objects.get(id=page_id)),
        AddPageItem(Page.objects.get(id=page_id)),
    ]

    for fn in hooks.get_hooks('construct_wagtail_edit_bird'):
        fn(request, items)

    # Render the items
    rendered_items = [item.render(request) for item in items]

    # Remove any unrendered items
    rendered_items = [item for item in rendered_items if item]

    # Render the edit bird
    return render(request, 'wagtailadmin/userbar/base.html', {
        'items': rendered_items,
    })

def for_moderation(request, revision_id):
    items = [
        EditPageItem(PageRevision.objects.get(id=revision_id).page),
        AddPageItem(PageRevision.objects.get(id=revision_id).page),
        ApproveModerationEditPageItem(PageRevision.objects.get(id=revision_id)),
        RejectModerationEditPageItem(PageRevision.objects.get(id=revision_id)),
    ]

    for fn in hooks.get_hooks('construct_wagtail_edit_bird'):
        fn(request, items)

    # Render the items
    rendered_items = [item.render(request) for item in items]

    # Remove any unrendered items
    rendered_items = [item for item in rendered_items if item]

    # Render the edit bird
    return render(request, 'wagtailadmin/userbar/base.html', {
        'items': rendered_items,
    })