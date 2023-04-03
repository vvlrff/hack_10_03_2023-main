import requests
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
import unicodedata
import re
import time

PARSING_MOD = "lxml"


def get_emptyDataframe( listColoms : list) -> pd.DataFrame:
    df = pd.DataFrame(dict(zip(listColoms, []*len(listColoms))))
    return df

def get_soup(strURL : str) -> BeautifulSoup:
    try:
        time.sleep(0.5)
        response = requests.get(strURL)
        print('Status code :', response.status_code, 'for', strURL)
    except:
        print("Connection error", 'for', strURL)
    soup = BeautifulSoup(response.text, PARSING_MOD) # "html.parser"
    return soup     

def get_currentPart(soup : BeautifulSoup, strTagName : str, strClassName : str) -> BeautifulSoup: 
    soup_copy = soup
    soup_copy = soup.findAll(strTagName, class_=strClassName)  
    return BeautifulSoup(str(soup_copy), PARSING_MOD)

def make_jsonFile( df : pd.DataFrame, strFileName : str, strOrient = 'records'):
    path = __file__[:__file__.rfind('\\')] + '\\' + strFileName + '.json'
    with open(  path,'w', encoding='utf-8') as file:
        isWrited = file.write(df.to_json(force_ascii=False, indent=3, orient=strOrient))
        if isWrited : print(f'Successfully recorded in {path}')

def get_hrefs( soup : BeautifulSoup, tag : str, class_ : str) -> list:
    soup = get_currentPart(soup, tag, class_)
    listHrefs = []
    for link in soup.find_all('a'):
        listHrefs.append(link.get('href'))
    listHrefs = list(set(listHrefs))
    return listHrefs

def get_main_href(href : str) -> str:
    index = [i for i in range(len(href)) if href.startswith('/', i)]
    return href[:index[2]]

# def get_images_hrefs( soup : BeautifulSoup, main_href : str, tag : str, class_ : str ) -> list:
#     soup = get_currentPart( soup,  tag, class_ )
#     listImagesHrefs = []
#     counter = 0 
#     for link in soup.find_all('img'):
#         img_href =  main_href + link.get('src') # 	https://geobox.ru/include/logo2.png
#         if img_href == main_href : 
#             img_href = "https://geobox.ru/include/logo2.png"
        
#         listImagesHrefs.append( img_href )
#     listImagesHrefs = list(set(listImagesHrefs))
#     if len(listImagesHrefs) == 0: listImagesHrefs[0] = "https://geobox.ru/include/logo2.png"
#     return listImagesHrefs

def get_tag_and_hrefs( soup : BeautifulSoup,  tag : str, class_ : str ) -> list:
    soup = get_currentPart( soup,  tag, class_ )
    listHrefs = []
    listTags  = []
    for link in soup.find_all('a'):
        listHrefs.append(link.get('href'))
        text = link.get_text('|', strip=True)
        if text != '' : listTags.append(text) 
        
    listHrefs = list(set(listHrefs))
    return listHrefs, listTags

# def get_spec(soup : BeautifulSoup, tag : str) -> dict:
#     lines = []
#     cells = soup.find_all( 'td')
#     if len(cells) != 0:
#         for cell in cells:
#             lines.append( cell.get_text('|', strip=True) )   
        
#         specifications = {}
        
#         for i in range( 0,len(lines),2 ):
#             specifications[ lines[i] ] = specifications[i+1]
        
#         if len(specifications) == 0 : 
#             return {}
#         else:
#             return specifications
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
    
    keys = soup.find_all( 'th')
    keys = get_soup_text(keys)
    if len(keys) != 0 and keys[0] != '':
        values = soup.find_all( 'td')
        values = get_soup_text(values)
        result = set_dict(keys, values)
        return result
    elif len(keys) != 0 and keys[0] == '':
        result = {}
        values = soup.find_all( 'td')
        values = get_soup_text(values)
        
        for i in range( 0,len(values),2 ):
            result[i] = values[i+1]
        return result
    
    return 'None'

def get_content(soup : BeautifulSoup, listColumns : list, tag : str, name : str, href: str, img_href : str, net_href : str) -> pd.DataFrame:
    brand = 'None'    

    try:
        price = soup.find('span', class_ = 'c-prices__value js-prices_pdv_BASE c-prices__value_red c-prices__value_black').get_text('|', strip=True)
        price = price.replace(' ', '')
        price = re.findall(r'\d+', price)[0]
    except Exception:
        price = 'None'
    
    specifications = get_spec(soup)
    
    
    if len(specifications) == 0 : 
            specifications = "None"
        
    return pd.DataFrame([href ,tag, brand, name, price, specifications, img_href, net_href], index = listColumns)
    # return [href ,tag, brand, name, price, specifications, img_href, net_href]

def main() -> None:
    listZeroPages_url = [
                        'https://geobox.ru/catalog/'
                        ]

    listColumns = ['href','tag', 'brand', 'name','price','specifications', 'img_href', 'net_href']
    
    dfGeneral = get_emptyDataframe(listColumns) # Создаём пустой pd.dataframe с столбцами из listColumns

    try:
        for zeropage_url in listZeroPages_url: # Нулевая страница 
            soup = get_soup(zeropage_url)
            main_href = get_main_href(zeropage_url)
            type_hrefs = get_hrefs( soup, 'li',  'section col-xs-6 col-md-6 col-md-4 col-lg-5rs')

            # pprint(hrefs)
            # print( len( type_hrefs))
            
            for type_href in type_hrefs: # Страница каталога
                current_url = main_href + type_href            
                soup = get_soup(current_url)
                tag_hrefs, tags = get_tag_and_hrefs( soup, 'li', 'section col-xs-6 col-md-6 col-md-4 col-lg-5rs' )
                # tag_images_href = get_images_hrefs(soup, main_href,'ul', "row list-unstyled")
                
                
                for tag_href in tag_hrefs: # Страница типов
                    tag_index = tag_hrefs.index( tag_href )
                    tag = tags[tag_index]
                    current_url = main_href + tag_href   

                    
                    soup = get_soup(current_url)
                    item_hrefs, item_names = get_tag_and_hrefs( soup, 'div', 'list-showcase__name')
                    
                    
                    for item_href in item_hrefs:
                        item_index = item_hrefs.index( item_href )
                        name = item_names[item_index]
                        current_url = main_href + item_href
                        soup = get_soup(current_url)
                        
                        # df = get_content( soup, listColumns, tag, name, current_url, tag_images_href[tag_index], main_href)
                        df = get_content( soup, listColumns, tag, name, current_url, "https://geobox.ru/include/logo2.png", main_href)
                        df = df.transpose()
                        dfGeneral = pd.concat([dfGeneral, df])
    except Exception:                  
        make_jsonFile( dfGeneral, 'data_geobox')
    finally:
        make_jsonFile( dfGeneral, 'data_geobox')
main()