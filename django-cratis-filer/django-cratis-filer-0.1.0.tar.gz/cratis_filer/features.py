from cratis.features import Feature
from cratis_cms.features import Cms


class Filer(Feature):
    """
    Pillow installation

    sudo apt-get install python-dev libjpeg-dev libfreetype6-dev zlib1g-dev

    $ sudo ln -s /usr/lib/`uname -i`-linux-gnu/libfreetype.so /usr/lib/
    $ sudo ln -s /usr/lib/`uname -i`-linux-gnu/libjpeg.so /usr/lib/
    $ sudo ln -s /usr/lib/`uname -i`-linux-gnu/libz.so /usr/lib/
    """

    def configure_settings(self):

        self.append_apps([
            'easy_thumbnails',
            'filer',
            'mptt'
        ])

        self.settings.THUMBNAIL_PROCESSORS = (
            'easy_thumbnails.processors.colorspace',
            'easy_thumbnails.processors.autocrop',
            #'easy_thumbnails.processors.scale_and_crop',
            'filer.thumbnail_processors.scale_and_crop_with_subject_location',
            'easy_thumbnails.processors.filters',
        )

        self.settings.THUMBNAIL_FORMAT = 'PNG'

        self.settings.FILER_DEBUG = self.settings.DEBUG

        self.settings.SOUTH_MIGRATION_MODULES = {
            'easy_thumbnails': 'easy_thumbnails.south_migrations',
        }



class FilerCms(Feature):

    def get_required(self):
        return [Filer, Cms]

    def configure_settings(self):

        self.append_apps([
            'cmsplugin_filer_file',
            'cmsplugin_filer_folder',
            'cmsplugin_filer_image',
            'cmsplugin_filer_teaser',
            'cmsplugin_filer_video',
        ])