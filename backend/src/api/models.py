from sqlalchemy import DateTime, MetaData, Table, Column, Integer, String, JSON
import datetime

metadata = MetaData()



raw_data = Table(
    'raw_data',
    metadata,
    Column('id_data', Integer, primary_key=True),
    Column('country', String),
    Column('category', String),
    Column('name', String),
    Column('brand', String),
    Column('price', String),
    Column('created_at', DateTime, default=datetime.datetime.now),
    Column('update_at', DateTime, default=datetime.datetime.now),
    Column('specifications', JSON),
    Column('url', String),
    Column('img_href', String),
    Column('net_href', String),
)

log_changes = Table(
    'log_changes',
    metadata,
    Column('id_changes', Integer, primary_key=True),
    Column('dite_changes',DateTime, default=datetime.datetime.now),
    Column('log_change',String)
)