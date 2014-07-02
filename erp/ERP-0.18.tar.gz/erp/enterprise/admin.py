__author__ = 'cltanuki'
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from .models import CorpUser, CorpUnit, CorpObject

from erp.enterprise.forms import UserChangeForm, UserCreationForm, UnitCreateForm


class CorpUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('username', 'email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': ('date_of_birth', 'first_name', 'last_name', 'mid_name', 'groups')}),
        ('Permissions', {'fields': ('is_admin', 'is_superuser')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'date_of_birth', 'password1', 'password2')}
        ),
    )
    search_fields = ('username', 'email')
    ordering = ('username', 'email')
    filter_horizontal = ()


class CorpUnitAdmin(GroupAdmin):
    # The forms to add and change user instances
    form = UnitCreateForm
    add_form = UnitCreateForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('name', 'chief')
    list_filter = ('name', 'chief')
    fieldsets = (
        (None, {'fields': ('name',)}),
        ('Personal info', {'fields': ('chief',)}),
        ('Permissions', {'fields': ('permissions',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('chief',)}
        ),
    )
    search_fields = ('name', 'chief')
    ordering = ('name', 'chief')
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(CorpUser, CorpUserAdmin)
admin.site.register(CorpUnit, CorpUnitAdmin)
admin.site.unregister(Group)
admin.site.register(CorpObject)