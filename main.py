import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

URL = 'http://www.st-petersburg.vybory.izbirkom.ru/region/st-petersburg?action=ik&vrn='

driver = webdriver.PhantomJS(executable_path='C:\Program Files (x86)\Google\phantomjs.exe')
url = 'http://www.st-petersburg.vybory.izbirkom.ru/region/st-petersburg?action=ik&vrn=27820001006425'
driver.get(url)
html_tree = driver.find_element(By.ID, 'tree')
source_code = html_tree.get_attribute("outerHTML")
soup_tree = BeautifulSoup(source_code, 'lxml')
find_id = soup_tree.find_all('li', class_='jstree-node jstree-closed')
TikIds = []
for li in find_id:
    ID = li.get('id')
    if ID is not None:
        TikIds.append(ID)
find_id = soup_tree.find_all('li', class_='jstree-node jstree-closed jstree-last')
for li in find_id:
    ID = li.get('id')
    if ID is not None:
        TikIds.append(ID)
print(TikIds)

file = open('cik.tsv', 'w', encoding='utf-8')
file.write('Название избирательной комиссии\t'+'Название вышестоящей комиссии\t'+'ФИО\t'+'Статус\t'+'Кем предложен\n')
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
soup = soup.find('div', class_='center-colm')
tds = soup.find_all('td')
tds_text = []
for str in tds:
    str = str.get_text()
    tds_text.append(str)
i = 0
while i < len(tds_text):
    file.write(soup.find('h2').text+'\t-\t'+tds_text[i+1]+'\t'+tds_text[i+2]+'\t'+tds_text[i+3]+'\n')
    i = i+4

mas = []
mas.append(TikIds)
j = 0
for TikId in TikIds:
    j = j + 1
    UikIds = []
    while len(UikIds) == 0:
        driver.get(URL+TikId)
        html_tree = driver.find_element(By.ID, 'tree')
        source_code = html_tree.get_attribute("outerHTML")
        soup_tree = BeautifulSoup(source_code, 'lxml')

        response = requests.get(URL+TikId)
        soup = BeautifulSoup(response.text, 'lxml')
        soup = soup.find('div', class_='center-colm')
        tds = soup.find_all('td')
        tds_text = []
        for str in tds:
            str = str.get_text()
            tds_text.append(str)
        i = 0
        while i < len(tds_text):
            file.write(soup.find('h2').text + '\tСанкт-Петербургская избирательная комиссия\t' + tds_text[i + 1] + '\t' + tds_text[i + 2] + '\t' + tds_text[
                i + 3] + '\n')
            i = i + 4

        find_id = soup_tree.find_all('li', class_='jstree-node jstree-leaf')
        UikIds = []
        for Uik in find_id:
            UikId = Uik.get('id')
            if UikId is not None:
                UikIds.append(UikId)
        '''
        find_id = soup_tree.find_all('li', {'class':['jstree-node  jstree-leaf jstree-last','jstree-node jstree-leaf']})
        for Uik in find_id:
            UikId = Uik.get('id')
            if UikId is not None:
                UikIds.append(UikId)
        '''
        if len(UikIds) != 0:
            for UikId in UikIds:
                response = requests.get(URL+UikId)
                soup = BeautifulSoup(response.text, 'lxml')
                soup = soup.find('div', class_='center-colm')
                tds = soup.find_all('td')
                tds_text = []
                for str in tds:
                    str = str.get_text()
                    tds_text.append(str)
                i = 0
                while i < len(tds_text):
                    file.write(
                        soup.find('h2').text + '\tТИК ' + j.__str__() + '\t' + tds_text[i + 1] + '\t' + tds_text[i + 2]
                        + '\t' + tds_text[i + 3] + '\n')
                    i = i + 4

        mas.append(UikIds)
file.close()
print(mas)