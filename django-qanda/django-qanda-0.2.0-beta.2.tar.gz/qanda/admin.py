from django.contrib import admin
from .models import Topic, Question


def action_message(model, count, actioned_phrase):
    singular = model._meta.verbose_name.lower()
    plural = model._meta.verbose_name_plural.lower()
    if count == 1:
        message_bit = '1 {} was'.format(singular)
    else:
        message_bit = '{} {} were'.format(count, plural)
    return '{} successfully {}.'.format(message_bit, actioned_phrase)


def make_published(modeladmin, request, queryset):
    actioned_phrase = 'published'
    row_count = queryset.update(is_published=True)
    modeladmin.message_user(
        request,
        action_message(queryset.model, row_count, actioned_phrase)
        )
make_published.short_description = 'Publish selected questions'


def make_unpublished(modeladmin, request, queryset):
    actioned_phrase = 'unpublished'
    row_count = queryset.update(is_published=False)
    modeladmin.message_user(
        request,
        action_message(queryset.model, row_count, actioned_phrase)
        )
make_unpublished.short_description = 'Unpublish selected questions'


def make_staff_access(modeladmin, request, queryset):
    actioned_phrase = 'given staff access'
    row_count = queryset.update(access=Question.STAFF)
    modeladmin.message_user(
        request,
        action_message(queryset.model, row_count, actioned_phrase)
        )
make_staff_access.short_description = 'Give staff access to selected questions'


def make_member_access(modeladmin, request, queryset):
    actioned_phrase = 'given member access'
    row_count = queryset.update(access=Question.MEMBERS)
    modeladmin.message_user(
        request,
        action_message(queryset.model, row_count, actioned_phrase)
        )
make_member_access.short_description = (
    'Give member access to selected questions'
    )


def make_public_access(modeladmin, request, queryset):
    actioned_phrase = 'given public access'
    row_count = queryset.update(access=Question.PUBLIC)
    modeladmin.message_user(
        request,
        action_message(queryset.model, row_count, actioned_phrase)
        )
make_public_access.short_description = (
    'Give public access to selected questions'
    )


class TopicAdmin(admin.ModelAdmin):
    list_display = ('title',)
    prepopulated_fields = {'slug': ('title',)}


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'topic', 'access', 'is_published', 'modified')
    list_filter = ('is_published', 'access', 'topic')
    readonly_fields = ('created', 'modified')
    search_fields = ('text', 'answer')
    prepopulated_fields = {'slug': ('text',)}
    actions = [
        make_published,
        make_unpublished,
        make_staff_access,
        make_member_access,
        make_public_access
        ]

admin.site.register(Topic, TopicAdmin)
admin.site.register(Question, QuestionAdmin)
