import pandas as pd
import requests
from bs4 import BeautifulSoup


url = "https://www.meb.gov.tr/baglantilar/okullar/index.php?ILKODU=6&ILCEKODU=27"



response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table')

records = []
columns = []
for tr in table.findAll("tr"):
    ths = tr.findAll("th")
    if ths != []:
        for each in ths:
            columns.append(each.text)
    else:
        trs = tr.findAll("td")
        record = []
        for each in trs:
            try:
                link = each.find('a')['href']
                text = each.text
                record.append(link)
                record.append(text)
            except:
                text = each.text
                record.append(text)
        records.append(record)

columns.insert(1, 'Link')
df = pd.DataFrame(data=records, columns = columns)