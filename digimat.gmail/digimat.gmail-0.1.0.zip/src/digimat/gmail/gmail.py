
import StringIO
import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEImage import MIMEImage
import sys, traceback

#require pil
import Image


class GoogleMail:
    def __init__(self, user, password, debugLevel=0):
        self._user=user
        self._password=password
        self._server=None
        self._debugLevel=debugLevel
        self.reset()

    def reset(self):
        self._recipients=[]
        self._attach=[]
        self._cid=0
        self._html=''
        self._style=''
        self.createMessage()

    def connect(self):
        try:
            self._server=smtplib.SMTP('smtp.gmail.com:587')
            if self._debugLevel:
                self._server.set_debuglevel(self._debugLevel)
            self._server.starttls()
            self._server.login(self._user, self._password)
            return True
        except:
            traceback.print_exc(file=sys.stdout)
            self._server=None

    def disconnect(self):
        try:
            self.server.quit()
        except:
            pass
        self._server=None

    def getCID(self):
        self._cid+=1
        return 'cdi-{0}'.format(self._cid)

    def attach(self, obj):
        self._attach.append(obj)

    def createMessage(self, subject=None):
        self._message=MIMEMultipart(_subtype='related')
        if subject:
            self.setSubject(subject)

    def setSubject(self, subject):
        self._message['Subject']=subject

    def writeStyle(self, style):
        self._style = self._style + style

    def writeHtml(self, html):
        self._html = self._html + html

    def imageToHtmlSnipet(self, image, format='PNG'):
        if image:
            buf=StringIO.StringIO()
            image.save(buf, format)
            obj=MIMEImage(buf.getvalue(), image.format)
            buf.close()

            cid=self.getCID()
            obj.add_header('Content-Id', '<{0}>'.format(cid))
            self.attach(obj)
            return "<img src='cid:{0}'/>".format(cid)
        return ''

    def addRecipient(self, address):
        if address:
            if type(address)==type(''):
                address=address.split(',')
            for a in address:
                if not a in self._recipients:
                    self._recipients.append(a)

    def getHtml(self):
        html="<head>"
        if self._style:
            html += "<style type='text/css'>" + self._style + "</style>"
        html += "</head>"
        html += "<body>" + self._html + "</body>"
        return html

    def send(self, recipients=None):
        result=False
        self.addRecipient(recipients)
        if self._recipients:
            if self.connect():
                originator='Digimat'
                self._message['From']=originator
                self._message['To']=', '.join(self._recipients)

                self._message.attach(MIMEText(self.getHtml(), _subtype='html'))

                if self._attach:
                    for obj in self._attach:
                        self._message.attach(obj)

                try:
                    self._server.sendmail(originator, self._recipients, self._message.as_string())
                    result=True
                except:
                    traceback.print_exc(file=sys.stdout)
                    pass

                self.disconnect()

        return result


if __name__ == "__main__":
    # gm=GoogleMail('xxxx', 'xxxx')
    # gm.setSubject('test')
    # gm.writeHtml('test')
    # gm.send('joe@xxx.com')
    pass






