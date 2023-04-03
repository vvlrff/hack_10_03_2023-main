from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy import  create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import File, UploadFile
from fastapi.responses import FileResponse
from ..config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

import pandas as pd
import datetime



DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
Base = declarative_base()


engine = create_engine(DATABASE_URL)
session = sessionmaker(bind=engine)
s = session()

router = APIRouter (
    prefix='/output',
    tags= ['output']
)

@router.get("/get_XlSX")
def create_xlsx_file():
    dt_obj =datetime.datetime.now()
    dt_string = dt_obj.strftime("%d-%b-%Y (%H:%M:%S)")
    print(dt_string)
    total_row_data = pd.read_sql("select * from \"raw_data\"", engine)
    changes_log_data = pd.read_sql("select * from \"log_changes\"", engine)

    with pd.ExcelWriter('parsing.xlsx') as writer:
        total_row_data.to_excel(writer, sheet_name='All Data', index=False)
        changes_log_data.to_excel(writer, sheet_name='Changes', index=False)
    return FileResponse(path='parsing.xlsx',filename=str(dt_string)+':Результат парсинга.xlsx', media_type='multipart/form-data' )
