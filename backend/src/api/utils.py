from .models import raw_data
import json
from sqlalchemy import distinct, insert, select
 
 
async def get_all(session):
    res = await session.execute(select(raw_data).order_by(raw_data.c.created_at))
    return res.all()

async def get_countru(session):
    country_d = distinct(raw_data.c.country)
    res = await session.execute(select(country_d))
    return res.all()
async def get_link_from_country(session, country_input):
    res = await session.execute(select(raw_data.c.net).where(raw_data.c.country == country_input))

async def get_item(session,id):
    res = await session.execute(select(raw_data).where(raw_data.c.id_data == id))
    return res.all()

async def get_items_countru(session,country_input):
    res = await session.execute(select(raw_data).where(raw_data.c.country == country_input))
    return res.all()

async def get_category(session):
    category_d = distinct(raw_data.c.category)
    res = await session.execute(select(category_d))
    return res.all()

async def get_items_category(session, category_input):
    res = await session.execute(select(raw_data).where(raw_data.c.category == category_input))
    return res.all()


async def get_net_href(session):
    category_d = distinct(raw_data.c.net_href)
    res = await session.execute(select(category_d))
    return res.all()


async def get_items_net_href_(session, net_href_input):
    res = await session.execute(select(raw_data).where(raw_data.c.net_href == net_href_input))
    return res.all()