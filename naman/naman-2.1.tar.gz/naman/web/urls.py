from django.conf.urls import url, patterns, include


urlpatterns = patterns("",
    url(r"^machine/delete/(\d+)?/?", "naman.web.views_machine.delete", name="delete_machine"),
    url(r"^machine/(\d+)?/?", "naman.web.views_machine.edit", name="machine"),
    url(r"^machines", "naman.web.views_machine.listado", name="machines"),

     url(r"^service/(\d+)?/?", "naman.web.views_service.edit", name="service"),

    #url(r"^service/(\d+)?/?", "naman.web.views_machine.edit", name="machine"),


    url(r"^iface/delete/(\d+)?/?", "naman.web.views_iface.delete", name="delete_iface"),
    #url(r"^iface_short/(\d+)?/?", "web.views_iface.edit_short", name="iface_short"),
    url(r"^iface_by_machine/(\d+)?/?", "naman.web.views_iface.edit_by_machine", name="iface_by_machine"),
    url(r"^iface/(\d+)?/?", "naman.web.views_iface.edit", name="iface"),
    url(r"^ifaces_by_machine_json/(\d+)?/?(\d+)?", "naman.web.views_iface.list_by_machine_json", name="ifaces_by_machine_json"),
    url(r"^ifaces_by_machine/(\d+)?/?(\d+)?", "naman.web.views_iface.list_by_machine", name="ifaces_by_machine"),
    url(r"^ifaces", "naman.web.views_iface.listado", name="ifaces"),

    url(r"^conflictingip/(\d+)?/?", "naman.web.views_conflicting_ip.edit_modal", name="conflictingip_modal"),

    url(r"^vlanconfig/(\d+)?/?", "naman.web.views_vlanconfig.edit", name="vlanconfig"),

    url('^conflicting_ip.js$', 'naman.web.views_js.conflicting_ip', name='conflicting_ip_js'),
    url('^iface.js$', 'naman.web.views_js.iface', name='iface_js'),
    url('^machine.js$', 'naman.web.views_js.machine', name='machine_js'),
    url('^vlanconfig.js$', 'naman.web.views_js.vlanconfig', name='vlanconfig_js'),

    url('^login/?$', 'django.contrib.auth.views.login', name='login'),
    url('^logout/', 'django.contrib.auth.views.logout', {'next_page':'/login?next=/'}, name='logout'),
    url(r"^", "naman.web.views.home", name="home"),
)

