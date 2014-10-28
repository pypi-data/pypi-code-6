from distutils.core import setup
setup(
	name = 'SYTAD',
	packages = ['SYTAD'],
	version = '0.1.3',
	description = 'Provides a simple terminal/scripting interface for downloading audio from YouTube via pafy. Works on Android through QPython.',
	author = 'Johnny Hansen',
	author_email = 'johnnyredzin@gmail.com',
	url = 'https://github.com/redzin/SimpleYouTubeAudioDownloader', 
	download_url = 'https://github.com/redzin/SimpleYouTubeAudioDownloader/tarball/master',
	keywords = ['youtube', 'download', 'audio', 'pafy', 'android'],
	classifiers=[
		"Operating System :: Microsoft",
		"Operating System :: Microsoft :: Windows :: Windows 7",
		"Operating System :: Microsoft :: Windows :: Windows XP",
		"Operating System :: Microsoft :: Windows :: Windows Vista",
		"Operating System :: Android",
		"Programming Language :: Python",
		"Programming Language :: Python :: 3",
		"Programming Language :: Python :: 3.2",
		"Programming Language :: Python :: 3.3",
		"Programming Language :: Python :: 3.4",
		"Intended Audience :: Developers",
		"Intended Audience :: End Users/Desktop",
		"Topic :: Multimedia :: Sound/Audio :: Capture/Recording",
		"Topic :: Utilities",
		"Topic :: Multimedia :: Video",
		"Topic :: Internet :: WWW/HTTP"]
)