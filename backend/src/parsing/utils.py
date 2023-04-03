import datetime
from ..api.models import raw_data, log_changes

import json
from sqlalchemy import insert, select, update

async def add_new_note_raw_data(new_note_for_row_data, s):

    element_href = new_note_for_row_data[0]
    print(element_href)
    new_tag = new_note_for_row_data[1]
    new_name = new_note_for_row_data[2]
    new_brand = new_note_for_row_data[3]
    new_price = new_note_for_row_data[4]
    new_specifications = new_note_for_row_data[5]
    new_img_href = new_note_for_row_data[6]
    new_net_href = new_note_for_row_data[7]

    if 'aeromotus.ru' in element_href:
        new_country = 'Russian'
    if 'www.drone.net.' in element_href:
        new_country = 'Turkey'
    if 'www.banggood.com' in element_href:
        new_country = 'Germany'
    if 'www.dji.com' in element_href:
        new_country = 'Russian'
    if 'nelk.ru' in element_href:
        new_country = 'Russian'
    # else:
    #     new_country = 'none'

    stmt_for_new_note = insert(raw_data).values(country=new_country,category=new_tag, name=new_name, brand=new_brand, price=new_price, specifications=new_specifications, url=element_href, img_href=new_img_href, net_href=new_net_href)
    await s.execute(stmt_for_new_note)
    await s.commit()
    
    # text_for_new_row =
    print('New note was added to raw_data')


async def write_to_database_log_changes(text_changes, s):
    await s.execute(insert(log_changes).values(log_change=text_changes))
    await s.commit()
    print('Completed')


async def update_database_raw_data(ls_for_updating, s):
    element_href = ls_for_updating[0]
    new_tag = ls_for_updating[1]
    new_name = ls_for_updating[2]
    new_brand = ls_for_updating[3]
    new_price = ls_for_updating[4]
    new_specifications = ls_for_updating[5]
    new_time = datetime.datetime.now()

    if new_tag:
        s.execute(update(raw_data).where(raw_data.c.url == element_href).values(category = new_tag, update_at = new_time))
    if new_name:
        s.execute(update(raw_data).where(raw_data.c.url == element_href).values(name = new_name, update_at = new_time))
    if new_brand:
        s.execute(update(raw_data).where(raw_data.c.url == element_href).values(brand = new_brand, update_at = new_time))
    if new_price:
        s.execute(update(raw_data).where(raw_data.c.url == element_href).values(price = new_price, update_at = new_time))
    if new_specifications:
        s.execute(update(raw_data).where(raw_data.c.url == element_href).values(specifications = new_specifications, update_at = new_time))
    
    
    
    await s.commit()


async def find_differeces(filename, s):

    with open(filename, 'r', encoding='utf-8') as file:
        new_data = json.load(file)

    for element in new_data:
        element_href = element['href']
# / НО ессли с моим кодом то 
        result = await s.execute(select(raw_data).filter(raw_data.c.url.like(element_href)).limit(1))
        # result = s.query(raw_data).filter(raw_data.c.url.like(element_href)).first()/ а то он дает пустой список и у тебя код для пустого списка работает вот этот 
        result = result.all()

        # print(result)
        if result == []:
            
            new_note_for_row_data = [element['href'], element['tag'], element['name'], element['brand'], str(element['price']), element['specifications'], element['img_href'], element['net_href']]
            await add_new_note_raw_data(new_note_for_row_data, s)
            continue

        lil_dict_result = {'href': result[0][9], 'tag': result[0][2], 'name': result[0][3], 'brand': result[0][4], 'price': str(result[0][5]), 'specifications':  result[0][8]}
        lil_element = {'href': element['href'], 'tag': element['tag'], 'name': element['name'], 'brand': element['brand'], 'price': str(element['price']), 'specifications': element['specifications']}
        
        if lil_dict_result == lil_element:
            continue

        else:
            changes_line = 'Difference found in element with url: ' + lil_element['href'] + '\n'
            new_tag = ''
            new_name = ''
            new_brand = ''
            new_price = ''
            specifications_changes_flag = False

            # print()
            # print('Difference found in element with url:', lil_element['href'])

            if lil_dict_result['tag'] != lil_element['tag']:
                # print('Old tag:', lil_dict_result['tag'])
                # print('New tag:', lil_element['tag'])

                changes_line += 'Old tag: ' + lil_dict_result['tag'] + '\nNew tag: ' + lil_element['tag'] + '\n'
                new_tag = lil_element['tag']

            if lil_dict_result['name'] != lil_element['name']:
                # print('Old name:', lil_dict_result['name'])
                # print('New name:', lil_element['name'])

                changes_line += 'Old name: ' + lil_dict_result['name'] + '\nNew name: ' + lil_element['name'] + '\n'
                new_name = lil_element['name']

            if lil_dict_result['brand'] != lil_element['brand']:
                # print('Old brand:', lil_dict_result['brand'])
                # print('New brand:', lil_element['brand'])

                changes_line += 'Old brand: ' + lil_dict_result['brand'] + '\nNew brand: ' + lil_element['brand'] + '\n'
                new_brand = lil_element['brand']

            if str(lil_dict_result['price']) != str(lil_element['price']):
                # print('Old price:', lil_dict_result['price'])
                # print('New price:', lil_element['price'])

                changes_line += 'Old price: ' + str(lil_dict_result['price']) + '\nNew price: ' + str(lil_element['price']) + '\n'
                new_price = lil_element['price']

            if lil_dict_result['specifications'] != lil_element['specifications']:
                #print('Difference found in specifications')

                for key in lil_element['specifications']:
                    try:
                        if lil_dict_result['specifications'][key] != lil_element['specifications'][key]:
                            # print('Old {} (specifications): {}'.format(key, lil_dict_result['specifications'][key]))
                            # print('New {} (specifications): {}'.format(key, lil_element['specifications'][key]))

                            changes_line += 'Old {} (specifications): {}'.format(key, lil_dict_result['specifications'][key]) + '\n' + 'New {} (specifications): {}'.format(key, lil_element['specifications'][key])
                            new_specifications = lil_dict_result['specifications']
                            new_specifications[key] = lil_element['specifications'][key]
                            specifications_changes_flag = True

                    except KeyError:
                        # print('New value was found in specifications: ')
                        # print('{}: {}'.format(key, lil_element['specifications'][key]))

                        changes_line += 'Difference found in specifications' + '\nNew value was found in specifications: ' + '{}: {}'.format(key, lil_element['specifications'][key]) + '\n'
                        new_specifications = lil_dict_result['specifications']
                        new_specifications[key] = lil_element['specifications'][key]
                        specifications_changes_flag = True

            ls_for_updating = [element_href, new_tag, new_name, new_brand, new_price]

            if specifications_changes_flag:
                ls_for_updating.append(new_specifications)
            else:
                ls_for_updating.append(None)

            await update_database_raw_data(ls_for_updating, s)
            await write_to_database_log_changes(changes_line, s)
