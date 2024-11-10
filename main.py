from fastapi import FastAPI, Depends
from pydantic import BaseModel
from config import *
from models import *
from utils import *
from database import *

app = FastAPI(debug=True)


@app.post("/version_info/")
# @require_signature
async def version_info(data: VersionData, _: None = Depends(require_signature)):
    return {"need_update": False if last_app_version == data.version else True, "version": last_app_version}


@app.post("/check_hwid/")
async def check_hwid(data: Hwid):
    result = await db_check_hwid(data.hwid)
    return result


@app.post("/add_hwid/")
async def add_hwid(data: Hwid):
    result = await db_add_user(data.hwid)
    return result


@app.post("/activate_key/")
async def activate_key(data: Key):
    key_data = await db_get_key(data.key)
    if key_data:
        result = await db_activate_key(key_data, data.hwid)
        return result
    else:
        return False
