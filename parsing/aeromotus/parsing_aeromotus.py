import requests
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
import unicodedata

PARSING_MOD = "html5lib"

def get_soup(strURL : str) -> BeautifulSoup:
    try:
        response = requests.get(strURL)
        print('Status code :', response.status_code, 'for', strURL)
    except:
        print("Connection error")
    soup = BeautifulSoup(response.text, PARSING_MOD) 
    return soup        

def get_currentPart(soup : BeautifulSoup, strTagName : str, strClassName : str) -> BeautifulSoup: 
    soup_copy = soup
    soup_copy = soup.findAll(strTagName, class_=strClassName)  
    return BeautifulSoup(str(soup_copy), PARSING_MOD)

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

def get_pageCount(soup : BeautifulSoup) -> int:
    case = soup.find('ul', class_='page-numbers') 
    text = case.get_text('|', strip=True).split('|')[-2]
    return  int(text)

def get_items_hrefs( soup : BeautifulSoup ) -> list:
    soup = get_currentPart(soup, 'div', 'product-loop-header product-item__header')
    listHrefs = []
    for link in soup.find_all('a', class_='woocommerce-LoopProduct-link woocommerce-loop-product__link'):
        listHrefs.append(link.get('href'))
    return listHrefs

def get_tag_and_name( soup : BeautifulSoup ) -> str:
    tags = soup.find("nav", class_="woocommerce-breadcrumb")
    list_tags = []
    for tag in tags:
        text = tag.get_text("|", strip=True)
        if text != '':
            list_tags.append( tag.get_text("|", strip=True) )
        
    return list_tags[-2], list_tags[-1]

def get_img_href( soup : BeautifulSoup ) -> str:
    soup = get_currentPart(soup, 'div', 'flex-viewport')
    listHrefs = []
    for link in soup.find_all('a'):
        listHrefs.append(link.get('href'))
    return listHrefs

def get_spec(soup : BeautifulSoup) -> dict:
    soup = get_currentPart(soup, 'div', 'woocommerce-Tabs-panel woocommerce-Tabs-panel--specification panel entry-content wc-tab')
    
    keys   = soup.find_all( 'th')
    if len(keys) != 0:
        values = soup.find_all( "td" )
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

def get_content(soup : BeautifulSoup, listColumns : list,  href: str,  net_href : str, price : int, img_href : str) -> pd.DataFrame:
    tag, name = get_tag_and_name( soup )
    
    brand = 'None'    
    
    specifications = get_spec(soup)
        
    return pd.DataFrame([href ,tag, brand, name, str(price), specifications, img_href, net_href], index = listColumns)

def get_prices(soup : BeautifulSoup) -> list:
    soup = get_currentPart(soup, 'span', 'price')
    
    for link in soup: # .find_all('bdi')
        price = link.get_text("", strip=True).replace('[','').replace(']','').replace('₽','').split(',')
        for i in range( len(price) ):
            if price[i] == '' :
                price[i] = 'None'
            else:
                price[i] = (price[i].replace(' ', ''))
                
                if len(price[i]) > 7:
                    price[i] = price[i][: len(price[i])//2 ]
                
                price[i] = int(price[i])
                
        return price

def get_images( soup : BeautifulSoup) -> list:
    listHrefs = []
    soup = soup.find_all('div', class_='product-thumbnail product-item__thumbnail')
    i = len( soup )
    for item in soup:
        content = item.find('img').get('data-src')
        if ('jpg' in content) or ('png' in content) or ('webp' in content) or ('jpeg' in content) : listHrefs.append( content )
    if listHrefs[0] == 0 : 
        return listHrefs[1:]
    return listHrefs

def main() -> pd.DataFrame:
    listZeroPages_url = [
                        "https://aeromotus.ru/shop/" # -> https://aeromotus.ru/shop/page/22/
                        ]

    listColumns = ['href','tag', 'brand', 'name','price','specifications', 'img_href', 'net_href']
    
    dfGeneral = get_emptyDataframe(listColumns) # Создаём пустой pd.dataframe с столбцами из listColumns
    
    for zeropage_url in listZeroPages_url: # Нулевая страница 
        soup = get_soup(zeropage_url)
        last_page = get_pageCount( soup )  # Получаем количество подстраниц
        net_href = get_main_href(zeropage_url) # Получаем "основную" ссылку 
        for index in range ( 1, last_page):
            soup = get_soup(zeropage_url  + "page" + '/' + str( index ) + '/')
            list_items_hrefs = get_items_hrefs( soup )
            prices = get_prices( soup )
            images = get_images( soup )
            
            for items_href in list_items_hrefs:
                index = list_items_hrefs.index( items_href )
                soup = get_soup(items_href)
                df = get_content( soup, listColumns, items_href, net_href, prices[index], images[index] )
                df = df.transpose()
                dfGeneral = pd.concat([dfGeneral, df])

    return dfGeneral
    
print(f'{__name__} is here !')

if __name__ == '__main__': 
    make_jsonFile( main(), 'data_aeromotus')
    
    
