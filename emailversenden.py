import configparser
import smtplib
config = configparser.ConfigParser()
config.read("configfile.txt")
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = config["email"]["meinemail"]
SMTP_PASSWORD = "Meiler12"
EMAIL_FROM = config["email"]["meinemail"]
EMAIL_TO = config["email"]["meinemail"]
EMAIL_SUBJECT = "Attention:Subject here"
EMAIL_MESSAGE = "The message here"

s = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
s.starttls()
s.login(SMTP_USERNAME, SMTP_PASSWORD)
message = 'Subject: {}\n\n{}'.format(EMAIL_SUBJECT, EMAIL_MESSAGE)
s.sendmail(EMAIL_FROM, EMAIL_TO, message)
s.quit()
