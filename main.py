import urllib.request
from bs4 import BeautifulSoup
import urllib.request, sys, time
import requests
import csv
import pandas as pd
import re
import datetime
from datetime import datetime
from datetime import date
from datetime import timedelta

# import re #regular expressions looks for string patterns #print(re.findall(r'\$[0-9,.]+', page.text))

keywords = re.compile(
    r'\b(.*)Covid(.*)\b | \b(.*)vaccine(.*)\b | \b(.*)CDC(.*)\b | \b(.*)Janssen(.*)\b | \b(.*)Pfizer(.*)\b | \b(.*)Moderna(.*)\b | \b(.*)booster(.*)\b | \b(.*)omicron(.*)\b | \b(.*)variant(.*)\b | \b(.*)third dose(.*)\b',
    re.IGNORECASE)

TodaysDate = date.today()
TodaysDate = datetime.strptime(str(TodaysDate), '%Y-%m-%d').date()
print(TodaysDate)
pd.options.display.max_colwidth = 1000

# dates = [datetime.strptime(dates, '%m/%d/%Y').date()]
# ==============================================================================
# POLITICO

try:
    url = 'https://www.politico.com/'
    page = requests.get(url)
except Exception as e:
    error_type, error_obj, error_info = sys.exc_info()
    print('Error for link:')
    print(error_type, 'Line:', error_info.tb_lineno)

print(page.status_code)
print(page.headers.get('content-type', 'unknown'))
soup = BeautifulSoup(page.text, 'html.parser')
print(soup.title)

mainTag = soup.find_all(['body'])  # , attrs={'id':'main'})

results = []
results = ['</ul><a href=' + str(url) + '>Politico</a><ul>']
# print (results)
datelist = []
for links in mainTag:
    linkTags = links.find_all('a')  # , attrs={'class':'js-tealium-tracking'}
    for link in linkTags:
        target_link = keywords.search(link.text)
        target_politico_category = re.search('news', link.get('href'))
        if target_link != None and target_politico_category != None:
            # print (target_link)
            # print (target_politico_category)
            # print ("Aria Label:", link.get('aria-label'))
            # print ("Link text:",link.text)

            if len(link.text) < 100:
                LinkTitle = link.text
            else:
                LinkTitle = link.get('aria-label')

            TodaysDate = date.today()
            HTML_Links = '<li><a href=' + link.get('href') + '>' + LinkTitle + '</a></li>'

            results.append(HTML_Links)
            datelist.append(TodaysDate)

        else:
            pass

df = pd.DataFrame(results, columns=['Links'])
df['Date'] = pd.to_datetime('today').strftime('%Y-%m-%d')
df['Source'] = 'Politico'
df['ReadStatus'] = 0

# print(df)
# df.to_csv('output.csv', mode='w', header=False)

# ==============================================================================
# WaPo
import time

try:
    url = 'https://www.washingtonpost.com/coronavirus/'
    page = requests.get(url)
except Exception as e:
    error_type, error_obj, error_info = sys.exc_info()
    print('Error for link:')
    print(error_type, 'Line:', error_info.tb_lineno)
print(page.status_code)
print(page.headers.get('content-type', 'unknown'))
soup = BeautifulSoup(page.text, 'html.parser')
# print (soup.title)

mainTag = soup.find_all(['h2'])  # , attrs={'class':'h4'})
results = []
results = ['</ul><a href=' + str(url) + '>Washington Post</a><ul>']
datelist = []

for links in mainTag:
    linkTags = links.find_all('a')  # , attrs={'class':'js-tealium-tracking'}

    for link in linkTags:
        target_link = keywords.search(link.text)
        if target_link != None:
            # print (target_link)
            LinkTitle = link.text
            TodaysDate = date.today()
            HTML_Links = '<li><a href=' + link.get('href') + '>' + LinkTitle + '</a></li>'
            results.append(HTML_Links)
            datelist.append(TodaysDate)
        else:
            pass

df4 = pd.DataFrame(results, columns=['Links'])
df4['Date'] = pd.to_datetime('today').strftime('%Y-%m-%d')
df4['Source'] = 'WashingtonPost'
df4['ReadStatus'] = 0
df = df.append(df4, ignore_index=True)
# print(df)
# df.to_csv('output.csv', mode='w', header=False)

# ==============================================================================
# AXIOS/HEALTH SECTION

try:
    url = 'https://www.axios.com/health/'
    page = requests.get(url)
except Exception as e:
    error_type, error_obj, error_info = sys.exc_info()
    print('Error for link:')
    print(error_type, 'Line:', error_info.tb_lineno)

soup = BeautifulSoup(page.text, 'html.parser')

mainTag = soup.find_all(['h3'])  # , attrs={'id':'main'})

results = []
results = ['</ul><p>AXIOS|<a href="' + str(url) + '">Health</a><ul>']

for links in mainTag:
    linkTags = links.find_all('a')  # , attrs={'class':'js-tealium-tracking'}
    for link in linkTags:
        target_link = keywords.search(link.text)
        if target_link != None:
            # print (target_link)
            # print (target_politico_category)
            # print ("Aria Label:", link.get('aria-label'))
            # print ("Link text:",link.text)

            if len(link.text) < 100:
                LinkTitle = link.text
            else:
                LinkTitle = link.get('aria-label')

            HTML_Links = '<li><a href=' + link.get('href') + '>' + LinkTitle + '</a></li>'
            TodaysDate = date.today()

            results.append(HTML_Links)
            datelist.append(TodaysDate)

            # with open('output.csv', 'a', newline='') as csvfile:
            #    propertyWriter = csv.writer(csvfile)
            #    propertyWriter.writerow([HTML_Links])
        else:
            pass
# print (results)
df2 = pd.DataFrame(results, columns=['Links'])
df2['Date'] = pd.to_datetime('today').strftime('%Y-%m-%d')
df2['Source'] = 'Axios'
df2['ReadStatus'] = 0
df = df.append(df2, ignore_index=True)
# print(df)
# df.to_csv('output.csv', mode='a', header=False)

# ==============================================================================

# FDA
##
##try:
##    url = ('https://www.fda.gov/drugs/new-drugs-fda-cders-new-molecular-entities-and-new-therapeutic-biological-products/novel-drug-approvals-2021')
##    page = requests.get(url)
##except Exception as e:
##        error_type, error_obj, error_info = sys.exc_info()
##        print ('Error for link:')
##        print (error_type, 'Line:', error_info.tb_lineno)
##print (page.status_code)
##print (page.headers.get('content-type', 'unknown'))
##soup = BeautifulSoup(page.text, 'html.parser')
##FDA_title = (soup.title)
##
##results = []
##results = ['</ul>' + str(FDA_title.text[0:-3]) + '<a href="' + str(url) + '">'  + 'FDA</a><ul>']
##
##mainTag = soup.tbody
##for row in mainTag.find_all('tr'):
##    Brand_column = row.find_all('td')[1].contents
##    Generic_column = row.find_all('td')[2].contents
##    Indication_column = row.find_all('td')[4].contents
##    idNum = str(row.find('a').get('href'))
##    idNum = idNum.replace(' ','')
##    idNum = idNum[-6:]
##    Date_column = row.find_all('td')[3].contents
##    #print (Date_column, Brand_column, Generic_column, Indication_column)
##    date_strings = [''.join(dates) for dates in Date_column]
##    for dates in date_strings:
##       dates = [datetime.strptime(dates, '%m/%d/%Y').date()]
##       OneWeekAgo = [datetime.strptime(str((date.today() - timedelta(days = 7))),'%Y-%m-%d').date()]
##       #print ('Dates:', dates)
##       #print ('OneWeekAgo:', OneWeekAgo)
##    if dates > OneWeekAgo:
##        FDA_Drugs = ('<li>' + str(Brand_column) + ' (' + str(Generic_column) + ')' + '<br><font size=2px>' + str(Indication_column) + '. (' + str(Date_column) + ') | ' + '<a href=https://www.accessdata.fda.gov/drugsatfda_docs/label/2021/' + idNum + 's000lbl.pdf>Label</a></font></li>')
##        FDA_Drugs = FDA_Drugs.replace("'",'')
##        FDA_Drugs = FDA_Drugs.replace("[",'')
##        FDA_Drugs = FDA_Drugs.replace("]",'')
##        FDA_Drugs = FDA_Drugs.replace(' "','"')
##
##        results.append(FDA_Drugs)
##        datelist.append(TodaysDate)
##    else:
##        pass
##
##df3 = pd.DataFrame(results, columns=['Links'])
##df3['Date'] = pd.to_datetime('today').strftime('%Y-%m-%d')
##df3['Source'] = 'FDA'
##df3['ReadStatus'] = 0
##df = df.append(df3, ignore_index=True)


# ==============================================================================
# print (df)
df.sort_values(by='Source')
# print (df.sort_values(by='Source'))
# print ('End Dfs')
# ==============================================================================
# Output to CSV
df.to_csv('output.csv', mode='a', header=None)

df = pd.read_csv('output.csv', header=None)
# print (df)
df_unique = df.drop_duplicates(subset=[1], keep='first')  # removes duplicates from csv, retains first row
# print (df_unique)
df_unique.to_csv('output.csv', mode='w', header=None, index=False)

df_unique = df_unique.sort_values(by=[3, 4])
# print (df_unique.iloc[:,3])

# print(df_unique)

Unread = df_unique[(df_unique.iloc[:, 4] < 1)]
# print (Unread)
Unread = Unread.iloc[:, 1]
# print (Unread)
Unread_Links = Unread.to_string(index=False)

# print(Unread_Links)

if Unread_Links == 'Series([], )':
    Unread_Links = 'No news is good news.'
else:
    pass

df_MarkAsRead = pd.read_csv('output.csv', header=None)
# print(df_MarkAsRead)
df_MarkAsRead.iloc[:, 4] = df_MarkAsRead.iloc[:, 4].replace({0: 1})
# print(df_MarkAsRead)
df_MarkAsRead = df_MarkAsRead.sort_values(by=[3, 4])
df_MarkAsRead.to_csv('output.csv', mode='w', header=None, index=False)

# ==============================================================================

from tabulate import tabulate
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

me = 'datareads@gmail.com'
password = 'odpsifqnmcbtgbzw'
server = 'smtp.gmail.com:587'
you = 'ahimsel@comcast.net'

News_html = '''
    <html><body><p>Daily News Headlines</p>
    <ul>
    {table}
    </ul>
    </body></html>
    <p>
'''

message = MIMEMultipart('alternative', None, [MIMEText(Unread_Links, 'html')])

message['Subject'] = "Daily News Headlines"
message['From'] = me
message['To'] = you
server = smtplib.SMTP(server)
server.ehlo()
server.starttls()
server.login(me, password)
server.sendmail(me, you, message.as_string())
server.quit()

