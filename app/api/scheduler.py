from fastapi import APIRouter
from app.models.lark_bot.msg import alert
from datetime import datetime
from app.models.scheduler.sched import Once
from app.utils.utils import time_fmt
from app.models.analysis.ana import start_ana
from app.config.config import check_interval, check_buffer


# 創建Once實例
once = Once(start_ana,check_interval,check_buffer)

router = APIRouter()

@router.get("/start",summary="啟動排程器",description="詳細敘述")
async def start():
    return {"message": once.start()}

@router.get("/shutdown",summary="關閉排程器",description="詳細敘述")
async def shutdown():
    return {"message": once.shutdown()}

@router.get("/isalive",summary="檢查排程器是否正常",description="詳細敘述")
async def is_alive():
    return once.is_alive()