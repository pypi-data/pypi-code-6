# Copyright (c) 2014 by Manuel Saelices
#
# This file is part of django-pageguide
#
# django-pageguide is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# django-pageguide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with django-pageguide.  If not, see <http://www.gnu.org/licenses/>.

from django.contrib import admin

from .models import PageGuide, PageGuideStep


class PageGuideStepInline(admin.TabularInline):
    model = PageGuideStep


class PageGuideAdmin(admin.ModelAdmin):
    inlines = [PageGuideStepInline]



admin.site.register(PageGuide, PageGuideAdmin)
