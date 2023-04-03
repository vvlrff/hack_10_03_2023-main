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
    return 'None'

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
        if specifications == "None" : specifications = get_spec_alt(soup)
    except Exception:
        try:
            specifications = get_spec_alt(soup)
        except Exception:
            specifications = 'None'
    
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

def main() -> None:
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
            
    # make_jsonFile(file_path, dfGeneral, 'data_dji')
    make_jsonFile( dfGeneral, 'data_USA_')
    
