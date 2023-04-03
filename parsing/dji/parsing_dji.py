import requests
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
import unicodedata

# PARSING_MOD = "html.parser" 
PARSING_MOD = "lxml"

def get_soup(strURL : str) -> BeautifulSoup:
    try:
        response = requests.get(strURL)
        print('Status code :', response.status_code, 'for', strURL)
    except:
        print("Connection error")
    soup = BeautifulSoup(response.text, PARSING_MOD) # "html.parser"
    return soup        

def get_currentPart(soup : BeautifulSoup, strTagName : str, strClassName : str) -> BeautifulSoup: 
    soup_copy = soup
    soup_copy = soup.findAll(strTagName, class_=strClassName)  
    return BeautifulSoup(str(soup_copy), PARSING_MOD)

def get_hrefs( soup : BeautifulSoup) -> list:
    soup = get_currentPart(soup, 'div', 'product-item')
    listHrefs = []
    for link in soup.find_all('a'):
        listHrefs.append(link.get('href'))
    return listHrefs

def separate_href(hrefs : list) -> list : 
    result = []
    for href in hrefs:
        result.append( href.split('?')[0] )
    return result

def normolize_list_text(list_text : list) -> list:
    result = []
    for item in list_text:
        result = unicodedata.normalize("NFKD", item)
    return result

def get_soup_text( list_soups : list) -> list: 
    result = []
    for soup in list_soups:
        # text = soup.get_text('/n', strip=True)
        text = soup.get_text('/n', strip=True)
        # text = soup.get_text()
        
        text = unicodedata.normalize("NFKD", text)
        
        # text = text.split('|')
        # if len( text ) == 1 : text = text[0]
        result.append( text )
        # result.append( soup.text() )
    return result

def set_dict(keys : list, values : list) -> dict:
    result = {}
    for i in range( len(keys) ):
        result[keys[i]] = values[i]
    return result

def get_spec(soup : BeautifulSoup) -> dict:
    keys   = soup.find_all( 'li', class_='detailed-parameter-key' )
    if len(keys) != 0:
        values = soup.find_all( 'div', class_='detailed-parameter-value' )
        keys = get_soup_text(keys)
        values = get_soup_text(values)
        result = set_dict(keys, values)
    
        # pprint(result)
        
        return result
    return {'None':'None'}

def  get_spec_alt(soup : BeautifulSoup) -> dict:
    keys   = soup.find_all( 'th')
    values = soup.find_all( 'td')
    keys = get_soup_text(keys)
    values = get_soup_text(values)
    result = set_dict(keys, values)

    # pprint(result)
    
    return result

def get_name(soup : BeautifulSoup) -> str:
    try:
        name =  soup.find('p', class_='font-opensans product-title').get_text('|', strip=True)
    except Exception:
        try:
            name =  soup.find('span', class_='parent').get_text('|', strip=True)
        except Exception:
            name = 'None'
    
    return name

def get_content(soup : BeautifulSoup, listColumns : list, href: str, img_href : str, net_href : str) -> pd.DataFrame:
    tag = 'DJI'
    brand = 'DJI'    
    name = get_name( soup )
    price = 'None'
    
    try:
        specifications = get_spec(soup)
        if specifications == {'None':'None'} : specifications = get_spec_alt(soup)
    except Exception:
        try:
            specifications = get_spec_alt(soup)
        except Exception:
            specifications = {'None':'None'}
        
    
    return pd.DataFrame([href ,tag, brand, name, price, specifications, img_href, net_href], index = listColumns)

def get_emptyDataframe( listColoms : list) -> pd.DataFrame:
    df = pd.DataFrame(dict(zip(listColoms, []*len(listColoms))))
    return df

def make_jsonFile( df : pd.DataFrame, strFileName : str, strOrient = 'records'):
    path = __file__[:__file__.rfind('\\')] + '\\' + strFileName + '.json'
    with open(  path,'w', encoding='utf-8') as file:
        isWrited = file.write(df.to_json(force_ascii=False, indent=3, orient=strOrient))
        if isWrited : print(f'Successfully recorded in {path}')

def get_main_href(href : str) -> str:
    index = [i for i in range(len(href)) if href.startswith('/', i)]
    return href[:index[2]]

# def get_href()

def get_images(soup : BeautifulSoup) -> list:
    soup = get_currentPart(soup, 'div', 'product-item')
    listHrefs = []
    for link in soup.find_all('figure'):
        listHrefs.append(link.get("data-layzr")[2:] )
    return listHrefs

def main() -> pd.DataFrame:
    listZeroPages_url = [
                        'https://www.dji.com/ru/products/camera-drones?site=brandsite&from=nav',
                        'https://www.dji.com/ru/products/handheld-imaging-devices?site=brandsite&from=nav'
                    ]

    # listColumns = ['href','tag', 'brand', 'name','price','specifications']
    listColumns = ['href','tag', 'brand', 'name','price','specifications', 'img_href', 'net_href']
    
    dfGeneral = get_emptyDataframe(listColumns) # Создаём пустой pd.dataframe с столбцами из listColumns

    for zeropage_url in listZeroPages_url:
        soup = get_soup(zeropage_url)
        net_href = get_main_href(zeropage_url) # Получаем "основную" ссылку 
        hrefs = get_hrefs( soup )
        hrefs = list(set(hrefs))
        hrefs.remove('https://www.dji.com/ru/where-to-buy')
        imges_hrefs = get_images( soup )
        hrefs = separate_href( hrefs )

        # https://www.dji.com/ru/
        # /specs
        
        for href in hrefs:
            current_url = href + "/specs"
            soup = get_soup(current_url)
            index = hrefs.index(href)
            df = get_content( soup, listColumns, current_url, imges_hrefs[index], net_href )
            df = df.transpose()
            dfGeneral = pd.concat([dfGeneral, df])
            
    
    
    return dfGeneral

print(f'{__name__} is here !')

if __name__ == '__main__': 
    make_jsonFile( main(), 'data_dji')
    
    


'''import requests
from bs4 import BeautifulSoup
import pandas as pd
import unicodedata
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
    # try:
        for iteration in range( len(HTTPS_PROXIES) ):
            proxy_servers = get_proxy()
            
            try:
                response = requests.get(strURL, proxies=proxy_servers, timeout=5)
                code = response.status_code
            except Exception:
                code = -1
                
            if code == 200:
                print('Status code :', response.status_code, 'for', strURL, 'by', proxy_servers['http'])
                soup = BeautifulSoup(response.text, PARSING_MOD) 
                return soup
            else:
                response = requests.get(strURL)
                if response.status_code == 200:
                    print('Status code :', response.status_code, 'for', strURL, 'by self ip', )
                    soup = BeautifulSoup(response.text, PARSING_MOD) 
                    return soup
    # except:
    #     print("Connection error")
           
    
def get_currentPart(soup : BeautifulSoup, strTagName : str, strClassName : str) -> BeautifulSoup: 
    soup_copy = soup
    soup_copy = soup.findAll(strTagName, class_=strClassName)  
    return BeautifulSoup(str(soup_copy), PARSING_MOD)

def get_hrefs( soup : BeautifulSoup) -> list:
    soup = get_currentPart(soup, 'div', 'product-item')
    listHrefs = []
    for link in soup.find_all('a'):
        listHrefs.append(link.get('href'))
    return list(set(listHrefs))

def separate_href(hrefs : list) -> list : 
    result = []
    for href in hrefs:
        result.append( href.split('?')[0] )
    return result

def normolize_list_text(list_text : list) -> list:
    result = []
    for item in list_text:
        result = unicodedata.normalize("NFKD", item)
    return result

def get_soup_text( list_soups : list) -> list: 
    result = []
    for soup in list_soups:
        text = soup.get_text('/n', strip=True)
        text = unicodedata.normalize("NFKD", text)
        result.append( text )
    return result

def set_dict(keys : list, values : list) -> dict:
    result = {}
    for i in range( len(keys) ):
        result[keys[i]] = values[i]
    return result

def get_spec(soup : BeautifulSoup) -> dict:
    keys   = soup.find_all( 'li', class_='detailed-parameter-key' )
    if len(keys) != 0:
        values = soup.find_all( 'div', class_='detailed-parameter-value' )
        keys = get_soup_text(keys)
        values = get_soup_text(values)
        result = set_dict(keys, values)        
        return result
    return {'None':'None'}

def  get_spec_alt(soup : BeautifulSoup) -> dict:
    keys   = soup.find_all( 'th')
    values = soup.find_all( 'td')
    keys = get_soup_text(keys)
    values = get_soup_text(values)
    result = set_dict(keys, values)
    return result

def get_name(soup : BeautifulSoup) -> str:
    try:
        name =  soup.find('p', class_='font-opensans product-title').get_text('|', strip=True)
    except Exception:
        try:
            name =  soup.find('span', class_='parent').get_text('|', strip=True)
        except Exception:
            name = 'None'
    return name

def get_content(soup : BeautifulSoup, listColumns : list, href: str, img_href : str, net_href : str) -> pd.DataFrame:
    tag = 'DJI'
    brand = 'DJI'    
    name = get_name( soup )
    price = 'None'
    
    try:
        specifications = get_spec(soup)
        if specifications == {'None':'None'} : specifications = get_spec_alt(soup)
    except Exception:
        try:
            specifications = get_spec_alt(soup)
        except Exception:
            specifications = {'None':'None'}
        
    
    return pd.DataFrame([href ,tag, brand, name, price, specifications, img_href, net_href], index = listColumns)

def get_emptyDataframe( listColoms : list) -> pd.DataFrame:
    df = pd.DataFrame(dict(zip(listColoms, []*len(listColoms))))
    return df

def make_jsonFile( df : pd.DataFrame, strFileName : str, strOrient = 'records'):
    path = __file__[:__file__.rfind('\\')] + '\\' + strFileName + '.json'
    with open(  path,'w', encoding='utf-8') as file:
        isWrited = file.write(df.to_json(force_ascii=False, indent=3, orient=strOrient))
        if isWrited : print(f'Successfully recorded in {path}')

def get_main_href(href : str) -> str:
    index = [i for i in range(len(href)) if href.startswith('/', i)]
    return href[:index[2]]

def get_images(soup : BeautifulSoup) -> list:
    soup = get_currentPart(soup, 'div', 'product-item')
    listHrefs = []
    for link in soup.find_all('figure'):
        listHrefs.append(link.get("data-layzr")[2:] )
    return listHrefs

def getlistEqualPartsOfNumberParts(intNub : int, intParts : int) -> list:
  # Функция разбиения на равные части 
  d, r = divmod(intNub, intParts)
  return [d + (1 if i < r else 0) for i in range(intParts)]

def fill_list(current_list : list, item, to_count : int) -> list:
    result = current_list
    for i in range( len( current_list ),  to_count):
        result.append(item)
    return result

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
    return cache_df

def start_demons(list_threads : list) -> None:
    # Функция запуска потоков в фоне (демонов)
    for thread in list_threads:
       thread.start()

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

def main() -> pd.DataFrame:
    listZeroPages_url = [
                        'https://www.dji.com/ru/products/camera-drones?site=brandsite&from=nav',
                        'https://www.dji.com/ru/products/handheld-imaging-devices?site=brandsite&from=nav'
                    ]
    listColumns = ['href','tag', 'brand', 'name','price','specifications', 'img_href', 'net_href']    
    
    cache_hrefs  = []
    cache_images = []

    for zeropage_url in listZeroPages_url:
        soup = get_soup(zeropage_url)
        net_href = get_main_href(zeropage_url) # Получаем "основную" ссылку 
        hrefs = get_hrefs( soup )
        
        try:
            hrefs.remove('https://www.dji.com/ru/where-to-buy')
        except Exception:
            pass
        hrefs   = separate_href( hrefs )
        imges_hrefs = get_images( soup )
        imges_hrefs = fill_list(imges_hrefs, 'www2.djicdn.com/cms/uploads/3f953b382abf679144358de6bdc84ac9.png', len( hrefs ))
        
        
        cache_images.extend( imges_hrefs )
        cache_hrefs.extend (    hrefs    )

        # https://www.dji.com/ru/
        # /specs
        
    list_threads = []
    slice_start = 0
    parts = getlistEqualPartsOfNumberParts( len(cache_hrefs), COUNT_THREADS)
    parts[-1] = parts[-1] - 1 
    for i in range( len(parts) ):
        list_threads.append( CustomThread(    
                                          th_parsing ,  
                                          listColumns ,
                                          cache_hrefs[slice_start : slice_start + parts[i]+1] ,
                                          cache_images[slice_start : slice_start + parts[i] + 1] ,
                                          net_href                
                                        ) 
                            )
        print(slice_start, slice_start + parts[i])
        slice_start += parts[i]
        
        
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
    make_jsonFile(main(), 'data_dji')
    

'''