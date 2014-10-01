import os


class Cache:

    def __init__(self, location):
        self.location = location

    @classmethod
    def in_default_location(cls):
        return Cache("/tmp")

    def get(self, dist):

        artifact_location = os.path.join(self.location, dist.get_filename())

        if not os.path.isfile(artifact_location) or "SNAPSHOT" in dist.get_filename():
            dist.download(self.location)
        else:
            print "File %s is already cached." % dist.get_filename()

        return artifact_location