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
    soup = BeautifulSoup(response.text, PARSING_MOD) # "html.parser"
    return soup        

def get_currentPart(soup : BeautifulSoup, strTagName : str, strClassName : str) -> BeautifulSoup: 
    soup_copy = soup
    soup_copy = soup.findAll(strTagName, class_=strClassName)  
    return BeautifulSoup(str(soup_copy), PARSING_MOD)

def get_hrefs( soup : BeautifulSoup, tag : str, class_ : str, item_tag : str, item : str) -> list:
    soup = get_currentPart(soup, tag, class_)
    listHrefs = []
    for link in soup.find_all(item_tag):
        listHrefs.append(link.get(item))
        # break
    hrefs = list(set(listHrefs))
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

def set_dict(keys : list, values : list) -> dict:
    result = {}
    for i in range( len(keys) ):
        if values[i] != '':
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
    try:
        case = soup.find('div', class_='nums') 
        text = case.get_text('|', strip=True).split("|")[-1]
        return  int(text)
    except Exception:
        return 2

def get_prices(soup : BeautifulSoup) -> list:
    soup = get_currentPart(soup, 'td', 'information_wrapp main_item_wrapper')
    listHrefs = []
    for link in soup.find_all("span"):
        listHrefs.append(link.get_text('|', strip=True))
        # break
    hrefs = list(set(listHrefs))
    return listHrefs

def get_item_tag(soup : BeautifulSoup) -> str:
    cells = soup.find_all( "span" , attrs={'itemprop':'name'})
    tags = []
    for item in cells[:-1]:
        tags.append( item.get_text('|', strip=True) )
    return tags[-2]

def get_item_price(soup : BeautifulSoup) -> str:
    cell = soup.find("div", class_="price")
    
    try:
        cell = cell.get('data-value')
    except Exception:
        cell = 'None'
    return cell

def drop_zero_values(content : dict)-> dict:
    for key in content.keys:
        if content[key] == '':
            del content[key]

def get_spec(soup : BeautifulSoup) -> dict:
    cells = soup.find('table', class_='colored_table')
    if len(cells) == 0:
        return  {'None':'None'}
    cells = cells.find('tbody')
    cells = cells.find_all('tr')
    # cell = cell.get_text('|', strip=True).split('|')
    keys = []
    values = []
    
    for cell in cells:
        items = cell.get_text('|', strip=True).split('|')
        keys.append( items[0] )
        
        value = ''
        for i in range(1, len(items) ):
            
            if (items[i]).isdigit() == False : value += items[i] + "\n"
        values.append( value )    
    
    try:
        return set_dict(keys, values)
    except Exception:
        return {'None':'None'}


def  get_spec_alt(soup : BeautifulSoup) -> dict:
    cells = soup.find('ul', class_='tabs_content tabs-body')
    if len(cells) == 0:
        return  {'None':'None'}
    cells = cells.find('tbody')
    try:
        cells = cells.find_all('tr')
    except:
        return  {'None':'None'}
    
    keys = []
    values = []
    
    for cell in cells:
        items = cell.get_text('|', strip=True).split('|')
        keys.append  ( items[0] )
        if len(items[1:]) == 1:
            values.append( items[1])        
        else:
            values.append( items[1:])        
    try:
        return set_dict(keys, values)
    except Exception:
        return {'None':'None'}

def get_item_img(soup : BeautifulSoup, net_href : str) -> str:
    cell = soup.find('div', class_="slides")
    cell = cell.find('img').get('src')
    return net_href + cell

def get_content(soup : BeautifulSoup, listColumns : list, href: str, net_href : str) -> pd.DataFrame:
    tag = get_item_tag(soup)
    name = soup.find("h1", attrs={'id':"pagetitle"}).get_text('|', strip=True)
    brand = 'НЕЛК'

    price = get_item_price(soup)
    
    try:
        specifications = get_spec(soup)
        
    except Exception:
        specifications = {'None':'None'}
        
    if specifications == {'None':'None'} : specifications = get_spec_alt(soup)
    
    img_href = get_item_img(soup, net_href)
    
    # drop_zero_values(specifications)
    
    return pd.DataFrame([href ,tag, brand, name, price, specifications, img_href, net_href], index = listColumns)

def main():
    listZeroPages_url = [
                        "https://nelk.ru/catalog/"
                    ]

    listColumns = ['href','tag', 'brand', 'name','price','specifications', 'img_href', 'net_href']
    
    dfGeneral = get_emptyDataframe(listColumns) # Создаём пустой pd.dataframe с столбцами из listColumns

    for zeropage_url in listZeroPages_url:
        soup = get_soup(zeropage_url)
        net_href = get_main_href(zeropage_url) # Получаем "основную" ссылку 
        hrefs = get_hrefs( soup , 'li', 'name', 'a', 'href')
        for href in hrefs:
            current_url = net_href + href
            soup = get_soup(current_url)
            last_page = get_pageCount( soup )  # Получаем количество подстраниц
            for index in range(1, last_page):
                current_url = net_href + href  + "?PAGEN_1=" + str(index)
                # imges_hrefs = get_hrefs ( soup , 'div', 'image_wrapper_block', "img", 'src')
                item_hrefs       = get_hrefs ( soup , 'div', 'image_wrapper_block',  'a', 'href')
                # prices      = get_prices(soup)
                for item_href in item_hrefs:
                    current_url = net_href + item_href
                    soup = get_soup(current_url)
                    df = get_content( soup, listColumns, current_url, net_href )
                    df = df.transpose()
                    dfGeneral = pd.concat([dfGeneral, df])
                
    make_jsonFile( dfGeneral, 'data_Russian_nelik')
    # return dfGeneral
        
# print(f'{__name__} is here !')
        
# if __name__ == '__main__': 
#     make_jsonFile( main(), 'data_Russian_nelik')
