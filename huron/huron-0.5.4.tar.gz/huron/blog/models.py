# -- coding:utf-8 --
from django.db import models
from django.template.defaultfilters import slugify
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

try:
    from cStringIO import StringIO
except:
    from io import BytesIO as StringIO

from PIL import Image as PILImage
from PIL import ImageOps

from huron.utils.models import has_changed, RichTextField

from datetime import datetime


class PostManager(models.Manager):
    def get_published(self):
        return self.filter(pub_date__lte=datetime.today(), published=True)


@python_2_unicode_compatible
class Category(models.Model):
    """

    Category model for blog entries

    Fields available:

    * title - str
    * slug - str

    .. note::
        Those fields are available for a Category object and can be called in
        templates

    """
    title = models.CharField(_(u'title'), max_length=100)
    slug = models.SlugField(_(u'slug'), max_length=100, unique=True)

    def get_absolute_url(self):
        """Return permalink of the category"""
        return reverse('blog:list_blog_categ', None, [self.slug])

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Post(models.Model):
    """

    Post model of blog application

    Fields available:

    * title - str
    * image - image
    * short_desc - str
    * article - str
    * slug - str
    * rec_date - date
    * pub_date - date
    * last_mod - date
    * published - bool
    * categories - manytomany

    .. note::
        Those fields are available for a Post object and can be called in
        templates

    """
    title = models.CharField(_(u'title'), max_length=100)
    image = models.ImageField(_(u'main image'), upload_to=u'blog',
                              blank=True, null=True)
    short_desc = RichTextField(_(u'short description'), blank=True)
    article = RichTextField(_(u'article'), )
    slug = models.SlugField(_(u'slug'), max_length=100, unique=True)
    rec_date = models.DateField(_(u'recording date'), auto_now_add=True)
    pub_date = models.DateTimeField(_(u'publication date'), blank=True)
    last_mod = models.DateTimeField(_(u'last modification date'),
                                    auto_now=True)
    published = models.BooleanField(_(u'published'), default=False)
    categories = models.ManyToManyField(Category)
    objects = PostManager()

    def save(self, *args, **kwargs):
        if has_changed(self, 'image'):
            if self.image:
                filename = slugify(self.title)
                image = PILImage.open(self.image.file)

                if image.mode not in ('L', 'RGB'):
                    image = image.convert('RGB')

                imagefit = ImageOps.fit(image, (340, 220), PILImage.ANTIALIAS)

                temp = StringIO()
                try:
                    imagefit.save(temp, 'jpeg')
                except TypeError:
                    temp.seek(0)
                    imagefit.save(temp, 'jpeg')
                temp.seek(0)

                self.image.save(
                    filename+'.jpg',
                    SimpleUploadedFile('temp', temp.read()),
                    save=False)

        # Save this Post instance
        if self.pub_date == '' or not self.pub_date:
            self.pub_date = datetime.now()
        super(Post, self).save()

    def get_absolute_url(self):
        """Return permalink of the post object"""
        return reverse('blog:single', None, [self.pub_date.day,
                                             self.pub_date.month,
                                             self.pub_date.year,
                                             self.slug])

    def __str__(self):
        return self.title
