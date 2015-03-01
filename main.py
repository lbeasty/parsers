# -*- coding: utf-8 -*-
import ConfigParser
import lxml.html as html
import HTML
import datetime
import os.path
import smtplib

from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#from email.utils import COMMASPACE, formatdate
#from pandas import DataFrame
from time import gmtime, strftime

Config = ConfigParser.ConfigParser()

def send_email(user, pswd, from_, to_, subject, text):
    msg = MIMEMultipart()
    msg.preamble = 'This is a multi-part message in MIME format.\n'
    msg.epilogue = ''
    
    body = MIMEMultipart('alternative')
    body.attach(MIMEText("Some results"))
    
    body.attach(MIMEText(text, 'html'))
    msg.attach(body)

    msg.add_header('From', from_)
    msg.add_header('To', to_)
    #msg.add_header('Cc', ccaddy)    #doesn't work apparently
    #msg.add_header('Bcc', bccaddy)  #doesn't work apparently
    msg.add_header('Subject', subject)
    msg.add_header('Reply-To', from_)
    #msg.add_header('Content-Type', "text/html; charset=utf-8")

    try:
        #server = smtplib.SMTP(SERVER) 
        server = smtplib.SMTP('smtp.gmail.com', 587) #SMTP("localhost", 50) #or port 465 doesn't seem to work!
        server.set_debuglevel(True)
        server.ehlo()
        server.starttls()
        server.login(user, pswd)
        server.sendmail(from_, to_, msg.as_string())
        server.quit()
        #server.close()
        print 'successfully sent the mail'
    except:
        print "failed to send mail"

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

def ReadConfig(config, template):
    Config.read(config)
    addresses = []
    email_list = []
    for i in range(len(Config.sections())):
        if template in Config.sections()[i]:
            for k, v in ConfigSectionMap(Config.sections()[i]).items():
                if Config.sections()[i][-1] != "/" and v[0] != "/":
                    v = "/" + v
                addresses.append(Config.sections()[i] + v)      
        if "mail" in Config.sections()[i]:
            for k, v in ConfigSectionMap(Config.sections()[i]).items():
                email_list.append(v)
    
    return addresses, email_list


begin = """<html>
  <head>
    <meta charset=UTF-8">
    <title>Opinions</title>
  </head>
  <body>
"""
#<meta http-equiv="Content-Type" content="text/html;charset=ISO-8859-1">

end = """
  </body>
</html>
"""

username = "sashaslenastestserver@gmail.com"
passwd = "SashasLenasPassword" 
