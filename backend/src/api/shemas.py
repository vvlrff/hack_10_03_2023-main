from pydantic import BaseModel,Json
from datetime import datetime
from typing import Any, Dict, List
class RawData(BaseModel):
    
    id_data : int 
    country : str 
    category : str 
    name : str 
    brand : str 
    price : str | int
    created_at : datetime
    update_at : datetime
    specifications : Dict |  str | List | None
    url : str 
    img_href : str
    net_href : str
    class Config:
            orm_mode = True
            
class Log_changes(BaseModel):
    id_changes : int
    dite_changes : datetime
    log_change : str
    class Config :
        orm_mode = True