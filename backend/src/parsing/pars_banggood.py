import requests
# from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
import re
# import support_function as sf

class OwnError(Exception):
    def __init__(self, *args: object) -> None:
        if args:
            self.message = args[0]
        else:
            self.message = None
    
    def __str__(self) -> str:
        if self.message:
            return 'OwnError, {0} '.format(self.message)
        else:
            return 'OwnError has been raised!'

def get_soup(strURL : str) -> BeautifulSoup:
    try:
        response = requests.get(strURL)
        print('Status code :', response.status_code)
    except:
        print("Connection error")
    soup = BeautifulSoup(response.text, "html.parser") # "html.parser"
    return soup        

def get_currentPart(soup : BeautifulSoup, strTagName : str, strClassName : str) -> BeautifulSoup: 
    soup_copy = soup
    soup_copy = soup.findAll(strTagName, class_=strClassName)  
    return BeautifulSoup(str(soup_copy), "html.parser")

def get_hrefs( soup : BeautifulSoup) -> list:
    soup = get_currentPart(soup, 'span', 'img notranslate')
    listHrefs = []
    for link in soup.find_all('a'):
        listHrefs.append(link.get('href'))
    return listHrefs

def get_pageCount(soup : BeautifulSoup) -> int:
    soup = get_currentPart(soup, 'div', 'num')
    print(soup)
    return  int(soup.text.strip().rstrip().split('\n')[-2])
    
def get_emptyDataframe( listColoms : list) -> pd.DataFrame:
    df = pd.DataFrame(dict(zip(listColoms, []*len(listColoms))))
    return df

def get_spec_alt(soup : BeautifulSoup) -> dict:
    spec = soup.find('div', attrs={"style": "font-size:14px;"}) # style="font-size:14px;" .get_text('|', strip=True)
    specifications = {}
    
    for case in spec:
        case = case.get_text('|', strip=True)
        case = case.split("|")[2:]
        for item in case:
            content = item.split(':')
            if len( content ) == 2 and content[1] != '':
                specifications[content[0]] = content[1]
    return specifications

def get_spec(soup : BeautifulSoup) -> dict:
    spec = soup.find('div', class_='cont' ,attrs={"data-spm": "0000000UX"}).get_text('|', strip=True)
    spec = spec.split("|")[2:]
    specifications = {}
    
    for item in spec:
        content = item.split(':')
        if len( content ) == 2 and content[1] != '':
            specifications[content[0]] = content[1]
    return specifications

def get_content(soup : BeautifulSoup, listColumns : list, href: str, img_href : str, net_href : str) -> pd.DataFrame:
    try:
        tag = soup.find('span', attrs={"data-spm": "00000000a-3"}).get_text('|', strip=True)
    except Exception:
        tag = "None"
    
    try:
        brand = soup.find('a', attrs={"data-spm": "0000000Au"}).get_text('|', strip=True)
    except Exception:
        brand = "None"
        
    name =  soup.find('span', attrs={"data-spm": "0000000Ap"}).get_text('|', strip=True)
    price = 'None'
    
    try:
        specifications = get_spec(soup)
    except Exception:
        try:
            specifications = get_spec_alt(soup)
        except:
            specifications = 'None'
    
    return pd.DataFrame([href ,tag, brand, name, price, specifications, img_href, net_href], index = listColumns)

    
def make_jsonFile( df : pd.DataFrame, strFileName : str, strOrient = 'records'):
    path = __file__[:__file__.rfind('\\')] + '\\' + strFileName + '.json'
    with open(  path,'w', encoding='utf-8') as file:
        isWrited = file.write(df.to_json(force_ascii=False, indent=3, orient=strOrient))
        if isWrited : print(f'Successfully recorded in {path}')

def get_prices( soup : BeautifulSoup ) -> list:
    listHrefs = []
    soup = soup.find_all('span', attrs={"data-spm":"0000001Ut"} )
    
    for item in soup:
        content = item.get_text()
        listHrefs.append( content )

    return listHrefs
 
def get_images( soup : BeautifulSoup ) -> list:
    listHrefs = []
    soup = soup.find_all('span', attrs={"data-spm":"0000001Um"} )
    
    for item in soup:
        content = item.find('img').get('data-src')
        listHrefs.append( content )

    return listHrefs

def get_main_href(href : str) -> str:
    index = [i for i in range(len(href)) if href.startswith('/', i)]
    return href[:index[2]]
    
def main() -> None:
    strURL = 'https://www.banggood.com/ru/buy/germany-drone/8768-0-0-1-1-60-0-price-0-0_p-1.html' # Первая страница
    # strURL = 'https://www.banggood.com/ru/buy/germany-drone/8768-0-0-1-1-60-0-price-0-0_p-2.html' # Вторая страница
    
    listColumns = ['href','tag', 'brand', 'name','price','specifications', 'img_href', 'net_href']

    soup = get_soup(strURL) # Получаем содержимое страници 
    last_page = get_pageCount( soup )  # Получаем количество подстраниц
    dfGeneral = get_emptyDataframe(listColumns) # Создаём пустой pd.dataframe с столбцами из listColumns
    
    # last_page = 1
    
    for index in range(1, last_page ): # Проходим по всем страницам с деталями
        strURL = f'https://www.banggood.com/ru/buy/germany-drone/8768-0-0-1-1-60-0-price-0-0_p-{index}.html' # Страница с определённым индексом
        soup = get_soup(strURL) # Получаем содержимое страници 
        hrefs = get_hrefs(soup) # Получаем ссылки на продукты на данной странице
        net_href = get_main_href(strURL)
        imges_hrefs = get_images( soup )
        prices = get_prices( soup )
        for href in hrefs:    
            print(href)
            index = hrefs.index( href )
            soup = get_soup(href) # Получаем содержимое страници с определённой позицией
            df = get_content(soup, listColumns, href, imges_hrefs[index], net_href) # Получаем набор записей о позиции
            df = df.transpose()
            # print(df)
            dfGeneral = pd.concat([dfGeneral, df])
            
    make_jsonFile( dfGeneral, 'data_Germany_')
    
    # print( soup.div )
    # print( soup.find_all('div', class_= 'num') )

    
