# -*- coding: utf-8 -*-
import ConfigParser

import lxml.html as html
from pandas import DataFrame
import HTML

from time import gmtime, strftime
import datetime
import os.path

import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

def send_email(user, pswd, from_, to_, subject, text):
            #import smtplib
	    print text
            gmail_user = user
            gmail_pwd = pswd
            FROM = from_
            TO = to_ #must be a list
            SUBJECT = subject
            TEXT = text

            txt = "test text"
#            print message

            msg = MIMEMultipart()
            msg.preamble = 'This is a multi-part message in MIME format.\n'
            msg.epilogue = ''

   	    body = MIMEMultipart('alternative')
    	    body.attach(MIMEText(txt))
    
    	    body.attach(MIMEText(text, 'html'))
    	    msg.attach(body)


            msg.add_header('From', from_)
    	    msg.add_header('To', from_)
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
                server.login(gmail_user, gmail_pwd)
                server.sendmail(FROM, TO, msg.as_string())
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



Config = ConfigParser.ConfigParser()
conf = "test3.ini"
Config.read(conf)

address = ConfigSectionMap(Config.sections()[0])['address']
email = ConfigSectionMap(Config.sections()[0])['email']

today = strftime("%d.%m.%Y %H:%M", gmtime())

main_domain_stat = 'http://mosclinic.ru/medcentres'

page = html.parse('%s/%s' % (main_domain_stat, "59"))


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

a = []
b = []
#for el in page.getroot().find_class('noline'):
for el in page.getroot().find_class('margin15 font_arial12 as_a2'):
 link = el.values()[2]
 if "medreview" in link:
    page1 = html.parse('%s' % (link))
    #content = page1.getroot().findall(".//p[@style]")[0].text_content()
    content = page1.getroot().find_class('margin15 font_arial12')[0].text_content()
    #time = page1.getroot().findall(".//span[@style]")
    #imgs = page1.getroot().findall(".//img[@style]")
    dates = page1.getroot().findall(".//meta[@itemprop]")
    for date in dates:
        if date.items()[0][0] == "itemprop" and date.items()[0][1] == "datePublished":
            time = date.items()[1][1]
    a.append(unicode(content).encode("utf-8"))#.encode("ISO-8859-1"))#.decode("utf-8"))
  
    b.append(unicode(time).encode("utf-8"))

print a
print b
table_data = []
#	['date', 'description']]

for i in range(len(a)):
  if os.path.isfile("tmpfile"):
    f = open("tmpfile", "r+")
    lasttime = f.readline()
    if lasttime:
      x1 = b[i].encode("utf-8").split("|")[0].split()[0].split("-")
      x2 = b[i].encode("utf-8").split("|")[1].split()[0].split(":")
      y1 = lasttime.split()[0].split(".")
      y2 = lasttime.split()[1].split(":")
      #months = (u'января', u'февраля', u'марта', u'апреля', u'мая', u'июня', u'июля', u'августа', u'сентября', u'октября', u'ноября', u'декабря')
      #month = next(i for i,name in enumerate(months,1) if name in x1[1].decode("utf-8")) 
      now = datetime.datetime(int(x1[0]), int(x1[1]), int(x1[2]), int(x2[0]), int(x2[0]))
      last = datetime.datetime(int(y1[2]), int(y1[1]), int(y1[0]), int(y2[0]), int(y2[1]))
      if now > last:
        table_data.append([b[i], a[i]])
    else:
      table_data.append([b[i], a[i]])
    f.close()
  else:
    table_data.append([b[i], a[i]])
    
f = open("tmpfile", "w+")
f.write(today)
f.close()

print
print table_data
htmlcode = HTML.table(table_data, header_row = ['date', 'description'])

if len(table_data) > 0:
  newfile = "Opinions_" + main_domain_stat.split("/")[2] + "_".join(today.split()) + ".html"
  f = open(newfile, "w+")
  tmp = begin + htmlcode + end
  f.write(tmp)
  f.close()
   
  
  #send_mail(send_from=email, send_to=[email], subject="Opinion " + today, text="Opinions are in attachments", files=[newfile])
  mailer = smtplib.SMTP('smtp.gmail.com', 587)
  username = "sashaslenastestserver@gmail.com"
  passwd = "SashasLenasPassword"

  send_email(username, passwd, email , [email], "test subject", tmp)


#['__class__', '__contains__', '__copy__', '__deepcopy__', '__delattr__', '__delitem__', '__dict__', '__doc__', '__format__', '__getattribute__', '__getitem__', '__hash__', '__init__', '__iter__', '__len__', '__module__', '__new__', '__nonzero__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_init', '_label__del', '_label__get', '_label__set', 'addnext', 'addprevious', 'append', 'attrib', 'base', 'base_url', 'body', 'clear', 'cssselect', 'drop_tag', 'drop_tree', 'extend', 'find', 'find_class', 'find_rel_links', 'findall', 'findtext', 'forms', 'get', 'get_element_by_id', 'getchildren', 'getiterator', 'getnext', 'getparent', 'getprevious', 'getroottree', 'head', 'index', 'insert', 'items', 'iter', 'iterancestors', 'iterchildren', 'iterdescendants', 'iterfind', 'iterlinks', 'itersiblings', 'itertext', 'keys', 'label', 'make_links_absolute', 'makeelement', 'nsmap', 'prefix', 'remove', 'replace', 'resolve_base_href', 'rewrite_links', 'set', 'sourceline', 'tag', 'tail', 'text', 'text_content', 'values', 'xpath']
  
