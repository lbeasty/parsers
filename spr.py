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

addresses, email_list = main.ReadConfig("main.ini", "spr")
main_domain_stat = addresses[0].split("/")[2]
print main_domain_stat
today = strftime("%d.%m.%Y %H:%M", gmtime())
a = []
b = []
table_data = []
for page_link in addresses:
    print page_link
    #main_domain_stat = 'http://mosclinic.ru/medcentres'
    #page_link = '%s/%s' % (main_domain_stat, "59")
    page = html.parse(page_link)
    for el in page.getroot().find_class('noline'):
        link = el.values()[1]
        if "id_tema" in link:
            page1 = html.parse('%s' % (link))
            content = page1.getroot().findall(".//p[@style]")[0].text_content()
            time = page1.getroot().findall(".//span[@style]")
            a.append(unicode(content + "<br>" + page_link).encode("utf-8"))
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
                #months = (u'января', u'февраля', u'марта', u'апреля', u'мая', u'июня', u'июля', u'августа', u'сентября',     u'октября', u'ноября', u'декабря')
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
