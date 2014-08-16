from django.db import models
from django.core.files.storage import FileSystemStorage
from PIL import Image as MyImage
from django.core.management import setup_environ
from django.conf import settings
from django.utils.translation import ugettext_lazy as _

fs = FileSystemStorage()

class DefaultClass(models.Model):
    name = models.CharField(max_length=255)
    ts = models.DateTimeField(auto_now=True)
    def __unicode__(self):
            return self.name
    
    class Meta:
        verbose_name_plural = "Default classes"

class ListClass(models.Model):
    name = models.CharField(max_length=255)
    ts = models.DateTimeField(auto_now=True)
    def __unicode__(self):
            return self.name

    class Meta:
        verbose_name_plural = "List classes"

class ParagraphClass(models.Model):
    name = models.CharField(max_length=255)
    ts = models.DateTimeField(auto_now=True)
    def __unicode__(self):
            return self.name
    
    class Meta:
        verbose_name_plural = "Paragraph classes"
    
class PageClass(models.Model):
    name = models.CharField(max_length=255)
    ts = models.DateTimeField(auto_now=True)
    def __unicode__(self):
            return self.name
    
    class Meta:
        verbose_name_plural = "Page classes"

class IllustrationClass(models.Model):
    name = models.CharField(max_length=255)
    ts = models.DateTimeField(auto_now=True)
    def __unicode__(self):
            return self.name
    

    class Meta:
        verbose_name_plural = "Illustration classes"


class ImageClass(models.Model):
    name = models.CharField(max_length=255)
    ts = models.DateTimeField(auto_now=True)
    def __unicode__(self):
            return self.name
    
    class Meta:
        verbose_name_plural = "Image classes"


class LinkClass(models.Model):
    name = models.CharField(max_length=255)
    ts = models.DateTimeField(auto_now=True)
    def __unicode__(self):
            return self.name
    
    class Meta:
        verbose_name_plural = "Link classes"

    
class ChapterClass(models.Model):
    name = models.CharField(max_length=255)
    ts = models.DateTimeField(auto_now=True)
    def __unicode__(self):
            return self.name

    class Meta:
        verbose_name_plural = "Chapter classes"


class Download(models.Model):
    number = models.IntegerField(default=0)
    kind = models.ForeignKey(DefaultClass)
    style = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    label = models.TextField(blank=True)
    path = models.FileField(upload_to='downloads/%Y/%m/%d', max_length=255, storage=fs)
    notes = models.TextField(blank=True)
    params = models.CharField(max_length=255, blank=True)
    ts = models.DateTimeField(auto_now=True)
    def __unicode__(self):
            return self.title
    
    def get_absolute_url(self):
        return '/downloads/%s' % self.path
        
    class Meta:
        ordering = ['number']


class MediaBox(models.Model):
    """Represents a generic media container. """
    number = models.IntegerField(default=0)
    kind = models.ForeignKey(DefaultClass)
    label_style = models.CharField(max_length=255, blank=True)
    image_style = models.CharField(max_length=255, blank=True)
    box_height = models.CharField(max_length=255, blank=True)
    box_width = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    label = models.TextField(blank=True)
    codebox = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/images/%Y/%m/%d', max_length=255, storage=fs, blank=True)
    media_path = models.FileField(upload_to='media/%Y/%m/%d', max_length=255, storage=fs, blank=True)
    notes = models.TextField(blank=True)
    params = models.CharField(max_length=255, blank=True)
    ts = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
            return self.title
    
    def get_image(self):
        
        return '/site_media/%s' % self.image
    
    def get_path(self):

        return '/site_media/%s' % self.media_path
        
    def save(self): 
        super(MediaLink, self).save()
        if self.image: 
            filename = self.image.path
            i = MyImage.open(filename) 
            wpercent = (148/float(i.size[0]))
            hsize = int((float(i.size[1])*float(wpercent)))
            i.thumbnail((148,hsize), MyImage.ANTIALIAS) 
            i.save(filename)
    
    class Meta:
        ordering = ['number']
        verbose_name_plural = 'Media Boxes'



    

    
class Illustration(models.Model):
    number = models.IntegerField(default=0)
    kind = models.ForeignKey(IllustrationClass)
    style = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    label = models.TextField(blank=True)
    path = models.FileField(upload_to='media/%Y/%m/%d', max_length=255, storage=fs)
    notes = models.TextField(blank=True)
    params = models.CharField(max_length=255, blank=True)
    ts = models.DateTimeField(auto_now=True)
    def __unicode__(self):
            return self.title
    
    def get_absolute_url(self):
        return '/site_media/%s' % self.path
        
    class Meta:
        ordering = ['number']


class Image(models.Model):
    number = models.IntegerField(default=0)
    kind = models.ForeignKey(ImageClass)
    image_style = models.CharField(max_length=255, blank=True)
    thumb_style = models.CharField(max_length=255, blank=True)
    link_style = models.CharField(max_length=255, blank=True)
    label_style = models.CharField(max_length=255, blank=True)
    image_width = models.IntegerField(blank=True, default=0)
    ALIGN_CHOICES = (
        ('left', 'Align image left'),
        ('right', 'Align image right'),
        ('', 'Show image inline'),
    )
    image_align = models.CharField(max_length=8, blank=True, choices=ALIGN_CHOICES)
    thumb_align = models.CharField(max_length=8, blank=True, choices=ALIGN_CHOICES)
    fullsize_align = models.CharField(max_length=8, blank=True, choices=ALIGN_CHOICES)
    title = models.CharField(max_length=255)
    label = models.TextField(blank=True)
    image = models.ImageField(upload_to='gallery/images/%Y/%m/%d', max_length=255, storage=fs, blank=True)
    thumb = models.ImageField(upload_to='gallery/thumbs/%Y/%m/%d', max_length=255, storage=fs, blank=True)
    fullsize = models.ImageField(upload_to='gallery/fullsize/%Y/%m/%d', max_length=255, storage=fs, blank=True)
    notes = models.TextField(blank=True)
    params = models.CharField(max_length=255, blank=True)
    ts = models.DateTimeField(auto_now=True)
    
    def get_image_size(self):
        """ get default image size from settings if a relevent setting exists"""
        if 'APP_IMAGE_SIZE' in dir(settings):
            if settings.APP_IMAGE_SIZE:
                return settings.APP_IMAGE_SIZE
            else:
                return None
        else:
            return None
            
    def get_thumb_size(self):
        """ get thumbnail image size from settings if a relevent setting exists"""
        if 'APP_THUMB_SIZE' in dir(settings):
            if settings.APP_THUMB_SIZE:
                return settings.APP_THUMB_SIZE
            else:
                return None
        else:
            return None
    
    def get_fullsize_size(self):
        """ get fullsize image size from settings if a relevent setting exists"""
        if 'APP_FULLSIZE_IMAGE_SIZE' in dir(settings):
            if settings.APP_FULLSIZE_IMAGE_SIZE:
                return settings.APP_FULLSIZE_IMAGE_SIZE
            else:
                return None
        else:
            return None
    
        
    def __unicode__(self):
            return self.title
    
    def get_absolute_url(self):
        return '/site_media/%s' % self.image, '/site_media/%s' % self.thumb, '/site_media/%s' % self.fullsize
    
    def get_image(self):
        return '/site_media/%s' % self.image
        
    def get_image_dimensions(self):
        filename = self.image.path
        try:
            i = MyImage.open(filename)
            return i.size[0], i.size[1]
        except:
            return None
            
    def get_thumb_dimensions(self):
        filename = self.thumb.path
        try:
            i = MyImage.open(filename)
            return i.size[0], i.size[1]
        except:
            return None
    
    def get_fullsize_dimensions(self):
        filename = self.fullsize.path
        try:
            i = MyImage.open(filename)
            return i.size[0], i.size[1]
        except:
            return None


    def get_thumb(self):
        return '/site_media/%s' % self.thumb

    def get_fullsize(self):
        return '/site_media/%s' % self.fullsize
    
        
    def save(self): 
        """Resizes image, thumb and fullsize while saving """
        super(Image, self).save() 
        if self.image: 
            size = self.get_image_size() if self.get_image_size() else self.image_width if self.image_width else 297
            filename = self.image.path
            i = MyImage.open(filename) 
            wpercent = (size/float(i.size[0]))
            hsize = int((float(i.size[1])*float(wpercent)))
            i.thumbnail((size,hsize), MyImage.ANTIALIAS) 
            i.save(filename)
        if not self.image_width: self.image_width = self.get_image_size()
        
        if self.thumb:
            size = self.get_thumb_size() if self.get_thumb_size() else 148
            filename = self.thumb.path
            i = MyImage.open(filename) 
            wpercent = (size/float(i.size[0]))
            hsize = int((float(i.size[1])*float(wpercent)))
            i.thumbnail((size,hsize), MyImage.ANTIALIAS) 
            i.save(filename)
            
        if self.fullsize:
            size = self.get_fullsize_size() if self.get_fullsize_size() else 917
            filename = self.fullsize.path
            i = MyImage.open(filename) 
            wpercent = (size/float(i.size[0]))
            hsize = int((float(i.size[1])*float(wpercent)))
            i.thumbnail((size,hsize), MyImage.ANTIALIAS) 
            i.save(filename)
        
    
    class Meta:
        ordering = ['number']

    
class RelativeLink(models.Model):
    number = models.IntegerField(default=0)
    kind = models.ForeignKey(LinkClass)
    chapter = models.ForeignKey("Chapter", blank=True, null=True)
    page = models.ForeignKey("Page", blank=True, null=True)
    text = models.CharField(max_length=255, blank=True)
    style = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    notes = models.TextField(blank=True)
    params = models.CharField(max_length=255, blank=True)
    ts = models.DateTimeField(auto_now=True)
    def __unicode__(self):
            return self.title
            
    class Meta:
        ordering = ['number']
    

class AbsoluteLink(models.Model):
    number = models.IntegerField(default=0)
    kind = models.ForeignKey(LinkClass)
    text = models.CharField(max_length=255, blank=True)
    style = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    path = models.URLField(verify_exists=True)
    notes = models.TextField(blank=True)
    params = models.CharField(max_length=255, blank=True)
    ts = models.DateTimeField(auto_now=True)
    def __unicode__(self):
            return self.title
    
    class Meta:
        ordering = ['number']
    

class EmailLink(models.Model):
    number = models.IntegerField(default=0)
    kind = models.ForeignKey(LinkClass)
    text = models.CharField(max_length=255, blank=True)
    style = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    email = models.EmailField()
    notes = models.TextField(blank=True)
    params = models.CharField(max_length=255, blank=True)
    ts = models.DateTimeField(auto_now=True)
    def __unicode__(self):
            return self.title
            
    class Meta:
        ordering = ['number']
    
                
     
class ListItem(models.Model):
    """Defines a list item dom element. Content is defined by one or more paragraphs"""
    kind = models.ForeignKey(DefaultClass, default="default")
    number = models.IntegerField(default=0)
    style = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    options = models.ManyToManyField("Option", blank=True)
    notes = models.TextField(blank=True)
    params = models.CharField(max_length=255, blank=True)
    ts = models.DateTimeField(auto_now=True)
    def __unicode__(self):       
        if not self.name:
            if len(self.text) > 35:
                return '%s...' % self.text[:35] 
            else:
                return self.text
        else:
            return self.name


    class Meta:
        ordering = ['number']
    
    
class List(models.Model):
    """Defines a list dom element"""
    kind = models.ForeignKey(ListClass, default='default')
    number = models.IntegerField(default=0)
    style = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255)
    list_items = models.ManyToManyField(ListItem)
    notes = models.TextField(blank=True)
    params = models.CharField(max_length=255, blank=True)
    ts = models.DateTimeField(auto_now=True)
    def __unicode__(self):
            return 'list %s %s' % (self.name, self.pk)
    
    class Meta:
        ordering = ['number']


class DataListData(models.Model):
    """Defines a dd dom element. Content is one or more paragraphs"""
    kind = models.ForeignKey(DefaultClass, default="default")
    number = models.IntegerField(default=0)
    style = models.CharField(max_length=255, blank=True)
    name = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    options = models.ManyToManyField("Option", blank=True)
    notes = models.TextField(blank=True)
    params = models.CharField(max_length=255, blank=True)
    ts = models.DateTimeField(auto_now=True)
    def __unicode__(self):       
        if not self.name:
            if len(self.text) > 35:
                return '%s...' % self.text[:35] 
            else:
                return self.text
        else:
            return self.name

    class Meta:
        ordering = ['number']
    

class DataListTitle(models.Model):
    """Defines a datalist title dom element"""
    kind = models.ForeignKey(DefaultClass, default='default')
    number = models.IntegerField(default=0)
    style = models.CharField(max_length=255, blank=True)
    text = models.CharField(max_length=255, blank=True)
    data_items = models.ManyToManyField(DataListData)
    notes = models.TextField(blank=True)
    params = models.CharField(max_length=255, blank=True)
    ts = models.DateTimeField(auto_now=True)
    def __unicode__(self):
            return self.text
            
    class Meta:
        ordering = ['number']

            
class DataList(models.Model):
    """Defines a datalist dom element"""
    kind = models.ForeignKey(DefaultClass, default='default')
    number = models.IntegerField(default=0)
    style = models.CharField(max_length=255, blank=True)
    data_titles = models.ManyToManyField(DataListTitle)
    name = models.CharField(max_length=255)
    header = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    params = models.CharField(max_length=255, blank=True)
    ts = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
            return 'datalist %s %s' % (self.name, self.pk)
    
    class Meta:
        ordering = ['number']
        
class Cell(models.Model):
    """Defines a table cell"""
    kind = models.ForeignKey(DefaultClass, default='default')
    number = models.IntegerField(default=0)
    style = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    options = models.ManyToManyField("Option", blank=True)
    notes = models.TextField(blank=True)
    params = models.CharField(max_length=255, blank=True)
    ts = models.DateTimeField(auto_now=True)
    

class Row(models.Model):
    """Defines a table row"""     
    kind = models.ForeignKey(DefaultClass, default='default')
    number = models.IntegerField(default=0)
    style = models.CharField(max_length=255, blank=True)
    cells = models.ManyToManyField(Cell)
    notes = models.TextField(blank=True)
    params = models.CharField(max_length=255, blank=True)
    ts = models.DateTimeField(auto_now=True)
       

class Table(models.Model):
    """Defines a table"""
    kind = models.ForeignKey(DefaultClass, default='default')
    number = models.IntegerField(default=0)
    style = models.CharField(max_length=255, blank=True)
    rows = models.ManyToManyField(Row)
    notes = models.TextField(blank=True)
    params = models.CharField(max_length=255, blank=True)
    ts = models.DateTimeField(auto_now=True)
    

class Option(models.Model):
    """Contains optional dom elements for all other models""" 
    number = models.IntegerField(default=0)
    images = models.ManyToManyField(Image, blank=True)
    illustrations = models.ManyToManyField(Illustration, blank=True)
    email_links = models.ManyToManyField(EmailLink, blank=True)
    relative_links = models.ManyToManyField(RelativeLink, blank=True)
    absolute_links = models.ManyToManyField(AbsoluteLink, blank=True)
    media_boxes = models.ManyToManyField(MediaBox, blank=True)
    data_lists = models.ManyToManyField(DataList, blank=True)
    lists = models.ManyToManyField(List, blank=True)
    downloads = models.ManyToManyField(Download, blank=True)
    tables = models.ManyToManyField(Table, blank=True)
    
    def __unicode__(self):
        
        names = []
        if self.images:
            for i in self.images.all():
                names.append(''.join(['img: ', i.title]))
        if self.illustrations:
            for ill in self.illustrations.all():
                names.append(''.join(['ill: ', ill.title]))
        if self.email_links:
            for e in self.email_links.all():
                names.append(''.join(['email: ', e.title]))
        if self.relative_links:
            for rel in self.relative_links.all():
                names.append(''.join(['rel: ', rel.title]))
        if self.absolute_links:
            for abs in self.absolute_links.all():
                names.append(''.join(['abs: ', abs.title]))
        if self.media_boxes:
            for med in self.media_boxes.all():
                names.append(''.join(['media: ', med.title]))
        if self.data_lists:
            for dl in self.data_lists.all():
                names.append(''.join(['dl: ', dl.name]))
        if self.lists:
            for l in self.lists.all():
                names.append(''.join(['list: ', l.name]))
        if self.tables:
            for t in self.tables.all():
                for tr in t.rows.all():
                    for td in tr.cells.all():
                        names.append(''.join(['table: ', td.text]))
        
        r = ', '.join(names)
        ret = r if len(r) < 80 else r[:80]
        return ret
                    

    
    class Meta:
        ordering = ['number']
         
    
class Paragraph(models.Model):
    number = models.IntegerField(default=0)
    kind = models.ForeignKey(ParagraphClass, default='default')
    name = models.CharField(max_length=255)
    text_style = models.CharField(max_length=255, blank=True)
    header_style = models.CharField(max_length=255, blank=True)
    header = models.CharField(max_length=255, blank=True)
    text = models.TextField(blank=True)
    options = models.ManyToManyField(Option, blank=True)
    publish_date = models.DateField()
    notes = models.TextField(blank=True)
    params = models.CharField(max_length=255, blank=True)
    ts = models.DateTimeField(auto_now=True)
    def __unicode__(self):
            return self.name
            
    class Meta:
        ordering = ['number']
        
        
class MetaTag(models.Model):
    """Represents a group of meta tags"""
    name = models.CharField(max_length=255)
    meta_keywords = models.TextField(blank=True)
    meta_description = models.TextField(blank=True)
    meta_author = models.CharField(max_length=255, blank=True)
    meta_copyright = models.CharField(max_length=255, blank=True)
    meta_robots = models.CharField(max_length=255, blank=True)
    meta = models.CharField(max_length=255, blank=True, help_text=_('Write you own meta tag here in HTML'))
    notes = models.TextField(blank=True)
    ts = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.name

class Page(models.Model):
    number = models.IntegerField(default=0)
    kind = models.ForeignKey(PageClass)
    metatag = models.ForeignKey(MetaTag, blank=True)
    paragraphs = models.ManyToManyField(Paragraph)   
    title_style = models.CharField(max_length=255, blank=True)
    summary_style = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField()   
    summary = models.TextField(blank=True)
    publish_date = models.DateField()
    notes = models.TextField(blank=True)
    params = models.CharField(max_length=255, blank=True)
    ts = models.DateTimeField(auto_now=True)
    def __unicode__(self):
            return "%(title)s, %(slug)s" % {'title': self.title, 'slug': self.slug}
            
    class Meta:
        ordering = ['number']



class Chapter(models.Model):
    number = models.IntegerField(default=0)
    kind = models.ForeignKey(ChapterClass, blank=True, null=True)
    pages = models.ManyToManyField(Page, blank=True)
    style = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField()   
    notes = models.TextField(blank=True)
    params = models.CharField(max_length=255, blank=True)
    ts = models.DateTimeField(auto_now=True)
    def __unicode__(self):
            return self.title    
            
    class Meta:
        ordering = ['number']
        
        

    