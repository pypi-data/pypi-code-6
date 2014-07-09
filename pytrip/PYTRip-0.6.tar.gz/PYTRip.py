import pafy
from pydub import AudioSegment
from bs4 import BeautifulSoup
import urllib2
import os

def downloadToMP3(url, folder, subfolder=""):
    video = pafy.new(url)
    best = video.getbest()
    folder = folder+subfolder
    if not os.path.exists(folder):
        os.makedirs(folder)

    path = folder+best.title+"."+best.extension
    brackets = [best.title.find('('), best.title.find('[')]
    
    artist = best.title[:(best.title.find(' -'))]
    song = best.title[(best.title.find('- '))+2:min(brackets)]
    best.download(filepath=path, quiet=False)
    vidFile = AudioSegment.from_file(path, best.extension)
    vidFile.export(folder+best.title+".mp3", format="mp3", tags={'artist': artist, 'title': song})
    os.remove(path)

def downloadPlaylist(url, folder):
    soup = BeautifulSoup(urllib2.urlopen(url))
    tracks = soup.findAll("li", {"class":"yt-uix-scroller-scroll-unit"})
    title = soup.find("h3", {"class":"playlist-title"}).text.rstrip('\n') + "/"
    print(title)
    
    for track in tracks:
        vidURL = "http://www.youtube.com/watch?v="+track['data-video-id']
        downloadToMP3(vidURL, folder, subfolder=title)

def downloadSong(artist, song, folder):
    artistRep = artist.replace(' ', '+')
    songRep = song.replace(' ', '+')
    query = artistRep + "+-+" + songRep
    url = "http://www.youtube.com/results?search_query="+query+"&filters=video"
    soup = BeautifulSoup(urllib2.urlopen(url))
    results = soup.find("ol", {"class":"item-section"})
    result = results.find("li")
    data = result.find("h3", {"class":"yt-lockup-title"})
    songURL = "http://www.youtube.com" + data.find("a")['href']
    print(songURL)
    downloadToMP3(songURL, folder)
    
def downloadTop(artist, folder, number=5):
    artistRep = artist.replace(' ','+')
    url = "http://www.youtube.com/results?search_query="+artistRep+"&filters=video"
    soup = BeautifulSoup(urllib2.urlopen(url))
    results = (soup.find("ol", {"class":"item-section"})).findAll("li", recursive=False)
    trackNum = 1
    for result in results:
        if trackNum > number:
            break
        data = result.find("h3", {"class":"yt-lockup-title"})
        songURL = "http://www.youtube.com" + data.find("a")['href']
        downloadToMP3(songURL, folder)
        trackNum += 1
    
