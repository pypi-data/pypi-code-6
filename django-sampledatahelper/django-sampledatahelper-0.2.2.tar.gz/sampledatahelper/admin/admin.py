from django.contrib import admin

class SampledatahelperAdmin(admin.ModelAdmin):
    change_list_template = "sampledatahelper/admin/change_list.html"
