

import requests; import datetime; from bs4 import BeautifulSoup as BS; import lxml;from lxml import html;
import csv;import urllib.request;from urllib.parse import urljoin;from lxml.html import fromstring, tostring
from lxml import etree;import xml.etree.ElementTree as ET; import xml.parsers.expat;
from urllib.parse import urlparse;import pyodbc;import re;import zipfile;import pandas as pd;
import sqlalchemy as sqla;from sqlalchemy import create_engine
from sqlalchemy import select; import numpy as np;from datetime import date;from datetime import datetime

url = ['http://reports.ieso.ca/public/VGTieBreakingRankings/']
translation_table = dict.fromkeys(map(ord, 'Tt_vV'), None)
translationtable2 = dict.fromkeys(map(ord, "-"),"/")
translation_table3 = dict.fromkeys(map(ord, 'Tt-:'), '_')
translation_table4 = dict.fromkeys(map(ord,'[datetime.timedelta()ys, 0:00:00]'),None)
Ranking = []
Ranking_Days = []
Price = []
date =[]
ResourceName = []



for i in url:
    proxy_support = urllib.request.ProxyHandler({})
    opener = urllib.request.build_opener(proxy_support)
    urllib.request.install_opener(opener)
    html = urllib.request.urlopen(i).read()
    soup = BS(html)
    tags = soup('a')
    for tag in tags:
        href = (tag.get('href'))
        if href.endswith(".xml"):
            xml_url = urllib.parse.urljoin(i, href)
            if xml_url != 'http://reports.ieso.ca/public/VGTieBreakingRankings/PUB_VGTieBreakingRankings.xml':
                xml_list = xml_url.split(',')
                for b in xml_list:
                    page = urllib.request.urlopen(b).read()
                    soup = BS(page, "lxml-xml")
                    startdate = soup.find("StartDate").text
                    startdate2 = startdate.translate(translationtable2)
                    a = datetime.strptime(startdate2, "%Y/%m/%d")
                    enddate = soup.find("EndDate").text
                    enddate2 = enddate.translate(translationtable2)
                    b = datetime.strptime(enddate2, "%Y/%m/%d")
                    l1 = str(b-a)
                    l2 = l1.translate(translation_table4)
                    l3 = int(l2)
                    c = l3 + 1
                    date_version1 = soup.find("CreatedAt").text
                    date_version = date_version1.translate(translation_table3)
                    ranking_days = soup.find_all('RankingDay')
                    for a1 in ranking_days:
                        Ranking_Days.append(a1.get_text())
                    rankings = soup.find_all("Ranking")
                    for b1 in rankings:
                        Ranking.append(b1.get_text())
                    resourcenms = soup.find_all("ResourceName")
                    for c1 in resourcenms:
                        ResourceName.append(c1.get_text())
                    forDateDF =[]
                    for d1 in ResourceName:
                        forDateDF.append(date_version)
                    Rankings = []
                    binit = 0;bstop = c
                    while bstop <= len(Ranking):
                        Rankings.append(Ranking[binit:bstop])
                        binit += c;bstop += c
                    RankingDF = pd.DataFrame(Rankings)
                    DateDF = pd.DataFrame(forDateDF)
                    Resource_NameDF = pd.DataFrame(ResourceName)
                    final = pd.concat([Resource_NameDF, RankingDF], axis = 1)
                    final['Dateversion'] = forDateDF
                    filename = ("C:/Users/smacn/desktop/test/VGTieBreakingRankings%s"
                                % date_version + ".csv")
                    filenames = []
                    if filename not in filenames:
                        filenames.append(filename)
                        final.to_csv(filename, header=False, index=False)
