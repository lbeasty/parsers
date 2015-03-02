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

addresses, email_list = main.ReadConfig("main.ini", "med-otzyv")
main_domain_stat = addresses[0].split("/")[2]
today = strftime("%d.%m.%Y %H:%M", gmtime())
a = []
b = []
table_data = []
for page_link in addresses:
    page = html.parse(page_link)
    #page1.getroot().findall(".//p[@style]")[0].text_content()
    for el in page.getroot().find_class('comment-body'):
        a.append(unicode(el.text_content() + "<br>" + page_link).encode("utf-8")) #(el.text_content().encode("ISO-8859-1"))#.decode("utf-8"))
    for el in page.getroot().find_class("comment-date"): #('review_date'):
        b.append(unicode(el.text_content()).encode("utf-8")) #el.getchildren()[0].text.encode("ISO-8859-1"))#.decode("utf-8"))

for i in range(len(a)):
    if os.path.isfile("tmpfile"):
        f = open("tmpfile", "r+")
        lasttime = f.readline()
        if lasttime:
            x1 = b[i].encode("utf-8").split()[0].split(".")
            x2 = b[i].encode("utf-8").split()[1].split(":")
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
    newfile = "Opinions_" + main_domain_stat + "_".join(today.split()) + ".html"
    f = open(newfile, "w+")
    tmp = main.begin + htmlcode + main.end
    f.write(tmp)
    f.close()

    for email in email_list:
        main.send_email(main.username, main.passwd, email , email, "test subject", tmp)

else:
    print "Nothing new"
