
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.core.mail import send_mail,mail_admins
from django.conf import settings
import urllib

def redirect_with_auth_superuser(request,tag,suburl):#,redirect_tag=None,except_url=None):
    """If access user is a superuser and return return X-Accel-Redirect.
    """

    if(request.user.is_superuser):
        if(tag in settings.DJANGO_REDIRECTER_SUPERUSER):
            return make_redirect_header(request,settings.DJANGO_REDIRECTER_SUPERUSER[tag],suburl)
        raise Http404
    raise PermissionDenied


def redirect_with_auth_staff(request,tag,suburl):#,redirect_tag=None,except_url=None):
    """If access user is a staff and return return X-Accel-Redirect.
    """
    if(request.user.is_staff):
        if(tag in settings.DJANGO_REDIRECTER_STAFF):
            return make_redirect_header(request,settings.DJANGO_REDIRECTER_STAFF[tag],suburl)
        raise Http404
    raise PermissionDenied


def redirect_with_auth_group(request,tag,suburl):#,redirect_tag=None,except_url=None):
    """If access user is a group and return return X-Accel-Redirect.
    """
    if(tag in settings.DJANGO_REDIRECTER_GROUP):
        (redirect_tag,groupname) = settings.DJANGO_REDIRECTER_GROUP[tag]
        if(request.user.groups.filter(name=groupname).count()>0):
            return make_redirect_header(request,redirect_tag,suburl)
        raise PermissionDenied
    raise Http404


def redirect_with_auth_login(request,tag,suburl):#,redirect_tag=None,except_url=None):
    """If access user is a staff and return return X-Accel-Redirect.
    """

    if(request.user.is_authenticated()):
        if(tag in settings.DJANGO_REDIRECTER_LOGIN):
            return make_redirect_header(request,settings.DJANGO_REDIRECTER_LOGIN[tag],suburl)
        raise Http404
    raise PermissionDenied


def redirect_for_exceptions(request, tag, suburl):
    """ Check tag in settings.DJANGO_REDIRECTER_EXCEPT and return X-Accel-Redirect when True.
    """
    if(tag in settings.DJANGO_REDIRECTER_EXCEPT):
        return make_redirect_header(request,settings.DJANGO_REDIRECTER_EXCEPT[tag],suburl)
    raise Http404


def make_redirect_header(request,redirect_tag,suburl):

    flag = False
    for key,item in request.GET.items():
        if(not flag):
            flag = True
            suburl = "%s?%s=%s" % (suburl,key,urllib.quote(item))
        else:
            suburl = "%s&%s=%s" % (suburl,key,urllib.quote(item))

    if(redirect_tag[-1]!="/"):
        redirect_tag = redirect_tag+"/"

    if(redirect_tag.find("://")!=-1):
        head="%s%s"  % (redirect_tag,suburl)
    else:
        if(redirect_tag[0]=="/"):
            head="%s%s"  % (redirect_tag,suburl)
        else:
            head="/%s%s"  % (redirect_tag,suburl)

    response = HttpResponse()
    response['X-Accel-Redirect']=head

    return response
