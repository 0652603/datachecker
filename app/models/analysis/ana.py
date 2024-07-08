from app.models.bot.lark.msg import alert
from datetime import datetime
import app.config.glob as glob
import pytz

def analysis():
    ana_time = datetime.now(pytz.timezone('Asia/Taipei'))
    result = ana_by_case(ana_time)
    if result[0]:
        alert(result[1],result[2],result[3],result[4],result[5])    
    glob.sync_once_last_execute_time = ana_time


def ana_by_case(ana_time:datetime):
    is_alert = False
    trigger_time = ana_time
    source = ""
    event = ""
    info = ""
    url = None

    # ToDo 所有檢查
    is_alert = True
    return is_alert,trigger_time,source,event,info,url