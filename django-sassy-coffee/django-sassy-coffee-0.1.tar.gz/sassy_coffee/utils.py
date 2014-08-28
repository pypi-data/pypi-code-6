from django.conf import settings
import os, fnmatch, codecs

def locate_files_to_compile(format, exclusions=list()):
    matches = list()
    for root, dirnames, filenames in os.walk(settings.STATIC_ROOT):
        for filename in fnmatch.filter(filenames, format):
            base = os.path.splitext(filename)[0]
            if not filename in exclusions and not base in exclusions:
                matches.append((root, os.path.join(root, filename), base))
    return matches

def write_to_file(format, name, path, content):
    if not os.path.exists(os.path.join(os.path.dirname(path), format)):
        os.mkdir(os.path.join(os.path.dirname(path), format))
    dest_f = codecs.open(os.path.join(os.path.dirname(path), '{0}/{1}.{0}'.format(format, name)), mode='w', encoding='utf-8')
    dest_f.write(content)
    dest_f.close()