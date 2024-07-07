from app.models.lark_bot.msg import alert
from datetime import datetime
import app.config.config


def start_ana():
    app.config.config.sync_once_last_execute_time = datetime.now()
    # alert("全站最近[X]筆RTP超過 105%","起始注單:d4419c87\n結束注單:4c623bcf")
