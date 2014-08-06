from django.contrib.staticfiles.management.commands.collectstatic import Command as OrigCommand
from django.conf import settings

class Command(OrigCommand):
    def copy_file(self, path, prefixed_path, source_storage):
        '''
        Mostly copied from OrigCommand's inherited, except don't
        attempt to resolve absolute path as the pexstaticfiles
        storage is not capable of that
        '''
        if prefixed_path in self.copied_files:
            return self.log("Skipping '%s' (already copied earlier)" % path)
        # The full path of the source file
        source_path = source_storage.path(path)
        # Finally start copying
        if self.dry_run:
            self.log("Pretending to copy '%s'" % source_path, level=1)
        else:
            self.log("Copying '%s'" % source_path, level=1)
            with source_storage.open(path) as source_file:
                self.storage.save(prefixed_path, source_file)
        if not prefixed_path in self.copied_files:
            self.copied_files.append(prefixed_path)
