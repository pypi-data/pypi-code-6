import sys

from setuptools import setup, find_packages

setup(
    name='music-score-creator',
    version='0.7',
    description="Music score creator. Generate a music score from an audio.",
    long_description=open('README.srt').read(),
    author = 'Jose Carlos Montanez Aragon',
    author_email = 'jose90clari@gmail.com',
    license='GPLv3',
    packages=['music_score_creator'],
    data_files=[('music_score_creator/images', ['music_score_creator/images/open32.png', 'music_score_creator/images/pdf32.png', 'music_score_creator/images/play32.png', 'music_score_creator/images/record32.png', 'music_score_creator/images/save32.png']),
                ('music_score_creator', ['music_score_creator/sound.py'])],
    scripts=['music_score_creator/music-score-creator.py'],
    url='https://github.com/Montagon/A-music-score-creator',
    download_url = 'https://github.com/Montagon/A-music-score-creator/releases/tag/v0.6-beta',
    include_package_data=True,
    #install_requires=[
       #'pyaudio',
       #'numpy',
       #'scipy',
       #'matplotlib',
       #'lilypond'
    #],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: X11 Applications',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX',
        'Topic :: Multimedia :: Sound/Audio :: Capture/Recording',
        'Topic :: Scientific/Engineering',
        'Topic :: Utilities'
        ],
    keywords = ['music', 'creator', 'music score', 'audio'],
)