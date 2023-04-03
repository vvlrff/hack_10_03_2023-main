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
            specifications = {'None':'None'}
    
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
    
def main() -> pd.DataFrame:
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
            
    print(dfGeneral)
    
    return dfGeneral

print(f'{__name__} is here !')

if __name__ == '__main__': 
    make_jsonFile( main(), 'data_banggood')
    
    



"""

"""

'''import requests
from bs4 import BeautifulSoup
import pandas as pd
from threading import Thread
from time import sleep
from random import choice

PARSING_MOD = "html5lib" # Используемый парсер HTML страницы

COUNT_THREADS = 8

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
                 "183.221.242.102:9443",
                 "183.221.242.103:9443",
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
    return BeautifulSoup(str(soup_copy), PARSING_MOD)

def get_hrefs( soup : BeautifulSoup) -> list:
    soup = get_currentPart(soup, 'span', 'img notranslate')
    listHrefs = []
    for link in soup.find_all('a'):
        listHrefs.append(link.get('href'))
    return listHrefs

def get_pageCount(soup : BeautifulSoup) -> int:
    soup = get_currentPart(soup, 'div', 'num')
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
            specifications = {'None':'None'}
    
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


def th_parsing(listColumns : list, hrefs : list, imges_hrefs : list, net_href : str  ) -> pd.DataFrame:
    # Прототип потока парсинга
    dfGeneral = get_emptyDataframe(listColumns) # Создаём пустой pd.dataframe с столбцами из listColumns
    for href in hrefs:
        current_url = href + "/specs"
        soup = get_soup(current_url)
        index = hrefs.index(href)
        try:
            img = imges_hrefs[index]
        except IndexError:
            img = 'www2.djicdn.com/cms/uploads/3f953b382abf679144358de6bdc84ac9.png'
        df = get_content( soup, listColumns, current_url, img, net_href )
        df = df.transpose()
        dfGeneral = pd.concat([dfGeneral, df])
    return dfGeneral



def getlistEqualPartsOfNumberParts(intNub : int, intParts : int) -> list:
  # Функция разбиения на равные части 
  d, r = divmod(intNub, intParts)
  return [d + (1 if i < r else 0) for i in range(intParts)]

def start_demons(list_threads : list) -> None:
    # Функция запуска потоков в фоне (демонов)
    for thread in list_threads:
       thread.start()

class CustomThread(Thread): # Создаём экземпляр потока Thread
    def __init__(self, var, listColumns : list, hrefs : list, imges_hrefs : list, net_href : str  ):
        Thread.__init__(self)
        self.daemon = True # Указываем, что этот поток - демон
        self.val = "None"
        self.var = var
        self.listColumns  = listColumns
        self.hrefs        = hrefs
        self.imges_hrefs  = imges_hrefs
        self.net_href     = net_href
        
    def run(self): # метод, который выполняется при запуске потока
        self.val = self.var( self.listColumns , self.hrefs , self.imges_hrefs , self.net_href )
        
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

def th_parsing(listColumns : list, hrefs : list, imges_hrefs : list, net_href : str  ) -> pd.DataFrame:
    # Прототип потока парсинга
    dfGeneral = get_emptyDataframe(listColumns) # Создаём пустой pd.dataframe с столбцами из listColumns
    for href in hrefs:    
        print(href)
        index = hrefs.index( href )
        soup = get_soup(href) # Получаем содержимое страници с определённой позицией
        df = get_content(soup, listColumns, href, imges_hrefs[index], net_href) # Получаем набор записей о позиции
        df = df.transpose()
        dfGeneral = pd.concat([dfGeneral, df])
    return dfGeneral

def main() -> pd.DataFrame:
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

        list_threads = []
        slice_start = 0
        parts = getlistEqualPartsOfNumberParts( len(hrefs), COUNT_THREADS)
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
    make_jsonFile(main(), 'data_banggood')'''