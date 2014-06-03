from django.conf.urls.defaults import url, patterns
from pgsearch.views import ModalSearchView
from pgsearch.forms import PGSearchForm
from djinn_forms.views.fileupload import UploadView
from djinn_forms.views.relate import RelateSearch
from djinn_forms.views.contentimages import ContentImages
from django.views.decorators.csrf import csrf_exempt


urlpatterns = patterns(

    "",

    url(r'^fileupload$',
        csrf_exempt(UploadView.as_view()),
        name='djinn_forms_fileupload'
        ),

    url(r'^searchrelate$',
        RelateSearch.as_view(),
        name='djinn_forms_relatesearch'
        ),

    url(r'^contentimages/(?P<ctype>[\w]+)/(?P<pk>[\d]+)$',
        ContentImages.as_view(),
        name='djinn_forms_contentimages'
        ),

    # TODO: Move views/form to this module
    url(r'^contentlinks/',
        ModalSearchView(
            load_all=False,
            form_class=PGSearchForm,
            template='djinn_forms/snippets/contentlinks.html'
        ),
        name='haystack_link_popup'),

    url(r'^contentlinks_search/',
        ModalSearchView(
            load_all=False,
            form_class=PGSearchForm,
        ),
        name='haystack_link_search')
)
