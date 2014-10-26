from django.contrib import admin
from .models import (Profile, Section, Tag, Post, Page,Comment, Role,
    Contributor, RecentActivity)


admin.site.register(Profile)
admin.site.register(Section)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Page)
admin.site.register(Comment)
admin.site.register(Role)
admin.site.register(Contributor)
admin.site.register(RecentActivity)
