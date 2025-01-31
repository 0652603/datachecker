from app.models.bot.lark.msg import alert
from datetime import datetime
import app.config.glob as glob
import pytz
from app.models.analysis.check_if_win_too_much.checker import check_if_win_too_much
from app.models.bot.TG.TG_msg import Send_message 
def analysis():
    ana_time = datetime.now(pytz.timezone('Asia/Taipei'))
    result = ana_by_case(ana_time)
    if result["is_alert"]:
        print(result)
        #alert(result["trigger_time"],result["source"],result["event"],result["info"],result["url"])
        send_message= Send_message()
        send_message.send_message_TG(result)
    glob.sync_once_last_execute_time = ana_time


def ana_by_case(ana_time:datetime):
    # ToDo 所有檢查
    result = dict({"is_alert":False,"trigger_time":"","source":"","event":"","info":"","url":""})

    # Step1 : 玩家異常贏分
    result=check_if_win_too_much(ana_time)
    

    return result
