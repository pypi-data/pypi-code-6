def send_email(message_to_be_send):
    """Send mail using SMTP"""
    msg = MIMEText(message_to_be_send)
    msg['Subject'] = EMAIL_SUBJECT
    msg['To'] = EMAIL_TO
    msg['From'] = EMAIL_FROM
    mail = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    mail.starttls()
    mail.login(SMTP_USERNAME, SMTP_PASSWORD)
    mail.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())
    mail.quit()
url_ceyrek = "http://api.piyasa.com/json/?kaynak=metal_arsiv_ay_alti_CYR" #API for ceyrek
url_gram = "http://api.piyasa.com/json/?kaynak=metal_arsiv_ay_alti_GRM" #API for gram

if __name__ == '__main__':
    sys.exit(main())
