"""This module contains models for Quintet."""

from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.templatetags.static import static
from imagekit.models import ImageSpecField
from imagekit.processors import Transpose, ResizeToFill
from markdown import markdown


class Profile(models.Model):

    """This model holds extra user information."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    photo = models.ImageField(
        upload_to='user_photos',
        blank=True
    )
    thumbnail = ImageSpecField(source='photo',
        processors=[Transpose(), ResizeToFill(200, 200)],
        format='JPEG',
        options={
            'quality': 80,
        }
    )
    twitter = models.CharField(max_length=50, blank=True)
    bio = models.TextField(blank=True)

    class Meta:
        permissions = (
            ("set_perms", "Can set a users permissions"),
        )

    def __unicode__(self):
        """Return the users full name."""
        return self.user.get_full_name()

    def get_photo_url(self):
        if self.photo:
            return self.photo.url
        return static('img/default.jpg')

    def get_thumbnail_url(self):
        if self.photo:
            return self.thumbnail.url
        return static('img/default.jpg')

    def get_absolute_url(self):
        return reverse('quintet.blog.views.list_posts', kwargs={
            'contributor': self.user.username,
        })

    def get_admin_url(self):
        return reverse('edit_user', kwargs={
            'pk': self.user.pk
        })


class Section(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField()

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        """Return the Section name."""
        return self.name

    def get_absolute_url(self):
        return reverse('quintet.blog.views.list_posts', kwargs={
            'section': self.slug,
        })


class Tag(models.Model):
    title = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        """Return the tag name."""
        return self.title

    def get_absolute_url(self):
        return reverse('quintet.blog.views.list_posts', kwargs={
            'tag': self.slug,
        })


class Post(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(blank=True)
    section = models.ForeignKey(Section, blank=True, null=True)
    markdown = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.CharField(
        max_length=1,
        choices=(
            ('D', 'Draft'),
            ('R', 'Ready for Review'),
            ('S', 'Scheduled'),
            ('P', 'Published'),
            ('H', 'Hidden'),
            ('A', 'Archived'),
        ),
        default='D'
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    reviewers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='reviewing',
        blank=True
    )
    approved_by = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='approved',
        blank=True
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-date_published', '-date_updated']
        permissions = (
            ("publish_post", "Can publish posts"),
        )

    def __unicode__(self):
        """Return the Post title."""
        return self.title

    def html(self):
        """Return the markdown converted to HTML."""
        return markdown(self.markdown)

    def authors(self):
        return self.contributors.filter(role__title='Author')

    def get_absolute_url(self):
        return reverse('quintet.blog.views.view_posts', kwargs={
            'section': self.section.slug,
            'post': self.slug,
        })

    def get_admin_url(self):
        return reverse('edit_post', kwargs={
            'pk': self.pk
        })

    def get_set_draft_url(self):
        return reverse('set_post_status', kwargs={
            'pk': self.pk,
            'status': 'D',
        })

    def get_set_ready_for_review_url(self):
        return reverse('set_post_status', kwargs={
            'pk': self.pk,
            'status': 'R',
        })

    def get_set_show_url(self):
        return reverse('set_post_status', kwargs={
            'pk': self.pk,
            'status': 'P',
        })

    def get_set_hidden_url(self):
        return reverse('set_post_status', kwargs={
            'pk': self.pk,
            'status': 'H',
        })

    def get_publish_url(self):
        return reverse('publish_post', kwargs={
            'pk': self.pk,
        })

    def get_archive_url(self):
        return reverse('archive_post', kwargs={
            'pk': self.pk,
        })

    def get_delete_url(self):
        return reverse('delete_post', kwargs={
            'pk': self.pk,
        })


class Page(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(blank=True)
    markdown = models.TextField(blank=True)
    status = models.CharField(
        max_length=1,
        choices=(
            ('D', 'Draft'),
            ('R', 'Ready for Review'),
            ('S', 'Scheduled'),
            ('P', 'Published'),
            ('H', 'Hidden'),
            ('A', 'Archived'),
        ),
        default='D'
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    date_published = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-date_published', '-date_updated']
        permissions = (
            ("publish_page", "Can publish page"),
        )

    def __unicode__(self):
        """Return the page title."""
        return self.title

    def html(self):
        """Return the markdown converted to HTML."""
        return markdown(self.markdown)

    def get_absolute_url(self):
        return reverse('quintet.blog.views.view_page', kwargs={
            'post': self.slug,
        })

    def get_admin_url(self):
        return reverse('edit_page', kwargs={
            'pk': self.pk
        })

    def get_set_draft_url(self):
        return reverse('set_page_status', kwargs={
            'pk': self.pk,
            'status': 'D',
        })

    def get_set_ready_for_review_url(self):
        return reverse('set_page_status', kwargs={
            'pk': self.pk,
            'status': 'R',
        })

    def get_set_show_url(self):
        return reverse('set_page_status', kwargs={
            'pk': self.pk,
            'status': 'P',
        })

    def get_set_hidden_url(self):
        return reverse('set_page_status', kwargs={
            'pk': self.pk,
            'status': 'H',
        })

    def get_publish_url(self):
        return reverse('publish_page', kwargs={
            'pk': self.pk,
        })

    def get_archive_url(self):
        return reverse('archive_page', kwargs={
            'pk': self.pk,
        })

    def get_delete_url(self):
        return reverse('delete_page', kwargs={
            'pk': self.pk,
        })


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    comment = models.TextField()
    excerpt = models.TextField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __unicode__(self):
        """Return the comment text."""
        return self.comment


class Role(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField()

    def __unicode__(self):
        """Return role title."""
        return self.title


class Contributor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    post = models.ForeignKey(Post, related_name='contributors')
    role = models.ManyToManyField(Role)

    def __unicode__(self):
        """Return the User's full name."""
        return self.user.get_full_name()


class RecentActivityManager(models.Manager):
    def log_action(self, user, content_type, object_id, change_message):
        action = self.model(
            user=user,
            content_type=content_type,
            object_id=object_id,
            change_message=change_message
        )
        action.save()


class RecentActivity(models.Model):
    timestamp = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.TextField(blank=True, null=True)
    change_message = models.TextField(blank=True)

    objects = RecentActivityManager()

    class Meta:
        ordering = ('-timestamp',)

    def __unicode__(self):
        return self.change_message

    def url(self):
        """Return the URL to edit the object represented by this entry."""
        return None
