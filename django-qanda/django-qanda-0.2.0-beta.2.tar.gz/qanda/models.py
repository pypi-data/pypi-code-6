from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _


class AutoTimestampBase(models.Model):
    """Abstract base class to automatically set timestamps.

    Adds the fields 'created' and 'modified' to child classes.
    """

    created = models.DateTimeField(_('created'), blank=True, null=True)
    modified = models.DateTimeField(_('modified'), blank=True, null=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        """
        Set the modified and created, if required, timestamps.
        """
        self.modified = timezone.now()
        if not self.created:
            self.created = self.modified
        super(AutoTimestampBase, self).save(*args, **kwargs)


class TopicManager(models.Manager):

    def for_staff(self):
        """
        Return all topics whose questions are published.
        """
        qs = super(TopicManager, self).get_queryset()
        return qs.distinct().filter(questions__is_published=True)

    def for_members(self):
        """
        Return all topics whose questions are published and have public or
        members access level.
        """
        return self.distinct().filter(
            questions__is_published=True,
            questions__access__in=[Question.PUBLIC, Question.MEMBERS]
            )

    def for_anonymous(self):
        """
        Return all topics whose questions are published and
        have public access level.
        """
        return self.distinct().filter(
            questions__is_published=True,
            questions__access=Question.PUBLIC
            )


@python_2_unicode_compatible
class Topic(models.Model):
    """
    Generic Topics for FAQ questions.
    """
    title = models.CharField(_('title'), max_length=150, unique=True)
    slug = models.SlugField(_('slug'), max_length=150, unique=True)
    description = models.TextField(_('description'), blank=True)
    order = models.IntegerField(_('sort order'), default=0)

    # Managers
    objects = TopicManager()

    class Meta:
        ordering = ['order', 'title', ]
        verbose_name = _('topic')
        verbose_name_plural = _('topics')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse(
            'qanda.views.topicdetail',
            kwargs={'topic_slug': self.slug}
            )


class PublishedQuestionManager(models.Manager):

    use_for_related_fields = True

    def get_queryset(self):
        """
        Return all questions which are published.
        """
        qs = super(PublishedQuestionManager, self).get_queryset()
        return qs.filter(is_published=True)

    def for_members(self):
        """
        Return all questions which have public or members access.
        """
        return self.filter(access__in=[self.model.PUBLIC, self.model.MEMBERS])

    def for_anonymous(self):
        """
        Return all questions which have public access.
        """
        return self.filter(access=self.model.PUBLIC)


@python_2_unicode_compatible
class Question(AutoTimestampBase):
    """
    A frequently asked question.
    """
    text = models.TextField(_('question'))
    slug = models.SlugField(_('slug'), max_length=100, unique=True)
    answer = models.TextField(_('answer'), blank=True)
    topic = models.ForeignKey(
        Topic,
        verbose_name=_('topic'),
        related_name='questions'
        )

    is_published = models.BooleanField(_('is published?'), default=False)
    PUBLIC = 0
    MEMBERS = 1
    STAFF = 2
    ACCESS_CHOICES = (
        (PUBLIC, _('Public')),
        (MEMBERS, _('Members')),
        (STAFF, _('Staff')),
        )
    access = models.PositiveSmallIntegerField(
        _('access'),
        choices=ACCESS_CHOICES,
        default=PUBLIC,
        )

    order = models.IntegerField(_('sort order'), default=0)

    # Managers
    objects = models.Manager()
    published = PublishedQuestionManager()

    class Meta:
        ordering = ['order', 'created', ]
        verbose_name = _('question')
        verbose_name_plural = _('questions')

    def __str__(self):
        return self.text

    def get_absolute_url(self):
        return reverse(
            'qanda.views.questiondetail',
            kwargs={
                'topic_slug': self.topic.slug,
                'question_slug': self.slug
                }
            )
