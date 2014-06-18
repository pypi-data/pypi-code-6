#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
pySendMail - Fabrice Romand <fabrom AT jability.org> - release under GPL
goal: sending mail from standard input
usage: %s [-dhq] [-f <from>] [-t <to>] [-s <subject>]
               [-S <smtp host>]
               [-F <files list>] [-z <archive name>]
               [-c <charset>]
               [<file]
-h, --help    Display this help message
-d, --debug   Display debug info.
-q, --quiet   Silent mode
-f, --from    Sender email address
-t, --to      Person addressed emails list (comma sep.)
-s, --subject Subject
-F, --files   Attachments list (comma sep.)
-z, --zip     Zip attachments into archive before sending it
-S, --smtphost SMTP host (default=localhost)
-c, --charset Charset unicode à utiliser (utf-8 par défaut)

Retourne :
0 si ok, email envoyé
1 Si email envoyé mais certaines PJ non trouvées
2 Email non envoyé : erreur durant communication SMTP
3 Email non envoyé : erreur inconnue
9 si option incorrecte
"""


__author__ = "Fabrice Romand"
__copyright__ = "Copyleft 2008, Fabrice Romand"
__credits__ = [ "Fabrice Romand" ]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Fabrice Romand"
__email__ = "fabrom@jability.org"
__status__ = "Development"

_debug=False

from email import Encoders
from email.Header import Header
from email.MIMEBase import MIMEBase
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.Utils import COMMASPACE, formatdate
import getopt
import locale
import os.path
import platform
import smtplib
import sys
import traceback


def send(mfrom, mto, msubject, mbody, files=[],
         msmtpserver='localhost',
         charset='UTF-8',
         zip=False, zipFilename="archive.zip"):
    """
    Envoi effectif du mail par SMTP
    > mfrom: adresse de l'expéditeur
    > mto: liste des adresses des destinataires
    > msubject: objet du message
    > mbody: Corps du message (string)
    > files: Liste de pièces jointes
    > msmtpserver: IP ou nom du serveur SMTP
    > charset: code du charset à utiliser pour l'encodage du mail
    > zip: Vrai si les PJ doivent être zippées avant envoi
    > zipFilename: Nom de l'archive zip
    < code de retour :  O=ok,
                        1=warning (PJ pas trouvée),
                        2=Erreur (communication avec le serveur SMTP)
                        3=Erreur (inconnue)
    """

    ressend=0

    try:

        # On prépare le message
        email = MIMEMultipart()
        email['From']=mfrom.encode('ascii')
        email['To']=COMMASPACE.join(mto)
        email['Subject']=str(Header(msubject, charset))
        email['Date'] = formatdate(localtime=True)

        # On attache le texte du message
        email.attach(MIMEText(mbody.encode(charset), 'plain', charset))

        # Puis les éventuels pièces jointes
        if len(files)>0:
            # Faut-il zipper les PJ?
            if zip:
                import zipfile
                zipFile=zipfile.ZipFile(zipFilename, 'w')
                zipok=False
                for file in files:
                    if not os.path.exists(file):
                        ressend=1
                        print >>sys.stderr, \
                            u"Attachment '%s' not found !" % (file)
                        continue
                    # FIXME: Les noms de fichiers zippés avec accent sont mal
                    # encodés
                    zipFile.write(file,file.encode('cp437'))
                    zipok=True
                zipFile.close()
                if zipok:
                    files=[zipFilename]
                else:
                    files=[]
            # On ajoute les PJ
            for file in files:
                if not os.path.exists(file):
                    ressend=1
                    print >>sys.stderr, u"Attachment '%s' not found !" % (file)
                    continue
                part = MIMEBase('application', "octet-stream")
                part.set_payload(open(file, "rb").read())
                Encoders.encode_base64(part)
                part.add_header('Content-Disposition',
                                'attachment; filename="%s"' \
                                % os.path.basename(file.encode(charset)))
                email.attach(part)

        # On envoie le tout par SMTP...
        try:
            server = smtplib.SMTP(msmtpserver)
            server.sendmail(mfrom,
                            mto,
                            email.as_string())
            server.quit()
        except:
            ressend=2
            if _debug:
                raise
            return ressend

        # On fait le ménage
        if zip:
            os.remove(zipFilename)

    except:
        ressend=3
        if _debug:
            raise

    return ressend


def usage(name):
    """Affichage du mode d'emploi"""
    print >>sys.stderr, "pySendMail %s - Fabrice Romand "  % (__version__) + \
            "<fabrom AT jability.org> - release under GPL"
    print >>sys.stderr, "goal: sending mail from standard input"
    print >>sys.stderr, "usage: %s [-dhq] [-f <from>] [-t <to>] " % name  + \
            "[-s <subject>] [-S <smtp host>] [-F <attachments list>] " + \
            "[-c <charset>] [-z <archive name>] [< file]"
    print >>sys.stderr, '\t-f, --from\t\tSender email address'
    print >>sys.stderr, '\t-t, --to\t\tPerson addressed emails list ' + \
            '(comma sep.)'
    print >>sys.stderr, '\t-s, --subject\t\tSubject'
    print >>sys.stderr, '\t-F, --files\t\tAttachments list (comma sep.)'
    print >>sys.stderr, '\t-z, --zip\t\tzip all attachments in an archive'
    print >>sys.stderr, '\t-S, --smtphost\t\tSMTP host (default=localhost)'
    print >>sys.stderr, "\t-c, --charset\t\tcharset to encode email " + \
            "(utf-8 by default)"
    print >>sys.stderr, '\t-h, --help\t\tDisplay this help message'
    print >>sys.stderr, '\t-d, --debug\t\tDisplay debug info.'
    print >>sys.stderr, '\t-q, --quiet\t\tSilent mode'


if __name__ == '__main__':

    # Parsing et contrôle des options
    try:
        opts, args = getopt.getopt (sys.argv[1:], "c:df:F:hqs:S:t:z:",
                                    ["charset=", "help", "debug", "from=",
                                     "files=", "to=", "subject=", "smtphost=",
                                     "quiet", "zip="])
    except getopt.GetoptError:
        usage(sys.argv[0])
        sys.exit(9)

    # initialisation des composants du mail
    mfrom=u""
    mto=u""
    files=u""
    msubject=u""
    msmtphost=""
    charset="UTF-8"
    zip=False
    zipFilename="archive.zip"
    quiet=False

    dftlocale=locale.getdefaultlocale()[1]

    for o, a in opts:
        if o in ('-h', '--help'):
            usage(sys.argv[0])
            sys.exit(1)
        if o in  ('-d', '--debug'):
            _debug=True
        if o in ('-f', '--from'):
            mfrom = unicode(a,dftlocale)
        elif o in ('-t', '--to'):
            mto = unicode(a,dftlocale)
        elif o in ('-s', '--subject'):
            msubject = unicode(a,dftlocale)
        elif o in ('-S', '--smtphost'):
            msmtphost = a
        elif o in ('-F', '--files'):
            files = unicode(a,dftlocale)
        elif o in ('-c', '--charset'):
            charset = a
        elif o in ('-q', '--quiet'):
            quiet=True
            _debug=False
        elif o in ('-z', '--zip'):
            zip=True
            zipFilename = unicode(a,dftlocale)

    # Lecture des éléments manquants
    try:
        # Si l'entrée standard est une console
        # et que l'on n'est pas en mode silence,
        if sys.stdin.isatty() and not quiet:
            # et certain composant absent,
            # demande de saisie à l'utilisateur
            if mfrom==u"":
                mfrom=unicode(raw_input("From: "), dftlocale)
            if mto==u"":
                mto=unicode(raw_input("To: "), dftlocale)
            if msubject==u"":
                msubject=unicode(raw_input("Subject: "), dftlocale)
            if files==u"":
                files=unicode(raw_input("Attachments: "), dftlocale)
            if msmtphost=="":
                msmtphost=raw_input("SMTP host: ")
            if platform.system() == 'Windows':
                helpmsg=u"C-z"
            else:
                helpmsg=u"C-d"
            print >>sys.stdout, u"Body (%s to end): " % (helpmsg)

        # Lecture du corps du message
        lines=sys.stdin.readlines()

    except KeyboardInterrupt:
        sys.exit(0)
    except:
        print >>sys.stderr, u"Cannot read file !"
        if _debug:
            print >>sys.stderr, traceback.print_exc()
        sys.exit(2)

    # Création du corps du message (liste de chaines -> chaine unique)
    mbody=u""
    for line in lines:
        mbody=mbody+unicode(line, dftlocale)

    # parsing de la liste des pièces jointes
    if not files  == "":
        lfiles=files.split(u',')
    else:
        zip=False
        lfiles=[]

    # parsing de la liste des destinataires
    lmto=mto.encode('ascii').split(u',')

    # envoi du mail
    res=send(mfrom, lmto, msubject, mbody, lfiles, msmtphost, charset,
             zip, zipFilename)

    # Affichage du resultat
    if not quiet:
        if res == 0:
            print >>sys.stdout, u"Email send."
        elif res == 1:
            print >>sys.stdout, u"Email send (Warning detected)."
        elif res == 2:
            print >>sys.stderr, u"Email NOT send (SMTP error)"
        else:
            print >>sys.stderr, u"Email NOT send (Error) !"

    sys.exit(res)
