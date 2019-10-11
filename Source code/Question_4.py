from bs4 import BeautifulSoup
import requests
import pandas as pd
import string
import json
import re
import time

# The key problem in this question was trying to figure out the right URL to scrape as the webpage has a lot of javascript
# Inspect on chrome helped, going to Network tab helped figure out the right URL from https://www.umkc.edu/calendar/
url = "https://www.trumba.com/s.aspx?calendar=UMKC&widget=main&date=" + time.strftime('%Y%m%d') + "&index=0&srpc.cbid=trumba.spud.4&srpc.get=true"
html = requests.get(url)
web_content = html.content
soup = BeautifulSoup(web_content, "html.parser")
# print(soup)

# Since html was tagged inside of body of the scraped page, I did a subscript to end up with the right html
body_start = html.text.find('<!DOCTYPE html PUBLIC')
body_end = html.text.find('</html>') + 7
body_part = html.text[body_start:body_end]
body = BeautifulSoup(body_part, "lxml")

# Page header
title = body.find('div', role=re.compile("heading")).text
events = []
events_all = body.find_all('a', role=re.compile("heading"))
for i in events_all:
    events.append(i.text)
times = []
times_all = body.find_all('span', role=re.compile("heading"))
for j in times_all:
    times.append(j.text)

dates_all = body.find_all('span', {'class': re.compile('StartDate')})
dates = []
for j in dates_all:
    dates.append(j.text)
locations_all = body.find_all('span', {'class': re.compile('Location')})
locations = []
for k in locations_all:
    locations.append(k.text)

# Find tables
table = body.find('table', {'class': re.compile('SimpleTableTable')})
print(table)

# table rows
tr = table.find_all('tr')
print(tr)

data = []

# table data
for x in tr[1:]:
    td = x.find_all('td')
    #print(td)
    y = [x.text for x in td]
    data.append(y)
data_h=[]

#table headers
for x in tr[1:]:
    th = x.find_all('th')
    #print(td)
    y = [x.text for x in th]
    data_h.append(y)

th.insert(0, 'index')
#print(th)
# Since data is at two levels, I had to combine them into a single dataframe

df = pd.DataFrame(data)
df_h = pd.DataFrame(data_h)
comb_df = pd.merge(df, df_h, left_index=True, right_index=True)
calendar_df = comb_df[['2_x', '3_x', '0_y', '4_x']]
calendar_df.columns = ['Date', 'Time', 'Event', 'Location']

# Write to file.
calendar_df.to_excel('UMKC_Calendar.xlsx')