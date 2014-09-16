# -*- coding: utf-8 -*-

INSTANCE_PATH       = '/'.join(INSTANCE_HOME.split('/')[:-2])
THUMBNAIL_HOME      = INSTANCE_PATH + '/var/thumbnails'
TMP_FOLDER_LOCATION = INSTANCE_PATH + "/var/tmp"
LISTING_THUMBNAIL_SUFFIX         = ['48x48', '_listing.png']
THUMBNAIL_SUFFIX         = ['128x192', '.png']
#LARGE_THUMBNAIL_SUFFIX   = ['512x768', '_large.png']
LARGE_THUMBNAIL_SUFFIX   = ['458x687', '_large.png']

CONVERTABLE_DOCTYPES = ['doc','docx', 'dot', 'xls', 'xlsx', 'ppt', 'pptx','ppa', 'pps', 'xlb', 'xlt',
                        'odt','odp', 'odc','odg','otp','odm','ott','oth','ods',
                        'sdt','sdp', 'sdc',
                        'sxt','sxp', 'sxc','sxd',
                        'txt', 'csv', 
                        'py', 'php', 'js','json'
                        'htm', 'html','rtf','xml',
                        'psd',
                        'pgp',
                        ]
      
HTML_TMPL           = """
<!DOCTYPE html PUBLIC
  "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html>
    <head>
        <title>%s</title>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    </head>
    <body>
        <h1>%s</h1>
        <div><b>%s</b></div>
        <div id="content">%s</div>
    </body>
</html>
"""


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
