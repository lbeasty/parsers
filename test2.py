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
	    print text
            gmail_user = user
            gmail_pwd = pswd
            FROM = from_
            TO = to_ #must be a list
            SUBJECT = subject
            TEXT = text

            # Prepare actual message
            #message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            #""" % (FROM, ", ".join(TO), SUBJECT, TEXT)
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = FROM
            msg['To'] = TO
            txt = "test text"
            #part1 = MIMEText(text, 'plain')
            #part2 = MIMEText(text, 'html')
            #msg.attach(part1)
            #msg.attach(part2)

	    #message = """From: From Person <%s>
#To: To Person <%s>
#MIME-Version: 1.0
#Content-type: text/html
#Subject: %s

#This is an e-mail message to be sent in HTML format
#%s
#""" % (from_, to_, subject, text)

#            print message


	    test = """
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <title>html title</title>
  <style type="text/css" media="screen">
    table{
        background-color: #AAD373;
        empty-cells:hide;
    }
    td.cell{
        background-color: white;
    }
  </style>
</head>
<body>
  <table style="border: blue 1px solid;">
    <tr><td class="cell">Cell 1.1</td><td class="cell">Cell 1.2</td></tr>
    <tr><td class="cell">Cell 2.1</td><td class="cell"></td></tr>
  </table>
</body>
"""

            part1 = MIMEText(txt, 'plain')
            part2 = MIMEText(test, 'html')
            msg.attach(part1)
            msg.attach(part2)

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
conf = "test2.ini"
Config.read(conf)

address = ConfigSectionMap(Config.sections()[0])['address']
email = ConfigSectionMap(Config.sections()[0])['email']

today = strftime("%d.%m.%Y %H:%M", gmtime())
#print "today: ", "!" + today + "!"

main_domain_stat = 'http://www.spr.ru/otzyvy'

page = html.parse('%s/%s' % (main_domain_stat, address))

#print '%s/klinika-evro-med-moskva-pr-kt-mira-3-k-1' % (main_domain_stat)
#print dir(page)
#print 


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
for el in page.getroot().find_class('noline'):
  #print el.keys()
  #print
  #print el.values()
  #print 
  #print el.items()
  #print dir(el)
  link = el.values()[1]
  #print "LINK"
  #print link
  if "id_tema" in link:
    page1 = html.parse('%s' % (link))
    content = page1.getroot().findall(".//p[@style]")[0].text_content()
  
    #a.append(el.getchildren()[0].getchildren()[0].text.encode('utf-8'))
    #print
    #print el.text
    #print
    time = page1.getroot().findall(".//span[@style]")
    #print time[8].text_content()
    
    a.append(unicode(content).encode("utf-8"))#.encode("ISO-8859-1"))#.decode("utf-8"))
  
    #title = el.values()[4]
    #time = title.split()[2].split(".")[0]
    #print time
    b.append(unicode(time[8].text_content()).encode("utf-8"))


#datas = page.getroot().find_class('review_date')
#for el in datas:
  #print el.getchildren()[0].text.encode("ISO-8859-1").decode("utf-8")
  #print 
  #print "!" + ' '.join(el.text_content().split()) + "!"
#  b.append(el.getchildren()[0].text.encode("ISO-8859-1"))#.decode("utf-8"))

#print
#print a
#print
#print b
table_data = []
#	['date', 'description']]

for i in range(len(a)):
  if os.path.isfile("tmpfile"):
    f = open("tmpfile", "r+")
    lasttime = f.readline()
    if lasttime:
      #print b[i].encode("utf-8").split()
      #print
      x1 = b[i].encode("utf-8").split("|")[0].split()[0].split("-")
      #print x1
      #print "!", b[i].encode("utf-8").split("|")[1].split(), "!"
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
   
  from email.MIMEMultipart import MIMEMultipart
  from email.MIMEText import MIMEText
  from email.MIMEImage import MIMEImage
  msg = MIMEMultipart()
  msg.attach(MIMEText(file(newfile).read()))

  
  #send_mail(send_from=email, send_to=[email], subject="Opinion " + today, text="Opinions are in attachments", files=[newfile])
  mailer = smtplib.SMTP('smtp.gmail.com', 587)
  username = "sashaslenastestserver@gmail.com"
  passwd = "SashasLenasPassword"
  #mailer.connect()
  #mailer.ehlo()
  #mailer.starttls()
  #mailer.login(username, passwd)
  #mailer.sendmail(email, [email], msg.as_string())
  #mailer.close()

  send_email(username, passwd, "muskatus@inbox.ru" , ["muskatus@inbox.ru"], "test subject", tmp)
  #mailer.quit()
# -*- coding: utf-8 -*-
import HTML
import lxml.html as html
import datetime
import os.path
import smtplib
import main

from os.path import basename
#from pandas import DataFrame
from time import gmtime, strftime

addresses, email_list = main.ReadConfig("main.ini", "moskva.tulp")
main_domain_stat = addresses[0].split("/")[2]
print main_domain_stat
today = strftime("%d.%m.%Y %H:%M", gmtime())
a = []
b = []
table_data = []
for page_link in addresses:
    #main_domain_stat = 'http://mosclinic.ru/medcentres'
    #page_link = '%s/%s' % (main_domain_stat, "59")
    page = html.parse(page_link)
    for el in page.getroot().find_class('noline'):
        link = el.values()[1]
        if "id_tema" in link:
            page1 = html.parse('%s' % (link))
            content = page1.getroot().findall(".//p[@style]")[0].text_content()
            time = page1.getroot().findall(".//span[@style]")
            a.append(unicode(content).encode("utf-8"))
            b.append(unicode(time[8].text_content()).encode("utf-8"))

    for i in range(len(a)):
        if os.path.isfile("tmpfile"):
            f = open("tmpfile", "r+")
            lasttime = f.readline()
            if lasttime:
                x1 = b[i].encode("utf-8").split("|")[0].split()[0].split("-")
                x2 = b[i].encode("utf-8").split("|")[1].split()[0].split(":")
                #x2 = [0, 0]
                y1 = lasttime.split()[0].split(".")
                y2 = lasttime.split()[1].split(":")
                #months = (u'ц▒ц≈ц▓', u'ц├ц≈ц│ц▒, u'ц█ц▓ц│, u'ц│ц▓ц▄', u'ц█ц▒, u'ц┴ц▌', u'ц┴ц▄', u'ц│ц┤ц⌠ц│, u'ц⌠ц▌ц▒ц▓', u'ц▐ц■ц┌ц▒, u'ц▌ц▒ц▓', u'ц└ц▀ц┌ц▒)
      #month = next(i for i,name in enumerate(months,1) if name in x1[1].decode("utf-8"))
                now = datetime.datetime(int(x1[0]), int(x1[1]), int(x1[2]), int(x2[0]), int(x2[1]))
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
    newfile = "Opinions_" + main_domain_stat + "_".join(today.split()) + ".html"
    f = open(newfile, "w+")
    tmp = main.begin + htmlcode + main.end
    f.write(tmp)
    f.close()

    for email in email_list:
        main.send_email(main.username, main.passwd, email , email, "test subject", tmp)

else:
    print "Nothing new"
