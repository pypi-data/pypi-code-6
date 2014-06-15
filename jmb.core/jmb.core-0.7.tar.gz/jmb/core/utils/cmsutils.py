#! -*- coding: utf-8 -*-
# jmb.core cms utilities
#
# Helper classes and methods to be used with django-cms


def get_page_from_slug(pageslug, language="it"):
    """
    Try to retrieve a Page object from its slug
    :param pageslug: the page slug
    :return: a Page object with that slug, else None
    """
    try:
        from cms.models import Title, Page
        title = Title.objects.filter(slug=pageslug, language=language)[0]
        page = Page.objects.get(pk=title.page.id)
        return page
    except ImportError, e:
        print e
        # cms not installed in project/app
        return None
    except (Title.DoesNotExist, Page.DoesNotExist), e:
        print e
        return None


def get_abs_url_from_slug(pageslug):
    """
    Try to resolve the absolute path of a cms page from its slug
    :param pageslug: the page slug
    :return:the absolute path of page, or None
    """
    try:
        return get_page_from_slug(pageslug).get_absolute_url()
    except:
        return None

# def get_plugin_instance_from_page(pageslug):
#     """
#
#     :param pageslug:
#     :return:
#     """
#     page = get_page_from_slug(pageslug)
#     if page:
