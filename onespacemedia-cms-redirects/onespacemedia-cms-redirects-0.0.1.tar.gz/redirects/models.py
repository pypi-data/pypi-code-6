from django.db import models


class Redirect(models.Model):

    old_path = models.CharField(
        'redirect from',
        max_length=200,
        db_index=True,
        unique=True,
        help_text="This should be an absolute path, excluding the domain name. Example: '/events/search/'."
    )

    new_path = models.CharField(
        'redirect to',
        max_length=200,
        blank=True,
        help_text="This can be either an absolute path (as above) or a full URL starting with 'http://'."
    )

    class Meta:
        verbose_name = 'redirect'
        verbose_name_plural = 'redirects'
        ordering = ('old_path',)

    def __unicode__(self):
        return self.old_path
