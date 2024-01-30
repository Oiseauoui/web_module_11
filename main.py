# main.py
import re
from ipaddress import ip_address
from typing import Callable
from pathlib import Path

import redis.asyncio as redis
from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_limiter import FastAPILimiter
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.db import get_db
from src.routes import todos, auth, users
from src.conf.config import config

app = FastAPI()
banned_ips = [
    ip_address("192.168.1.1"),
    ip_address("192.168.1.2"),
    ip_address("127.0.0.1"),
]
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware('http')
async def custom_middleware(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    during = time.time() - start_time
    response.headers['performance'] = str(during)
    return response


templates = Jinja2Templates(directory='templates')
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse, description="Main page")
async def root(request: Request):
    return templates.TemplateResponse('index.html', {"request": request, "title": "Contacts Арр"})


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
    #Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


app.include_router(auth.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')
app.include_router(contacts.router, prefix='/api')

