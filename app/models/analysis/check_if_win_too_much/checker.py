import pandas as pd
import pymysql
import pymysql.cursors
from datetime import datetime, timedelta
import sys
sys.path.append('app\\models\\analysis\\check_if_win_too_much\\')
from transform_currency import get_transform_all_to_CNY_df
from get_DB_data import get_DB_5_min_info
from judge import first_judge_df_RTP_and_NW,judge_abnormal_player

def check_if_win_too_much(checktime:datetime): 
    now = checktime
    data_5_min_CNY = get_transform_all_to_CNY_df(get_DB_5_min_info(host_id='10.97.74.214',now=now))
    # Step 1
    first_judge_df = first_judge_df_RTP_and_NW(data_5_min_CNY,score_threshold=5000,RTP_threshold=1.1) # RTP
    #first_judge_df = first_judge_df_RTP_and_NW(data_5_min_CNY,score_threshold=40,RTP_threshold=1.1) # test
    '''
    #test
    df=pd.read_excel('D:\\Rudy\\Nex\\風控自動化\\data\\t_game_bet_log_0702_0704_test.xlsx')
    first_judge_df = first_judge_df_RTP_and_NW(df,score_threshold=5,RTP_threshold=1.01)
    '''
    # Step 2
    return judge_abnormal_player(first_judge_df,now=now)

#if __name__ == "__main__":
#    check_if_win_too_much(checktime:datetime)
