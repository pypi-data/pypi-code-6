from django.conf.urls import patterns, include, url
from quintet.backend.forms import SetPasswordFormWithMeter


urlpatterns = patterns('quintet.backend.views',
    url(r'^$', 'dashboard', name='dashboard'),

    url(r'^posts/$', 'list_posts', {'filter': 'my_posts'}, name='my_posts'),
    url(r'^posts/all/$', 'list_posts', name='all_posts'),
    url(r'^posts/(?P<filter>\w+)/$', 'list_posts', name='list_posts'),

    url(r'^post/$', 'create_post', name='create_post'),
    url(r'^post/(?P<pk>\d+)/$', 'edit_post', name='edit_post'),
    url(r'^post/(?P<pk>\d+)/view/$', 'view_post', name='view_post'),

    url(r'^post/(?P<pk>\d+)/add_contributor/$', 'add_contributor', name='add_contributor'),
    url(r'^post/(?P<pk>\d+)/edit_contributor/(?P<contributor_pk>\d+)/$', 'edit_contributor', name='edit_contributor'),
    url(r'^post/(?P<pk>\d+)/remove_contributor/(?:(?P<contributor_pk>\d+)/)?$', 'remove_contributor', name='remove_contributor'),

    url(r'^post/(?P<pk>\d+)/add_reviewer/$', 'add_reviewer', name='add_reviewer'),
    url(r'^post/(?P<pk>\d+)/remove_reviewer/(?:(?P<reviewer_pk>\d+)/)?$', 'remove_reviewer', name='remove_reviewer'),

    url(r'^post/(?P<pk>\d+)/set_status/(?P<status>[A-Z])/$', 'set_post_status', name='set_post_status'),
    url(r'^post/(?P<pk>\d+)/publish/$', 'publish_post', name='publish_post'),
    url(r'^post/(?P<pk>\d+)/archive/$', 'archive_post', name='archive_post'),
    url(r'^post/(?P<pk>\d+)/delete/$', 'delete_post', name='delete_post'),

    url(r'^post/(?P<pk>\d+)/approve/$', 'approve_post', name='approve_post'),
    url(r'^post/(?P<pk>\d+)/unapprove/$', 'unapprove_post', name='unapprove_post'),

    url(r'^post/(?P<pk>\d+)/comment/$', 'add_comment', name='add_comment'),
    url(r'^post/(?P<pk>\d+)/delete_comment/(?:(?P<comment_pk>\d+)/)?$', 'delete_comment', name='delete_comment'),

    url(r'^pages/$', 'list_pages', name='list_pages'),
    url(r'^page/$', 'create_page', name='create_page'),
    url(r'^page/(?P<pk>\d+)/$', 'edit_page', name='edit_page'),
    url(r'^page/(?P<pk>\d+)/set_status/(?P<status>[A-Z])/$', 'set_page_status', name='set_page_status'),
    url(r'^page/(?P<pk>\d+)/publish/$', 'publish_page', name='publish_page'),
    url(r'^page/(?P<pk>\d+)/archive/$', 'archive_page', name='archive_page'),
    url(r'^page/(?P<pk>\d+)/delete/$', 'delete_page', name='delete_page'),

    url(r'^users/$', 'list_users', name='list_users'),
    url(r'^user/add/$', 'add_user', name='add_user'),
    url(r'^user/(?P<pk>\d+)/$', 'edit_user', name='edit_user'),
    url(r'^user/(?P<pk>\d+)/change_photo/$', 'change_photo', name='change_photo'),
    url(r'^user/(?P<pk>\d+)/change_password/$', 'change_password', name='change_password'),
    url(r'^user/(?P<pk>\d+)/edit_permissions/$', 'edit_permissions', name='edit_permissions'),
    url(r'^user/(?P<pk>\d+)/delete/$', 'delete_user', name='delete_user'),

    url(r'^sections/$', 'list_sections', name='list_sections'),
    url(r'^sections/add$', 'add_section', name='add_section'),
    url(r'^sections/(?P<pk>\d+)/delete/$', 'delete_section', name='delete_section'),

    url(r'^markdown/', include('django_bootstrap_markdown.urls')),
)

urlpatterns += patterns('django.contrib.auth.views',
    url(r'^login/$', 'login',
        {
            'template_name': 'quintet/login.html',
        },
        name='quintet_login',),
    url(r'^logout/$', 'logout',
        {
            'next_page': '/',
        },
        name='quintet_logout',),
    url(r'^reset_password/$', 'password_reset', name='password_reset'),
    url(r'^reset_password/done/$', 'password_reset_done', name='password_reset_done'),
    url(r'^reset_password/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'password_reset_confirm', {'set_password_form': SetPasswordFormWithMeter},
        name='password_reset_confirm'),
    url(r'^reset_password/complete/$', 'password_reset_complete', name='password_reset_complete'),
)
