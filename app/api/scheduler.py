from fastapi import APIRouter
from app.models.lark_bot.msg import alert
from datetime import datetime
from app.models.scheduler.sched import Once
from app.utils.utils import time_fmt


router = APIRouter()

check_interval = 15 # 幾秒檢查一次
check_buffer = 300 # 幾秒鐘緩衝


def start_ana():
    alert("全站最近[X]筆RTP超過 105%","起始注單:d4419c87\n結束注單:4c623bcf")
    sync_once_last_execute_time = datetime.now()


# 創建Once實例
once = Once(start_ana,check_interval,check_buffer)

@router.get("/start",summary="啟動排程器",description="詳細敘述")
async def start():
    return {"message": once.start()}

@router.get("/shutdown",summary="關閉排程器",description="詳細敘述")
async def shutdown():
    return {"message": once.shutdown()}

@router.get("/isalive",summary="檢查排程器是否正常",description="詳細敘述")
async def is_alive():
    return once.is_alive()