from django.contrib import admin
from models import *


class ConditionalAdmin(admin.ModelAdmin):
    pass
admin.site.register(Conditional, ConditionalAdmin)


class RuleAdmin(admin.ModelAdmin):
    pass
admin.site.register(Rule, RuleAdmin)


class ExcludedIPRangeAdmin(admin.ModelAdmin):
    pass
admin.site.register(ExcludedIPRange, ExcludedIPRangeAdmin)


class ConflictingIPAdmin(admin.ModelAdmin):
    pass
admin.site.register(ConflictingIP, ConflictingIPAdmin)


class VLanConfigAdmin(admin.ModelAdmin):
    pass
admin.site.register(VLanConfig, VLanConfigAdmin)


class ServiceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Service, ServiceAdmin)


class ProjectAdmin(admin.ModelAdmin):
    pass
admin.site.register(Project, ProjectAdmin)


class MTypeAdmin(admin.ModelAdmin):
    pass
admin.site.register(MType, MTypeAdmin)


class MachineAdmin(admin.ModelAdmin):
    pass
admin.site.register(Machine, MachineAdmin)


class DNSZoneAdmin(admin.ModelAdmin):
    pass
admin.site.register(DNSZone, DNSZoneAdmin)


class IfaceAdmin(admin.ModelAdmin):
    pass
admin.site.register(Iface, IfaceAdmin)


class EnvironmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Environment, EnvironmentAdmin)


class RoleAdmin(admin.ModelAdmin):
    pass
admin.site.register(Role, RoleAdmin)


class OperatingSystemAdmin(admin.ModelAdmin):
    pass
admin.site.register(OperatingSystem, OperatingSystemAdmin)


class VLanAdmin(admin.ModelAdmin):
    pass
admin.site.register(VLan, VLanAdmin)
