from fastapi import FastAPI
from app.api import scheduler

# 起一個服務 app
app = FastAPI()


'''以下添加路由'''
app.include_router(scheduler.router, tags = ["排程器"])