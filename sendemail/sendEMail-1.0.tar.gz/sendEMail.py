import smtplib
import string

def dic_to_str(dic):
	st = ""
	for key in dic.keys():
		st += str(key) + " : " + str(dic[key]) + "\n"
	return st

def send_error_mail(HOST, username, password, FROM, TO, SUBJECT, dic):
	try:
		text = dic_to_str(dic)

		BODY = string.join((
			"From: %s" % FROM,
			"To: %s" % TO,
			"Subject: %s" % SUBJECT ,
			"",
			text
			), "\r\n")

		server = smtplib.SMTP(HOST)
		server.starttls()
		server.login(username,password)
		server.sendmail(FROM, [TO], BODY)
		server.quit()
	except:
		print "Erreur lors de l envoie du mail d erreur ... ca craint ..."
