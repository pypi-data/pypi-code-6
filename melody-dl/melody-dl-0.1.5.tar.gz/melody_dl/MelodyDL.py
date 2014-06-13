import os
import logging

from extractor import generate_extractors
from FileDownloader.FileDownloader import FileDownloader
from mutagen.mp3 import MP3
from mutagen.id3 import TIT2
from mutagen.easyid3 import EasyID3

from melody_dl import utils



class MelodyDL():
    def __init__(self, url, progress_callback=None, base_dir=None,
                template=None, log=logging.INFO):
        self.url = url
        self.progress_callback = progress_callback
        self.template = template
        self.base_dir = utils.get_best_path(base_dir)

        self.info_extractors = generate_extractors()
        self.logger = self._init_logging(log)


    def extract(self):
        info_extractor = self._get_related_info_extractor()
        return info_extractor.extract(self.url)


    def download(self):
        result = self.extract()
        self.logger.debug("Extraction Result: %s", result)
        return self._download_all_tracks(result)


    ###
    ### Private
    ###


    def _init_logging(self, log):
        logging.basicConfig()

        logger = logging.getLogger(__name__)
        logger.setLevel(log)

        return logger


    def _get_related_info_extractor(self):
        for info_extractor in self.info_extractors:
            if info_extractor.verify_url(self.url):
                return info_extractor


    def _download_all_tracks(self, results):
        """ Download all tracks with the given results dict """

        for track in results['tracks']:
            self._download_track(track)


    def _download_track(self, track):
        """ Download a single track with the given url """

        file_downloader = FileDownloader()
        path = self._build_track_full_path(track)

        self.logger.info("Downloading %s", track['title'])

        is_downloaded = file_downloader.download(track['url'], path,
                self.progress_callback)

        if is_downloaded:
            self._write_id3(path, track)


    def _write_id3(self, path, track):
        self.logger.info("Start encoding..")

        audio = MP3(path)
        audio["TIT2"] = TIT2(encoding=3, text=["title"])
        audio.save()

        audio = EasyID3(path)
        audio["title"] = track['title']
        audio["artist"] = track['artist']
        audio["album"] = track['album']
        audio.save()

        self.logger.info("Finished encoding..")


    def _build_track_full_path(self, track):
        """
        Build a full path based on the base_dir and track template
        """

        template_path = self._template_to_path(self.template, track)
        return os.path.join(self.base_dir, template_path)


    def _template_to_path(self, template, track):
        """ Convert a given template string to a full path """

        self.logger.info("Building path from template")

        if template:
            path = template

            path = path.replace("%{artist}", track['artist'])
            path = path.replace("%{album}", track['album'])
            path = path.replace("%{track}", track['track'])
            path = path.replace("%{title}", track['title'])
            path = "{0}/{1}.{2}".format(self.base_dir, path, track['type'])

        else:
            path = ""

        return path




# mdl = MusicDL()


# mdl = MusicDL("music.com/artist")
# mdl = MusicDL(url="music.com/artist", full_album=True, template="%{artist}",
#               art=True, base_dir=None)

# mdl.extract()
# mdl.extract(artist=True, album=True, tracks=True, art=True)

# mdl.download()
# mdl.download(callback=None, tracks="1..10", )
