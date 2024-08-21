import pandas as pd
import pymysql
import pymysql.cursors
from datetime import datetime, timedelta
import sys
sys.path.append('app\\models\\analysis\\check_if_win_too_much\\')
from app.models.analysis.check_if_win_too_much.transform_currency import get_transform_all_to_CNY_df
from app.models.analysis.check_if_win_too_much.get_DB_data import get_DB_5_min_info,get_company_id_tuple
from app.models.analysis.check_if_win_too_much.judge import first_judge_df_RTP_and_NW,judge_abnormal_player

def check_if_win_too_much(checktime:datetime): 
    now = checktime
    print(now)
    company_id_tuple=get_company_id_tuple()
    data_origin=get_DB_5_min_info(host_id='10.97.74.214',now=now,company_id_tuple=company_id_tuple)
    data_5_min_CNY = get_transform_all_to_CNY_df(data_origin,company_id_tuple)
    # Step 1
    first_judge_df = first_judge_df_RTP_and_NW(data_5_min_CNY,score_threshold=5000,RTP_threshold=1.1) # RTP
    
    #result=judge_abnormal_player(first_judge_df,now=now,company_id_tuple=company_id_tuple)
    #print(result)
    #return result
    #return {"is_alert":False, "trigger_time":now, "source":"","event":"","info":"","url":None} #for test
    # Step 2
    return judge_abnormal_player(first_judge_df,now=now,company_id_tuple=company_id_tuple)




#if __name__ == "__main__":
#    check_if_win_too_much(checktime:datetime)
