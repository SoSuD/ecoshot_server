import json

from fastapi import FastAPI, HTTPException, Request
from models import *
from functools import wraps

async def require_signature(request: Request):
    #@wraps(func)
    #   async def wrapper(request: Request, *args, **kwargs):
    if "google-signature-x" not in request.headers:
        raise HTTPException(status_code=400, detail="нужна сигнатура")
    else:
        reqj = await request.json()

        if reqj != json.loads(request.headers["google-signature-x"]):
            print(request.json())
            print(json.loads(request.headers["google-signature-x"]))
            raise HTTPException(status_code=400, detail="сигнатура не подошла")

        #return await func(request, *args, **kwargs)

    #return wrapper