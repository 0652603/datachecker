from fastapi import FastAPI
from app.api import scheduler
import logging
from app.models.analysis.ana import analysis
from app.models.scheduler.sched import Once


# 配置基本Log INFO
logging.basicConfig(level=logging.INFO)

# 一個服務 app :FastApi
app = FastAPI()

'''以下添加路由'''
app.include_router(scheduler.router, tags = ["排程器"])