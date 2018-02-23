# IESO_scrapes_py
A collection of scraping scripts for the IESO website (Independent Electricity Suppliers Ontario)
Some samples (pre class structuring) using py...

import requests; import datetime; from bs4 import BeautifulSoup as BS; import lxml;from lxml import html;
import csv;import urllib.request;from urllib.parse import urljoin;from lxml.html import fromstring, tostring
from lxml import etree;import xml.etree.ElementTree as ET; import xml.parsers.expat;
from urllib.parse import urlparse;import pyodbc;import re;import zipfile;import pandas as pd;
import sqlalchemy as sqla;from sqlalchemy import create_engine
from sqlalchemy import select; import numpy as np

url = ['http://reports.ieso.ca/public/Adequacy2/']
translation_table = dict.fromkeys(map(ord, '_vV'), None)
fueltype = []
energymw = []
date =[]

def getXmlURL(url):
    for i in url:
        proxy_support = urllib.request.ProxyHandler({})
        opener = urllib.request.build_opener(proxy_support)
        urllib.request.install_opener(opener)
        html = urllib.request.urlopen(i).read()
        soup = BS(html)
        tags = soup('a')
        #xml_list2 = []
        for tag in tags:
            href = (tag.get('href'))
            if href.endswith(".xml"):
                xml_url = urllib.parse.urljoin(i, href)
                if xml_url != 'http://reports.ieso.ca/public/Adequacy2/PUB_Adequacy2.xml':
                    xml_list = xml_url.split(',')
        return xml_list




def producemainattributes(xml_list):
    for a in xml_list:
        date_initial = (a.find('_201'))
        date_initial2 = (date_initial + 1)
        date_needed_for_logical_comparison2 = (a[date_initial2: -4])
        date_needed_for_logical_comparison3 = date_needed_for_logical_comparison2.translate(translation_table)
        date.append(date_needed_for_logical_comparison3)
        #for x in xml_list:
        page = urllib.request.urlopen(xml_list[-1]).read()
        soup = BS(page, "lxml-xml")
        soup.prettify()
        fuels = soup.find_all('RegionalArea')
        for a1 in fuels:
            fueltype.append(a1.get_text())
        energy = soup.find_all('EnergyMW')
        for b1 in energy:
            energymw.append(b1.get_text())
        print(date_needed_for_logical_comparison2)


a = getXmlURL(url)
b = producemainattributes(a)
#
energyDFprep  = []
i = 0;cin = 0;cout = 24
while i < len(energymw):
    energyDFprep.append(energymw[cin:cout])
    cin += 24; cout += 24;i += 24
#
# minMW = []
# i = 0;cin = 24;cout = 48
# while i < len(energymw):
#     minMW.append(energymw[cin:cout])
#     cin += 48;cout += 48;i += 48
#
# maxminsheader = ['Max','Min']
# AreasforDB = []
# for e1 in areas:
#     AreasforDB.append(e1);AreasforDB.append(maxminsheader[0]);AreasforDB.append(e1);AreasforDB.append(maxminsheader[1])
#

# AreasforDBPrecise = [i+j for i,j in zip(AreasforDB[::2], AreasforDB[1::2])]
#
# maxAreas = (AreasforDBPrecise[::2])
# minAreas = (AreasforDBPrecise[1::2])
Hour = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24]
# constmwT = np.array(Constrained_MW_for_Hour).T.tolist()
date_version = (date * 24)
#
Hours = pd.DataFrame(Hour)
date_ver_df = pd.DataFrame(date_version).T
Energy_MW = pd.DataFrame(energyDFprep).T #,minMW,constmwT]
# miniMWdf = pd.DataFrame(minMW).T
# maxareadf = pd.DataFrame(maxAreas).T
# allmaxDF = [maxiMWdf]#[maxareadf,maxiMWdf]

Energy_MW['Date_ver'] = date_version
Energy_MW['Hour'] = Hours

print(Energy_MW)
# #result = pd.Dataframe.join(maindf,date_ver_df,constrnedMWhrsdf)
#
# print(maxAreas)
# def produceCSV():
#         filename = ("C:/Users/smacn/desktop/test/DAAreaReserveConstraint%s"
#                     % date + ".csv")
#         filenames = []
#         if filename not in filenames:
#             filenames.append(filename)
#             result.to_csv(filename, header = False, index = False)
#             # for z in filenames:
#             #     with open(z, "w", newline='') as out:
#             #         # for this in df:
#             #         writer = csv.writer(out)
#             #         writer.writerow(df)
#         return filename
#
# #
# def writetosqldb(filename):
#     cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
#                                   "Server=LAPTOP-822QNLN6;"
#                                   "Database=IESO;"
#                                   "Trusted_Connection=yes;")
#     cursor = cnxn.cursor()
#     with open(filename, 'r') as f:
#         reader = csv.reader(f)
#         data = next(reader)
#         # for row in data:
#         #     cursor.execute('insert into [dbo].[DAAreaReserveConstraintsMax] values(?*39)',row[1:])
#         query = 'insert into dbo.DAAreaReserveConstraintsMax values ({0})'
#         query = query.format(','.join('?' * len(data)))
#         cursor = cnxn.cursor()
#         cursor.execute(query, data)
#         for data in reader:
#             cursor.execute(query, data)
#         cursor.commit()
#
#
#
# writetosqldb(produceCSV())

