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
# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Start
#

step_s_1 = { 
    'element': '#username',
    'title': u'Benutzername',
    'content': u'Hier sehen Sie Ihren Benutzernamen. Wenn Sie Ihren Benutzernamen anklicken, kommen Sie auf Ihr Profil.',
    'placement': 'bottom'
}

step_s_2 = { 
    'element': '#logout',
    'title': u'Abmelden',
    'content': u'Klicken Sie auf diesen Link, wenn Sie sich ausloggen wollen.',
    'placement': 'bottom'
}

step_s_3 = {
    'element': '#btn-imessage',
    'title': u'Dialog Übersicht',
    'content': u'Über dieses Symbol gelangen Sie zu einer Übersicht der Dialoge in denen Sie Mitglied sind. Dies betrifft Einzeldialoge zwischen Ihnen und einem anderen Benutzer, sowie Dialoge an denen mehrere Personen teilnehmen',
    'placement': 'top'
}

step_s_4 = {
    'element': '#btn-Members',
    'title': u'Übersicht registrierter Benutzer',
    'content': u'Über dieses Symbol gelangen Sie zu einer Übersicht der registrierten Benutzer. Dort können Sie u.a. auch direkt nach Benutzern suchen.',
    'placement': 'top'
}

step_s_5 = {
    'element': '#btn-myprofile',
    'title': u'Ihr eigenes Profil',
    'content': u'Über dieses Symbol gelangen Sie zu Ihrem eigenen Profil. Dort können Sie alle persönlichen Daten ändern und ein Bild hochladen.',
    'placement': 'top'
}

step_s_6 = {
    'element': '#btn-mystuff',
    'title': u'Übersicht vorhandener Dokumente',
    'content': u'Über dieses Symbol gelangen Sie zu einer Übersicht über hochgeladene/erstellte Dokumente.',
    'placement': 'top'
}


START = [ step_s_1, step_s_2, step_s_3, step_s_4, step_s_5, step_s_6, ]

# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Messaging System
#


step_ms_1 = {
    'element': '#group-member-content',
    'title': u'Dialogteilnehmer',
    'content': u'Hier können Sie sehen mit wem Sie sich gerade unterhalten. Sie können sich entweder in einem Einzeldialog befinden oder sich mit mehreren Nutzern gleichzeitig unterhalten.',
    'placement': 'bottom'
}

step_ms_2 = {
    'element': '#message-textarea',
    'title': u'Nachricht verfassen',
    'content': u'In diesem Textfeld können Sie Ihre Nachricht verfassen.',
    'placement': 'top'
}

step_ms_3 = {
    'element': '#receiver_list',
    'title': u'Empfänger',
    'content': u'Hier sehen Sie die Personen, die Sie als Empfänger Ihrer Nachricht ausgewählt haben.',
    'placement': 'bottom'
}

step_ms_4 = {
    'element': '#w_user_name',
    'title': u'Empfängerauswahl',
    'content': u'Über dieses Textfeld können Sie nach Empfängern Ihrer Nachricht suchen. Geben Sie einfach Bruchstücke des Namens ein und Sie erhalten automatisch Vorschläge.',
    'placement': 'bottom'
}



DIALOG = [ step_ms_1, step_ms_2 ]

MESSAGE = [ step_ms_3, step_ms_4 ]

# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Member Overview
#

step_mem_1 =  { 
    'element': '#user-table',
    'title': u'Übersicht registrierter Benutzer',
    'content': u'In dieser Tabelle können Sie alle registrierten Benutzer sehen.',
    'placement': 'top'
}

step_mem_2 =  { 
    'element': '#user-table_filter',
    'title': u'Benutzer suchen',
    'content': u'Möchten Sie nach einem Benutzer suchen, geben Sie hier einfach einige Buchstaben des Namens ein und Sie erhalten Resultate Ihrer Suche.',
    'placement': 'bottom'
}
    

MEMBER = [ step_mem_1, step_mem_2, ]

# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Userprofile
#

step_profile_1 =  { 
    'element': '#portrait',
    'title': u'Benutzerportrait',
    'content': u'Hier sehen Sie das Portrait eines Benutzers. In Ihrem eigenen Profil können Sie durch daraufklicken ein neues Bild hochladen.',
    'placement': 'top'
}

step_profile_2 =  { 
    'element': '#firstname',
    'title': u'Benutzerinformationen',
    'content': u'Diese Zeilen stellen alle angegebenen Informationen eines Benutzers dar. In Ihrem eigenen Profil können Sie durch den Klick auf eine Zeile, diese dann bearbeiten.',
    'placement': 'top'
}

step_profile_3 =  { 
    'element': '#user-activity-wrapper',
    'title': u'Benutzeraktivitäten',
    'content': u'Sofern der Benutzer Dokumente im System eingepflegt hat, können Sie dies unterhalb seines Profils sehen.',
    'placement': 'top'
}



PROFILE = [ step_profile_1, step_profile_2, step_profile_3, ]

# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Activity Stream
#

step_4_1 =  { 
        'element': '#username',
        'title': u'Das ist ein Dummy-Titel mit Umlauten öäü',
        'content': \
u"""Das ist ein schöner Text  mit mehreren 
Zeilen
und so weiter
""",
        'placement': 'bottom'
    }

step_4_2 =  { 
        'element': '#logout',
        'title': u'Das ist ein Dummy-Titel mit Umlauten öäü',
        'content': u'Das ist ein schöner Text...',
        'placement': 'bottom'
    }

ACTIVITY = [ step_4_1, step_4_2, ]

# ------------------------------------------------------------------------------


# ------------------------------------------------------------------------------
# Documents
#

step_doc_1 =  { 
        'element': '.documents-abstracts',
        'title': u'Über ASCO Beiträge diskutieren',
        'content': \
u"""Hier können Sie mit Kollegen und Kolleginnen über ASCO 
Beiträge diskutieren.
""",
        'placement': 'bottom'
    }

DOCUMENTS = [ step_doc_1, ]

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Abstract listing
#

step_al_1 =  { 
        'element': '#abstract_number',
        'title': u'Abstract Nummer eintragen',
        'content': \
u"""Bitte tragen Sie hier die Nummer des Abstract ein. Der Beitrag wird Ihnen 
anschließend angezeigt
""",
        'placement': 'bottom'
    }

ABSTRACTS = [ step_al_1, ]

# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Abstract
#

step_a_1 =  { 
        'element': '#abstract_number',
        'title': u'Abstract Nummer eintragen',
        'content': \
u"""Bitte tragen Sie hier die Nummer des Abstract ein. Der Beitrag wird Ihnen 
anschließend angezeigt
""",
        'placement': 'bottom'
    }

ABSTRACT = [ step_a_1, ]

# ------------------------------------------------------------------------------


GUIDE = {
    'start'             : START,
    'dialog'            : DIALOG,
    'message'           : MESSAGE,
    'member'            : MEMBER,
    'profile'           : PROFILE,
    'documents'         : DOCUMENTS,
    'abstracts'         : ABSTRACTS,
    'abstract'          : ABSTRACT,
}
