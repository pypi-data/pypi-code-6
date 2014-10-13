import os

ROOT = 'artister'

def getArtists():
    return dict(enumerate(os.listdir(ROOT)))

def getAlbums(parent):
    return dict(enumerate(os.listdir(os.path.join(ROOT, parent))))