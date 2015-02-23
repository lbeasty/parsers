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

def send_mail(send_from, send_to, subject, text, files=None,
              server="127.0.0.1"):
    assert isinstance(send_to, list)

    msg = MIMEMultipart(
        From=send_from,
        To=COMMASPACE.join(send_to),
        Date=formatdate(localtime=True),
        Subject=subject
    )
    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            msg.attach(MIMEApplication(
                fil.read(),
                Content_Disposition='attachment; filename="%s"' % basename(f)
            ))

    smtp = smtplib.SMTP(server)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()

def send_email(user, pswd, from_, to_, subject, text):
            #import smtplib

            gmail_user = user
            gmail_pwd = pswd
            FROM = from_
            TO = to_ #must be a list
            SUBJECT = subject
            TEXT = text

            # Prepare actual message
            message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
            try:
                #server = smtplib.SMTP(SERVER) 
                server = smtplib.SMTP("smtp.gmail.com", 587) #or port 465 doesn't seem to work!
                server.ehlo()
                server.starttls()
                server.login(gmail_user, gmail_pwd)
                server.sendmail(FROM, TO, message)
                #server.quit()
                server.close()
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
conf = "test.ini"
Config.read(conf)

address = ConfigSectionMap(Config.sections()[0])['address']
email = ConfigSectionMap(Config.sections()[0])['email']

today = strftime("%d.%m.%Y %H:%M", gmtime())
#print "today: ", "!" + today + "!"

main_domain_stat = 'http://www.apoi.ru'

page = html.parse('%s/%s' % (main_domain_stat, address))

#print '%s/klinika-evro-med-moskva-pr-kt-mira-3-k-1' % (main_domain_stat)
#print dir(page)
#print 


begin = """<html>
  <head>
    <meta charset="UTF-8">
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
for el in page.getroot().find_class('m_info inf_ml'):
  a.append(el.getchildren()[0].getchildren()[0].text.encode('utf-8'))

e = page.getroot().find_class('m_info inf_ml').pop()


datas = page.getroot().find_class('butt date lf mr5')
for el in datas:
  #print "!" + ' '.join(el.text_content().split()) + "!"
  b.append(unicode(el.text_content(), 'utf-8'))

table_data = []
#	['date', 'description']]

for i in range(len(a)):
  if os.path.isfile("tmpfile"):
    f = open("tmpfile", "r+")
    lasttime = f.readline()
    if lasttime:
      x1 = b[i].split()[0].split(".")
      x2 = b[i].split()[1].split(":")
      y1 = lasttime.split()[0].split(".")
      y2 = lasttime.split()[1].split(":")
    
      now = datetime.datetime(int(x1[2]), int(x1[1]), int(x1[0]), int(x2[0]), int(x2[1]))
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

htmlcode = HTML.table(table_data, header_row = ['date', 'description'])

if len(table_data) > 0:
  newfile = "Opinions_" + "_".join(today.split()) + ".html"
  f = open(newfile, "w+")
  tmp = begin + htmlcode + end
  f.write(tmp)
  f.close()
   
  from email.MIMEMultipart import MIMEMultipart
  from email.MIMEText import MIMEText
  from email.MIMEImage import MIMEImage
  msg = MIMEMultipart()
  msg.attach(MIMEText(file(newfile).read()))

  
  #send_mail(send_from=email, send_to=[email], subject="Opinion " + today, text="Opinions are in attachments", files=[newfile])
  mailer = smtplib.SMTP('smtp.gmail.com', 587)
  username = "lbeasty@gmail.com"
  passwd = "Nhfkzkz14Ifitr"
  #mailer.connect()
  mailer.ehlo()
  mailer.starttls()
  mailer.login(username, passwd)
  mailer.sendmail(email, [email], msg.as_string())
  mailer.close()

  send_email(email, "Nhfkzkz14Ifitr", email , ["roma.jam.zapman@gmail.com"], "test subject", "test text")
  #mailer.quit()
  
#e = page.getroot().find_class('m_info inf_ml').pop()



#['__class__', '__contains__', '__copy__', '__deepcopy__', '__delattr__', '__delitem__', '__dict__', '__doc__', '__format__', '__getattribute__', '__getitem__', '__hash__', '__init__', '__iter__', '__len__', '__module__', '__new__', '__nonzero__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_init', '_label__del', '_label__get', '_label__set', 'addnext', 'addprevious', 'append', 'attrib', 'base', 'base_url', 'body', 'clear', 'cssselect', 'drop_tag', 'drop_tree', 'extend', 'find', 'find_class', 'find_rel_links', 'findall', 'findtext', 'forms', 'get', 'get_element_by_id', 'getchildren', 'getiterator', 'getnext', 'getparent', 'getprevious', 'getroottree', 'head', 'index', 'insert', 'items', 'iter', 'iterancestors', 'iterchildren', 'iterdescendants', 'iterfind', 'iterlinks', 'itersiblings', 'itertext', 'keys', 'label', 'make_links_absolute', 'makeelement', 'nsmap', 'prefix', 'remove', 'replace', 'resolve_base_href', 'rewrite_links', 'set', 'sourceline', 'tag', 'tail', 'text', 'text_content', 'values', 'xpath']
  
