from django.conf import settings
from django.db import models
from django.utils.timezone import now


# Image upload support
class Image(models.Model):
    file = models.ImageField(upload_to="content_images/%Y/%m/%d/",
                             height_field="height", 
                             width_field="width")

    height = models.PositiveIntegerField(blank=True)
    width = models.PositiveIntegerField(blank=True)

    created = models.DateTimeField(auto_now_add=True)
    
    def admin_thumbnail(self):
        return '<img style="box-shadow: 1px 1px 2px #333; border:medium solid white;" '
        'src="%s" height="80"/>' % (self.file.url)
    admin_thumbnail.allow_tags = True
    admin_thumbnail.short_description = "Thumbnail"
    
    def admin_url(self):
        return "http://" + Site.objects.get_current().domain + self.file.url
    admin_thumbnail.allow_tags = True
    admin_url.short_description = "URL"
