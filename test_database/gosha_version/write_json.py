from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import Raw_Data, Country, Site, Category

import json
from psycopg2.extras import Json
from psycopg2.extensions import register_adapter
from sshtunnel import SSHTunnelForwarder

register_adapter(dict, Json)

with SSHTunnelForwarder(
    ('ovz1.j77761203.0pjxn.vps.myjino.ru', 49430), #Remote server IP and SSH port
    ssh_username = "root",
    ssh_password = "918808722",
    remote_bind_address=('127.0.0.1', 5432)) as server: #PostgreSQL server IP and sever port on remote machine
        
    server.start() #start ssh sever
    print ('Server connected via SSH')
    
    #connect to PostgreSQL
    local_port = str(server.local_bind_port)
    engine = create_engine('postgresql://team_hack:hack@127.0.0.1:' + local_port +'/hack_db', echo=True)

    session = sessionmaker(bind=engine)
    s = session()


    def get_json(path):
        with open(path, 'r', encoding='utf-8') as f:
            list_ = []
            try:
                my_data = json.load(f)  
                
                for row in my_data:

                    list_.append(Raw_Data(country='Germany',category=row["tag"],name=row["name"],brand=row["brand"],
                                        price=row["price"],specification=row["specifications"],url='in progress',site='https://www.banggood.com'))
                
                s.add_all(list_)
                s.commit()
                
            except BaseException as e:
                print(e)

                print('The file contains invalid JSON')
        




    path = 'data.json'
    get_json(path)

    for i in s.query(Raw_Data.specification):
        for j in i:
            print(j)