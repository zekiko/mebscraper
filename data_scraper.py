import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


schoolList = []
addressList = []

def getSchoolList(ilkodu):
    url = "https://www.meb.gov.tr/baglantilar/okullar/index.php?ILKODU=" + ilkodu
    df = pd.read_html(url)[0]

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')

    for tr in table.findAll("tr"):
        trs = tr.findAll("td")

        i = 0
        ar = []
        for each in trs:
            try:
                if(i == 0):
                    name = each.find('a').text
                    if("lise" in name.lower() or "LİSE" in name.upper()):
                        ar.append(name)
                    else:
                        break
                elif(i == 1):
                    link = each.find('a')['href']
                    ar.append(link)
                i = i + 1
            except:
                pass
        if(len(ar) != 0):
            schoolList.append(ar)

#df['Link'] = schoolList


def getPhyscalAddress(URL, index):
    try:
        html_doc = requests.get(URL)
        soup = BeautifulSoup(html_doc.text, 'html.parser')

        laka = soup.text
        for line in laka.split("\n"):
            keywords = re.findall(r'[^-/,\s.]+', line)

            for i in keywords:
                if ("sk" == i.lower() or "sok" == i.lower() or "sokak" == i.lower()  or "sokağı" in i.lower()
                    or "cd" == i.lower() or "cad" == i.lower() or "cadde" == i.lower() or "caddesi" in i.lower()
                    or "mh" == i.lower() or "mah" == i.lower() or "mah " == i.lower() or " mahalle" == i.lower() or "mahallesi" in i.lower())\
                    or "köyü" == i.lower() or "km" == i.lower() or "bulvar" == i.lower() or "bulvarı" in i.lower()\
                    or "kısım" == i.lower():

                    str = " ".join(keywords)
                    addressList.append(str)

                    print(index, keywords)

                    return

        addressList.append("-")
        print("BULAMADI")
        return
    except:
        pass


def appendAddressToSchoolList():
    for i in range(len(schoolList)):
        schoolList[i].append(addressList[i])



def application():

    getSchoolList("2")

    for i in range(len(schoolList)):
        getPhyscalAddress(schoolList[i][1], i)

    print("lengths: ", len(schoolList), len(addressList))

    appendAddressToSchoolList()

    for i in schoolList:
        print(i)

    df = pd.DataFrame(schoolList)
    csv_data = df.to_csv("lise.csv", header=['LİSE', 'WEB', 'ADRES'], mode='w')

application()