from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
import os 

from . import pars_banggood, parsing_drone, aeromotus, dji, geobox, nelik
from . import utils 
from src.datebase import get_async_session
dir_path = os.path.dirname(os.path.realpath(__file__))

router = APIRouter (
    prefix='/pars',
    tags= ['pars']
)

@router.get("/pars_Germany_banggood")
async def pars_germany(session: AsyncSession = Depends(get_async_session)):
    pars_banggood.main()
    await utils.find_differeces(dir_path +''+'\\data_Germany_.json',session)    
    return {'msg': 'parsing complite'}



@router.get("/pars_Turkey_drone")
async def pars_turkey_(session: AsyncSession = Depends(get_async_session)):
    parsing_drone.main()
    await utils.find_differeces(dir_path +''+'\\data_Turkey_.json',session)
    return {'msg': 'parsing complite'}

@router.get("/pars_Russian_dji")
async def pars_DJI_(session: AsyncSession = Depends(get_async_session)):
    dji.main()
    await utils.find_differeces(dir_path +''+'\\data_USA_.json',session)
    return {'msg': 'parsing complite'}


@router.get("/pars_Russian_aeromotus")
async def Russian_aeromotus(session: AsyncSession = Depends(get_async_session)):
    aeromotus.main()
    await utils.find_differeces(dir_path +''+'\\data_Russian_.json',session)    
    return {'msg': 'parsing complite'}

@router.get("/pars_Russian_nelik")
async def pars_Russian_nelik(session: AsyncSession = Depends(get_async_session)):
    nelik.main()
    await utils.find_differeces(dir_path +''+'\\data_Russian_nelik.json',session)
    return {'msg': 'parsing complite'}