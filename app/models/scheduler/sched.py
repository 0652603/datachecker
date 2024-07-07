from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
from app.utils.utils import time_fmt
import app.config.config as config


# 一個單例排程器 每隔 interval 秒數 固定執行一次 fn 函數 並更新最後執行時間 檢查時允許誤差在buffer內
class Once:
    def __init__(self, fn , interval:int, buffer: int):
        self.interval = interval # 初始化檢查間隔(秒為單位)
        self.scheduler = BackgroundScheduler()
        self.scheduler.add_job(fn,'interval',seconds= self.interval)
        self.time_with_buffer = buffer + interval
        self.initflag = False # 初始化旗標

    def start(self):
        if not self.initflag:
            self.scheduler.start()
            self.initflag = True
            return "啟動完成"
        return "無效操作:重複啟動"
    
    def shutdown(self):
        if self.initflag:
            self.scheduler.shutdown()
            self.initflag = False
            return "已關閉"
        return "無效操作:未初始化即關閉"


    def is_alive(self):
        if self.initflag:
            now = datetime.now()
            lasttime = config.sync_once_last_execute_time
            diff = now - lasttime
            if diff.seconds > self.time_with_buffer :
                return "[請注意排程器可能故障][上次執行時間:{tm}][相距:{df}秒]".format(tm= time_fmt(lasttime), df= diff.seconds)
            return "[正常運行中][上次執行時間:{tm}][相距:{df}秒]".format(tm= time_fmt(lasttime), df= diff.seconds)
        return "[無效操作:未初始化]"