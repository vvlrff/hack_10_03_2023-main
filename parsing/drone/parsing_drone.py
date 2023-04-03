'''
Европа :
https://www.drone.net.tr/drone-modelleri.html
'''


import requests
# from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
from googletrans import Translator

# translator = Translator()
translator = Translator(service_urls=['translate.googleapis.com'])

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
    soup = get_currentPart(soup, 'a', 'abt-single-image')
    listHrefs = []
    for link in soup.find_all('a'):
        listHrefs.append(link.get('href'))
    return listHrefs

def get_pageCount(soup : BeautifulSoup) -> int:
    case = soup.find('div', class_='ty-pagination') 
    text = case.get_text('|', strip=True).split('|')[-1]
    text = text.split('-')[-1].replace( " ", '')
    return  int(text)
    
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
    spec = soup.find('div', class_='ty-wysiwyg-content content-features').get_text('|', strip=True)
    spec = spec.split("|")[2:]
    specifications = {}
    
    for i in range( len( spec ) -1 ):
        # print( spec[i].find( ":" ) != -1 )
        if spec[i].find( ":" ) != -1 : 
           specifications[ translator.translate(spec[i], src='tr', dest='ru').text ] = translator.translate(spec[i+1], src='tr', dest='ru').text
    
    if len(specifications) == 0 : specifications = {'None':'None'}
    # print( specifications ) 
    
    # for item in spec:
    #     content = item.split(':')
    #     if len( content ) == 2 and content[1] != '':
    #         specifications[content[0]] = content[1]
    return specifications

def get_tag(soup : BeautifulSoup) -> str:
    cells = soup.find_all('span', attrs={"itemprop": "itemListElement"})
    tags = []
    for cell in cells:
        tags.append( cell.get_text("", strip=True) )
    return( tags[-1] )

def get_content(soup : BeautifulSoup, listColumns : list, href : str, img_href : str, net_href : str) -> pd.DataFrame:
    try:
        tag = get_tag( soup )
    except Exception:
        tag = "None"
    
    try:
        brand = soup.find('span',  class_ = 'ty-control-group').get_text('|', strip=True).split('|')[-1]
    except Exception:
        brand = "None"
        
    name =  soup.find('h1', class_ = 'ty-product-block-title').get_text('|', strip=True)
    # price = soup.find('span', class_='main-price', attrs={"data-spm": "0000000Bf"}).get_text('|', strip=True)
    price = soup.find('span', class_ = 'ty-price-num').get_text('|', strip=True)
    price = price.replace( ',', '').split( '.' )[0]
    
    try:
        specifications = get_spec(soup)
    except Exception:
        try:
            specifications = get_spec_alt(soup)
        except:
            specifications = {'None':'None'}
    
    tag = translator.translate(tag, src='tr', dest='ru').text
    price = int(int(price) * 4.03)
    
    # result = {listColumns[0]: tag, listColumns[1]: brand, listColumns[2]: name, listColumns[3]: price, listColumns[4]: specifications} 
    
    return pd.DataFrame([href, tag, brand, name, str(price), specifications, img_href, net_href], index = listColumns)


def make_jsonFile( df : pd.DataFrame, strFileName : str, strOrient = 'records'):
    # strPath = '../small_test_project/parsing/data/'
    # strPath = "parsing\data"
    
    # path = strPath + '\\' + strFileName + '.json'
    path = __file__[:__file__.rfind('\\')] + '\\' + strFileName + '.json'
    with open(  path,'w', encoding='utf-8') as file:
        isWrited = file.write(df.to_json(force_ascii=False, indent=3, orient=strOrient))
        if isWrited : print(f'Successfully recorded in {path}')
    
def get_main_href(href : str) -> str:
    index = [i for i in range(len(href)) if href.startswith('/', i)]
    return href[:index[2]]

def get_images( soup : BeautifulSoup) -> list:
    listHrefs = []
    soup = soup.find_all('a', class_='abt-single-image')
    i = len( soup )
    for item in soup:
        try:
            content = item.find('img').get('src')
        except Exception:
            content = 'https://www.drone.net.tr/images/thumbnails/230/230/detailed/2/H501M-1.png.jpg'
        listHrefs.append( content )
    if listHrefs[0] == 0 : 
        return listHrefs[1:]
    return listHrefs

def main() -> pd.DataFrame:
    strURL = 'https://www.drone.net.tr/drone-modelleri.html' # Первая страница
    # strURL = 'https://www.drone.net.tr/drone-modelleri-page-2.html' # Вторая страница
    
    listColumns = ['href','tag', 'brand', 'name','price','specifications', 'img_href', 'net_href']
    
    soup = get_soup(strURL) # Получаем содержимое страници 
    last_page = get_pageCount( soup )  # Получаем количество подстраниц
    dfGeneral = get_emptyDataframe(listColumns) # Создаём пустой pd.dataframe с столбцами из listColumns
    
    for index in range(1, last_page ): # Проходим по всем страницам с деталями
        strURL = f'https://www.drone.net.tr/drone-modelleri-page-{index}.html' # Страница с определённым индексом
        soup = get_soup(strURL) # Получаем содержимое страници 
        net_href = get_main_href(strURL) # Получаем "основную" ссылку 
        hrefs = get_hrefs(soup) # Получаем ссылки на продукты на данной странице
        imges_hrefs = get_images( soup )
        for href in hrefs:    
            try:
                print(href)
                soup = get_soup(href) # Получаем содержимое страници с определённой позицией
                index = hrefs.index(href)
                df = get_content(soup, listColumns, href, imges_hrefs[index], net_href ) # Получаем набор записей о позиции
                df = df.transpose()
                print(df)
                dfGeneral = pd.concat([dfGeneral, df])
            except Exception:
                pass
    # print(dfGeneral)
    
    return dfGeneral

print(f'{__name__} is here !')
    
if __name__ == '__main__': 
    make_jsonFile( main(), 'data_drone')
    


''''''
# Европа :
# https://www.drone.net.tr/drone-modelleri.html
'''


import requests
# from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
from googletrans import Translator

# translator = Translator()
translator = Translator(service_urls=['translate.googleapis.com'])

from random import choice
from threading import Thread
from time import sleep

PARSING_MOD = "lxml"
# PARSING_MOD = "html.parser" 

COUNT_THREADS = 4

HTTPS_PROXIES = ["143.42.26.80:8080",
                 "159.69.243.147:8080",
                 "65.108.212.10:8080",
                 "23.88.110.100:8080",
                 "167.235.228.20:8080",
                 "128.140.4.35:8080",
                 "45.79.251.98:8080",
                 "139.177.187.25:8080",
                 "139.162.29.240:8080",
                 "116.203.140.136:8080",
                 "49.12.244.38:8080",
                 "180.183.12.149:8080",
                 "168.119.167.98:8080",
                 "183.89.166.201:8080",
                 "5.78.79.194:8080"
                 ]

def get_proxy() -> dict:
    proxy = choice(HTTPS_PROXIES)
    return      { 
                 'http':  proxy,
                 'https': proxy,
                }
def remove_proxy( proxy : dict ) -> None:
    global HTTPS_PROXIES
    HTTPS_PROXIES.remove(proxy['http'])

def get_soup(strURL : str) -> BeautifulSoup:
    try:
        for iteration in range( len(HTTPS_PROXIES) ):
            proxy_servers = get_proxy()
            response = requests.get(strURL, proxies=proxy_servers, timeout=5)
            if response.status_code == 200:
                print('Status code :', response.status_code, 'for', strURL)
                soup = BeautifulSoup(response.text, PARSING_MOD) 
                return soup
            else:
                # remove_proxy(proxy_servers)
                pass
    except:
        print("Connection error")

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

def get_currentPart(soup : BeautifulSoup, strTagName : str, strClassName : str) -> BeautifulSoup: 
    soup_copy = soup
    soup_copy = soup.findAll(strTagName, class_=strClassName)  
    return BeautifulSoup(str(soup_copy), "html.parser")

def get_hrefs( soup : BeautifulSoup) -> list:
    soup = get_currentPart(soup, 'a', 'abt-single-image')
    listHrefs = []
    for link in soup.find_all('a'):
        listHrefs.append(link.get('href'))
    return listHrefs

def get_pageCount(soup : BeautifulSoup) -> int:
    case = soup.find('div', class_='ty-pagination') 
    text = case.get_text('|', strip=True).split('|')[-1]
    text = text.split('-')[-1].replace( " ", '')
    return  int(text)
    
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
    spec = soup.find('div', class_='ty-wysiwyg-content content-features').get_text('|', strip=True)
    spec = spec.split("|")[2:]
    specifications = {}
    
    for i in range( len( spec ) -1 ):
        if spec[i].find( ":" ) != -1 : 
           specifications[ translator.translate(spec[i], src='tr', dest='ru').text ] = translator.translate(spec[i+1], src='tr', dest='ru').text
    
    if len(specifications) == 0 : specifications = {'None':'None'}
    return specifications

def get_tag(soup : BeautifulSoup) -> str:
    cells = soup.find_all('span', attrs={"itemprop": "itemListElement"})
    tags = []
    for cell in cells:
        tags.append( cell.get_text("", strip=True) )
    return( tags[-1] )

def get_content(soup : BeautifulSoup, listColumns : list, href : str, img_href : str, net_href : str) -> pd.DataFrame:
    try:
        tag = get_tag( soup )
    except Exception:
        tag = "None"
    
    try:
        brand = soup.find('span',  class_ = 'ty-control-group').get_text('|', strip=True).split('|')[-1]
    except Exception:
        brand = "None"
        
    name =  soup.find('h1', class_ = 'ty-product-block-title').get_text('|', strip=True)
    # price = soup.find('span', class_='main-price', attrs={"data-spm": "0000000Bf"}).get_text('|', strip=True)
    price = soup.find('span', class_ = 'ty-price-num').get_text('|', strip=True)
    price = price.replace( ',', '').split( '.' )[0]
    
    try:
        specifications = get_spec(soup)
    except Exception:
        try:
            specifications = get_spec_alt(soup)
        except:
            specifications = {'None':'None'}
    
    tag = translator.translate(tag, src='tr', dest='ru').text
    price = int(int(price) * 4.03)

    return pd.DataFrame([href, tag, brand, name, str(price), specifications, img_href, net_href], index = listColumns)


def make_jsonFile( df : pd.DataFrame, strFileName : str, strOrient = 'records'):
    path = __file__[:__file__.rfind('\\')] + '\\' + strFileName + '.json'
    with open(  path,'w', encoding='utf-8') as file:
        isWrited = file.write(df.to_json(force_ascii=False, indent=3, orient=strOrient))
        if isWrited : print(f'Successfully recorded in {path}')
    
def get_main_href(href : str) -> str:
    index = [i for i in range(len(href)) if href.startswith('/', i)]
    return href[:index[2]]

def get_images( soup : BeautifulSoup) -> list:
    listHrefs = []
    soup = soup.find_all('a', class_='abt-single-image')
    i = len( soup )
    for item in soup:
        try:
            content = item.find('img').get('src')
        except Exception:
            content = 'https://www.drone.net.tr/images/thumbnails/230/230/detailed/2/H501M-1.png.jpg'
        listHrefs.append( content )
    if listHrefs[0] == 0 : 
        return listHrefs[1:]
    return listHrefs


def getlistEqualPartsOfNumberParts(intNub : int, intParts : int) -> list:
  # Функция разбиения на равные части 
  d, r = divmod(intNub, intParts)
  return [d + (1 if i < r else 0) for i in range(intParts)]

class CustomThread(Thread): # Создаём экземпляр потока Thread
    def __init__(self, var, listColumns : list, start : int, last_page : int   ):
        Thread.__init__(self)
        self.daemon = True # Указываем, что этот поток - демон
        self.val         = "None"
        self.var         = var
        self.listColumns = listColumns
        self.start          = start
        self.last_page      = last_page

        
    def run(self): # метод, который выполняется при запуске потока
        self.val = self.var( self.start , self.last_page  )
        
    def get_val(self):
        return self.val

def concat_list_of_df(list_df : list , listColumns : list) -> pd.DataFrame: 
    # Функция 'склеивания' dataframes
    cache_df =  get_emptyDataframe(listColumns) 
    for item_df in list_df:
        try:
            cache_df =  pd.concat([cache_df, item_df.get_val()])
        except Exception:
            pass
    return cache_df

def start_demons(list_threads : list) -> None:
    # Функция запуска потоков в фоне (демонов)
    for thread in list_threads:
       thread.start()

def th_parsing(listColumns : list, start : int, last_page : int  ) -> pd.DataFrame:
    # Прототип потока парсинга
    dfGeneral = get_emptyDataframe(listColumns) # Создаём пустой pd.dataframe с столбцами из listColumns
    for index in range(start, last_page ): # Проходим по всем страницам с деталями
        strURL = f'https://www.drone.net.tr/drone-modelleri-page-{index}.html' # Страница с определённым индексом
        soup = get_soup(strURL) # Получаем содержимое страници 
        net_href = get_main_href(strURL) # Получаем "основную" ссылку 
        hrefs = get_hrefs(soup) # Получаем ссылки на продукты на данной странице
        imges_hrefs = get_images( soup )
        for href in hrefs:    
            try:
                print(href)
                soup = get_soup(href) # Получаем содержимое страници с определённой позицией
                index = hrefs.index(href)
                df = get_content(soup, listColumns, href, imges_hrefs[index], net_href ) # Получаем набор записей о позиции
                df = df.transpose()
                print(df)
                dfGeneral = pd.concat([dfGeneral, df])
            except Exception:
                pass
    return dfGeneral

def main() -> pd.DataFrame:
    strURL = 'https://www.drone.net.tr/drone-modelleri.html' # Первая страница
    # strURL = 'https://www.drone.net.tr/drone-modelleri-page-2.html' # Вторая страница
    
    listColumns = ['href','tag', 'brand', 'name','price','specifications', 'img_href', 'net_href']
    
    soup = get_soup(strURL) # Получаем содержимое страници 
    last_page = get_pageCount( soup )  # Получаем количество подстраниц
    dfGeneral = get_emptyDataframe(listColumns) # Создаём пустой pd.dataframe с столбцами из listColumns
    
    
    # print(dfGeneral)
    
    list_threads = []
    slice_start = 0
    parts = getlistEqualPartsOfNumberParts( len(last_page), COUNT_THREADS)
    for i in range( len(parts) ):
        list_threads.append( CustomThread(    
                                          th_parsing ,  
                                          listColumns ,
                                          hrefs[slice_start : slice_start + parts[i]] ,
                                          imges_hrefs[slice_start : slice_start + parts[i]] ,
                                          net_href[slice_start : slice_start + parts[i]]                 
                                        ) 
                            )
        slice_start += parts[i]+1
        
    start_demons(list_threads)

    while True:
        sleep(3)
        b_in_progess = False
        for thread in list_threads:
            print(f" {thread.name} - {thread.is_alive()}")
            if  thread.is_alive() == True: b_in_progess = True
        if b_in_progess == False : 
            break
    
    return concat_list_of_df(list_threads, list_threads)
    
            
    
print(f'{__name__} is here !')

if __name__ == '__main__': 
    make_jsonFile(main(), 'data_drone')

'''