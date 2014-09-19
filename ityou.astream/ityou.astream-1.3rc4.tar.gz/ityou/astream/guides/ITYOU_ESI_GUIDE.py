# -*- coding: utf-8 -*-

# ESI GUIDED TOUR --------------------------
# from ityou.esi.theme.guide import GUIDE
# -------------------------------------------

#        'content': \
#u"""Das ist ein schöner Text  mit mehreren 
#Zeilen
#und so weiter
#""",


# ------------------------------------------------------------------------------
#
# step naming convention: http://bootstraptour.com/api/
#
# step = {
#   'element'   : ...,
#   'title'     : ...,
#   'content'   : ...,
#   'placement' : ...
# }
#
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Activity Stream
#

step_1 =  { 
        'element'   : '#personal-tools',
        'title'     : u'Persönliche Werkzeuge',
        'content'   : u'Hier finden Sie Verweise zu Ihren wichtigsten Seiten (Profil etc.).',
        'placement' : 'bottom'
    }

step_2 =  { 
        'element'   : '#notify-messages',
        'title'     : u'Persönliche Mitteilungen',
        'content'   : u'Erfahren Sie in Echtzeit sobald Ihnen jemanden eine neue Mitteilungen geschrieben hat.',
        'placement' : 'bottom'
    }
    
step_3 =  { 
        'element'   : '#notify-activities',
        'title'     : u'Letzte Aktivitäten',
        'content'   : u'Sobald jemand ein Dokument erstellt oder bearbeitet hat werden Sie in Echtzeit darüber informiert.',
        'placement' : 'bottom'
    }
    
step_4 =  { 
        'element'   : '#new-content',
        'title'     : u'Neuen Inhalt bereitstellen',
        'content'   : u'Erstellen Sie mit geringstem Aufwand neuen Inhalt und teilen diesen bei Bedarf mit den anderen Benutzer.',
        'placement' : 'bottom'
    }

step_5 =  { 
        'element'   : '#astream-tabs',
        'title'     : u'Auswahl letzter Aktivitäten',
        'content'   : u'Wechseln Sie zwischen den letzten Aktivitäten aller Benutzer oder denen Ihrer Favoriten.',
        'placement' : 'bottom'
    }


ACTIVITY = [ step_1, step_2, step_3, step_4, step_5 ]



GUIDE = {
    'activities' : ACTIVITY
}
