import pandas as pd
import requests
from bs4 import BeautifulSoup
import re


url = "https://www.meb.gov.tr/baglantilar/okullar/index.php?ILKODU=6&ILCEKODU=6"
df = pd.read_html(url)[0]

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
table = soup.find('table')

links = []
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
        links.append(ar)

#df['Link'] = links

#print(len(links), links)
#print (links[0][1])

addressList = []
def getAdress(URL, i):
    try:
        html_doc = requests.get(URL)
        soup = BeautifulSoup(html_doc.text, 'html.parser')

        #print(URL)
        #print (soup.text)

        laka = soup.text
        for line in laka.split("\n"):
            kom = re.split('.  |\ ', line)
            print(kom)
            #if ("sk." in line.lower() or "sok." in line.lower() or "sokak" in line.lower()  or "sokağı" in line.lower()
             #       or "cd." in line.lower() or "cad." in line.lower() or "cadde" in line.lower() or "caddesi" in line.lower()
              #      or "mh." in line.lower() or "mah." in line.lower() or "mah " in line.lower() or "mahalle" in line.lower() or "mahallesi" in line.lower())\
               #     or "köyü" in line.lower() or ".km" in line.lower():
            if ("sk." in list(map(lambda x:x.lower(), kom)) or "sok." in list(map(lambda x:x.lower(), kom)) or "sokak" in list(map(lambda x:x.lower(), kom)) or "sokağı" in list(map(lambda x:x.lower(), kom))
                or "cd." in list(map(lambda x:x.lower(), kom)) or "cad." in list(map(lambda x:x.lower(), kom)) or "cadde" in list(map(lambda x:x.lower(), kom)) or "caddesi" in list(map(lambda x:x.lower(), kom))
                or "mh." in list(map(lambda x:x.lower(), kom)) or "mah." in list(map(lambda x:x.lower(), kom)) or "mah " in list(map(lambda x:x.lower(), kom)) or "mahalle" in list(map(lambda x:x.lower(), kom)) or "mahallesi" in list(map(lambda x:x.lower(), kom))) \
                    or "köyü" in list(map(lambda x:x.lower(), kom)) or ".km" in list(map(lambda x:x.lower(), kom)):

                addressList.append(line)
                #print(line)
                break
    except:
        pass


def appendAddressToSchoolList():
    for i in range(len(links)):
        links[i].append(addressList[i])


#print (url)
for i in range(len(links)):
    getAdress(links[i][1], i)





print(len(links), len(addressList))


appendAddressToSchoolList()

#for i in links:
    #print(i)


df = pd.DataFrame(links)
csv_data = df.to_csv("lise.csv", header=['ADI', 'WEBSİTESİ', 'ADRESİ'])
