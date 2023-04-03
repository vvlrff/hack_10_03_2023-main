from sqlalchemy import JSON, create_engine, DateTime,Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_utils import database_exists, create_database
from sshtunnel import SSHTunnelForwarder

import datetime

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
    Base = declarative_base()


    class Raw_Data(Base):
        __tablename__ = 'raw_data'
        id_data = Column(Integer, primary_key=True)
        country = Column(String)
        category = Column(String)
        name = Column(String)
        brand = Column(String)
        price = Column(String)
        data = Column(DateTime, default=datetime.datetime.now)
        specification = Column(JSON)
        url = Column(String)
        site = Column(String)


    class Country(Base):
        __tablename__ = 'country'
        id_country = Column(Integer, primary_key=True)
        region = Column(String)
        name = Column(String)
        site = Column(String)


    class Site(Base):
        __tablename__ = 'site'
        id_site = Column(Integer, primary_key=True)
        name  = Column(String)
        


    class Category(Base):
        __tablename__ = 'category'
        id_category = Column(Integer, primary_key=True)
        name = Column(String)


    if __name__ == "__main__": 
        Base.metadata.create_all(engine)
        
        

#engine = create_engine('postgresql+psycopg2://team_hack:hack@ovz1.j77761203.0pjxn.vps.myjino.ru/hack_db')

# from sshtunnel import SSHTunnelForwarder #Run pip install sshtunnel
# from sqlalchemy.orm import sessionmaker #Run pip install sqlalchemy
# from sqlalchemy import create_engine

# with SSHTunnelForwarder(
#     ('<remote server ip>', 22), #Remote server IP and SSH port
#     ssh_username = "<username>",
#     ssh_password = "<password>",
#     remote_bind_address=('<local server ip>', 5432)) as server: #PostgreSQL server IP and sever port on remote machine
        
#     server.start() #start ssh sever
#     print 'Server connected via SSH'
    
#     #connect to PostgreSQL
#     local_port = str(server.local_bind_port)
#     engine = create_engine('postgresql://<username>:<password>@127.0.0.1:' + local_port +'/database_name')

#     Session = sessionmaker(bind=engine)
#     session = Session()
    
#     print 'Database session created'
    
#     #test data retrieval
#     test = session.execute("SELECT * FROM database_table")
#     for row in test:
#         print row['id']
        
#     session.close()