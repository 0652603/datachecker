from datetime import datetime, timedelta
import pytz


def time_fmt(time:datetime):
    '''給出datetime格式 回傳UTC+8台北時間'''
    intime = time.astimezone(pytz.timezone('Asia/Taipei'))
    utc_offset = intime.utcoffset().total_seconds() / 3600
    utc_offset_str = f"UTC{'+' if utc_offset >= 0 else ''}{int(utc_offset)}"
    return intime.strftime(f"%Y-%m-%d %H:%M:%S {utc_offset_str}")