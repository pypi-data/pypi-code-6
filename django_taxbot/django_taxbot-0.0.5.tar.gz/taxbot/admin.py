from django.contrib import admin
from taxbot import models as mod

# Register your models here.
admin.site.register(mod.Tax)
admin.site.register(mod.CanadianTax)
