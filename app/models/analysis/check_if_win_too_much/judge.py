from get_DB_data import get_one_user_DB_14_days_info,get_one_user_DB_history_info,build_sql_query
from datetime import datetime, timedelta
import pandas as pd

def first_judge_df_RTP_and_NW(df,score_threshold=5000,RTP_threshold=1.1):
    if df is not None and not df.empty:
        grouped_df = df.groupby(['uid', 'gameName'])[['validBet', 'score']].sum().reset_index()
        grouped_df['RTP'] = grouped_df['score']/grouped_df['validBet']
        mask      = ((grouped_df['score']>=score_threshold)&(grouped_df['RTP']>=RTP_threshold))
        result_df = grouped_df[mask]
        uid_list=result_df['uid'].tolist()
        gameName_list=result_df['gameName'].tolist()
        filtered_df = df[df['uid'].isin(uid_list) & df['gameName'].isin(gameName_list)]
        return filtered_df
    else:
        print('no data')

def get_game_type(df):
    if df is not None and not df.empty:
        game_id=df['gameId'].unique()
        chess_game_id_list=list(range(1,36))+list(range(40,44))+[105]+list(range(109,116))+[117,122]+list(range(125,128 ))+[129,132]
        fish_game_id_list=list(range(201,206))
        tiger_game_id_list=list(range(301,317))+[320,323,324]+list(range(801,805))+list(range(901,905))
        if game_id in chess_game_id_list  :
            df['game_type']='棋牌'
        elif game_id in fish_game_id_list :
            df['game_type']='魚機'
        elif game_id in tiger_game_id_list :
            df['game_type']='虎機'
        else:
            print('other company game')
        return df
    else:
        print('no data')

def is_bet_count_enough(df):
    if df is not None and not df.empty:
        game_type=df['game_type'].unique().tolist()[0]
        if game_type=='棋牌':
            if df.shape[0]>=100:
            #if df.shape[0]>=0:
                #print('fit bet count condition')
                return True
            else:
                #print('do not fit bet count condition')
                return False    
        elif game_type in ['魚機','虎機'] :
            #if df.shape[0]>=0:
            if df.shape[0]>=500:    
                #print('fit bet count condition')
                return True
            else:
                #print('do not fit bet count condition')
                return False
    else:
        print('no data')

def judge_win_days_rate(df):
    '''回傳(是否疑似異常)以及(贏錢天數比例)'''
    if df is not None and not df.empty: 
        df['add_time'] = pd.to_datetime(df['add_time'])
        df['date'] = df['add_time'].dt.date
        daily_profit = df.groupby('date')['score'].sum().reset_index()
        win_days = daily_profit[daily_profit['score'] > 0].shape[0]
        bet_days = daily_profit.shape[0]
        win_days_rate = win_days / bet_days
        if win_days_rate>=0.6:
            #print('fit win days rate condition')
            return True,win_days_rate
        else:
            #print('do not fit win days rate condition')
            return False,win_days_rate
    else:
        print('no data')
def judge_win_rate(df):
    if df is not None and not df.empty: 
        win_rate=(df['score']>0).sum()/df['score'].shape[0]
        game_type=df['game_type'].unique().tolist()[0]
        if game_type=='棋牌':
            if win_rate>=0.6:
                #print('fit win rate condition')
                return True,win_rate
            else:
                #print('do not fit win rate condition')
                return False,win_rate    
        elif game_type in ['魚機','虎機'] :
            if win_rate>=0.5:
                #print('fit win rate condition')
                return True,win_rate
            else:
                #print('do not fit win rate condition')
                return False,win_rate
    else:
        print('no data')

def judge_history_RTP(df):
    if df is not None and not df.empty:
        history_RTP=df['score'].sum()/df['validBet'].sum()
        #print(history_RTP)
        if history_RTP>=1.2:
            #print('fit history RTP condition')
            return True,history_RTP
        else:
            #print('do not fit history RTP condition')
            return False,history_RTP
    else:
        print('no data')

def get_df_return_abnormal_info(df):
    if df is not None and not df.empty:
        df.loc[:,'add_time'] = pd.to_datetime(df['add_time'])
        df_top3 = df.groupby(['uid', 'gameName'], group_keys=False).apply(lambda x: x.nlargest(3, 'score'))
        df_aggregated = df_top3.groupby(['uid', 'gameName'])['roundId'].agg(tuple).reset_index()
        unique_df = df.loc[df.groupby(['uid', 'gameName'])['add_time'].idxmax()]
        unique_df = df.drop_duplicates(subset=['uid', 'gameName'])
        unique_df=unique_df[['add_time','uid','agent','gameName','gameId','companyId']]
        unique_df = pd.merge(unique_df, df_aggregated[['uid','gameName','roundId']], on=['uid', 'gameName'], how='left')
        return unique_df
    else:
        print('no data')

# check_if_abnormal_player_over_five 異常玩家數量>=5
def check_if_abnormal_player_over_five(unique_df,trigger_time):
    result = {"is_alert":False, "trigger_time":trigger_time, "source":"","event":"","info":"","url":None}
    if unique_df.shape[0]>4:
        unique_df['sql_query'] = unique_df.apply(build_sql_query, axis=1)   
        result["is_alert"] = True
        result['source'] = "全平台"
        result['event']="最近5分鐘\nRTP高於110% 且\n贏分高於5,000CNY\n玩家數量超過5人"
        result['info'] += "---------------\n"
        result['info'] += "總共{count}人\n".format(count= unique_df.__len__())
        result['info'] += "---------------\n"
        for i in range(unique_df.__len__()):
            result['info'] += "[玩家{ct}]{uid}\n[遊戲]{gamename}\n[水池]{agent}\n---------------\n".format(ct= i+1,uid= unique_df.loc[i,"uid"],agent= unique_df.loc[i,"agent"],gamename= unique_df.loc[i,"gameName"])
    return result

'''
def check_step_2(unique_df,trigger_time):
    result = {"is_alert":False, "trigger_time":trigger_time, "source":"","event":"","info":"","url":None}
    if unique_df.shape[0]>0 :
            dict = unique_df.to_dict(orient='list')
            abnormal_user_dict={
                'uid':[],
                'gameName':[],
                'abnormal_info':[]
            }

            for index in range(len(dict['uid'])):
                host_id,uid,gameName='10.97.74.214',dict['uid'][index],dict['gameName'][index]
                print(f'uid : {uid}')
                
                one_user_DB_14_days_info=get_one_user_DB_14_days_info(host_id,uid,gameName,trigger_time)
                one_user_DB_14_days_info=get_game_type(one_user_DB_14_days_info)
                """
                test_df=pd.read_excel('D:\\Rudy\\Nex\\風控自動化\\data\\t_game_bet_log_0702_0704_test.xlsx')
                one_user_DB_14_days_info=test_df
                one_user_DB_14_days_info=get_game_type(one_user_DB_14_days_info)
                """
                # 如果押注數量夠多(有統計意義)才分析
                is_enough = is_bet_count_enough(one_user_DB_14_days_info)
                    
                # 如果太多天都贏:玩家有問題
                one_user_win_days_rate_info=judge_win_days_rate(one_user_DB_14_days_info)
                if is_enough and (one_user_win_days_rate_info[0]):
                    abnormal_user_dict['uid'].append(uid)
                    abnormal_user_dict['gameName'].append(gameName)
                    abnormal_user_dict['abnormal_info'].append(f'win days rate:{one_user_win_days_rate_info[1]}')
                
                # 如果太常贏:玩家有問題
                one_user_win_rate_info=judge_win_rate(one_user_DB_14_days_info)
                if is_enough and (one_user_win_rate_info[0]):
                    abnormal_user_dict['uid'].append(uid)
                    abnormal_user_dict['gameName'].append(gameName)
                    abnormal_user_dict['abnormal_info'].append(f'win rate:{one_user_win_rate_info[1]}')
                
                # 玩家在這個遊戲的歷史RTP是否太高
                one_user_history_RTP_info=judge_history_RTP(get_one_user_DB_history_info(host_id,uid,gameName))
                if is_enough and (one_user_history_RTP_info[0]):
                    abnormal_user_dict['uid'].append(uid)
                    abnormal_user_dict['gameName'].append(gameName)
                    abnormal_user_dict['abnormal_info'].append(f'history RTP:{one_user_history_RTP_info[1]}')
                        
            if abnormal_user_dict['uid']:
                filtered_df = unique_df[unique_df['uid'].isin(abnormal_user_dict['uid'])& unique_df['gameName'].isin(abnormal_user_dict['gameName'])]
                df_abnormal_info=pd.DataFrame(abnormal_user_dict)
                filtered_df = pd.merge(filtered_df, df_abnormal_info, on=['uid', 'gameName'], how='left')
                #print(abnormal_user_dict)
                #print(filtered_df)
                filtered_df['sql_query'] = filtered_df.apply(build_sql_query, axis=1) 
                
                result["is_alert"] = True
                result["event"]="players between 0 and 5"
                result["info"]=filtered_df
    return result
'''

def check_win_days_rate(unique_df,trigger_time, data):
    result = {"is_alert":False, "trigger_time":trigger_time, "source":"","event":"","info":"","url":None}
    if unique_df.shape[0]>0 :
        for index in range(len(unique_df)):
            
            # 如果押注數量夠多(有統計意義)才分析
            is_enough = is_bet_count_enough(data["two_week_data"][index])
                
            # 如果太多天都贏:玩家有問題
            one_user_win_days_rate_info=judge_win_days_rate(data["two_week_data"][index])
            if is_enough and (one_user_win_days_rate_info[0]):
                result['info'] += "[玩家]{uid}\n [遊戲]{game}\n [天數比例]{abinfo:.0%}\n------------\n".format(uid= data["uid"][index], game= data["game"][index], abinfo= one_user_win_days_rate_info[1])
            
        if len(result["info"])>0 :
            result["is_alert"] = True
            result["source"] = "全平台"
            result["event"] = "玩家贏錢天數比例太高"
    return result

def check_win_rate(unique_df,trigger_time, data):
    result = {"is_alert":False, "trigger_time":trigger_time, "source":"","event":"","info":"","url":None}
    if unique_df.shape[0]>0 :
        for index in range(len(unique_df)):
            # 如果押注數量夠多(有統計意義)才分析
            is_enough = is_bet_count_enough(data["two_week_data"][index])
                
            # 如果太常贏:玩家有問題
            one_user_win_rate_info=judge_win_rate(data["two_week_data"][index])
            if is_enough and (one_user_win_rate_info[0]):
                result['info'] += "[玩家]{uid}\n [遊戲]{game}\n [比例]{abinfo:.0%}\n------------\n".format(uid= data["uid"][index], game= data["game"][index], abinfo= one_user_win_rate_info[1])
            
        if len(result["info"])>0 :
            result["is_alert"] = True
            result["source"] = "全平台"
            result["event"] = "玩家贏錢比例太高"
    return result


def check_history_rtp(unique_df,trigger_time, data, host_id):
    result = {"is_alert":False, "trigger_time":trigger_time, "source":"","event":"","info":"","url":None}
    if unique_df.shape[0]>0 :
        for index in range(len(unique_df)):
            # 如果押注數量夠多(有統計意義)才分析
            is_enough = is_bet_count_enough(data["two_week_data"][index])
                
            # 如果歷史RTP太高:玩家有問題
            one_user_history_RTP_info= judge_history_RTP(get_one_user_DB_history_info(host_id,data["uid"][index],data["game"][index]))
            if is_enough and (one_user_history_RTP_info[0]):
                result['info'] += "[玩家]{uid}\n [遊戲]{game}\n [比例]{abinfo:.0%}\n------------\n".format(uid= data["uid"][index], game= data["game"][index], abinfo= one_user_history_RTP_info[1])
            
        if len(result["info"])>0 :
            result["is_alert"] = True
            result["source"] = "全平台"
            result["event"] = "玩家歷史RTP過高"
    return result


def judge_abnormal_player(df,now):
    result = {"is_alert":False, "trigger_time":now, "source":"","event":"","info":"","url":None}
    if df is not None and not df.empty:
        unique_df=get_df_return_abnormal_info(df)

        # Step 1 : 判斷是否太多玩家都異常
        result = check_if_abnormal_player_over_five(unique_df, now)
        if result["is_alert"] :
            return result
        
        # Step 1.1 : 玩家數量有限，可以仔細判斷各玩家狀況:
        data = {"uid":[],"game":[],"two_week_data":[]}
        host_id='10.97.74.214'
        for index in range(unique_df.__len__()):
            uid,gameName = unique_df.loc[index,'uid'],unique_df.loc[index,'gameName']
            data["uid"].append(uid)
            data["game"].append(gameName)
            data["two_week_data"].append(get_game_type(get_one_user_DB_14_days_info(host_id,uid,gameName,now)))


        # Step 2 : 如果太多天都贏:玩家有問題
        result = check_win_days_rate(unique_df, now, data)
        if result["is_alert"] :
            return result
        
        # Step 3 : 如果太常贏:玩家有問題
        result = check_win_rate(unique_df, now, data)
        if result["is_alert"] :
            return result
        
        # Step 4 : 如果歷史RTP太高:玩家有問題
        result = check_history_rtp(unique_df, now, data, host_id)
        if result["is_alert"] :
            return result
        
    return result

if __name__ == "__main__":
    df=pd.read_excel('D:\\Rudy\\Nex\\風控自動化\\data\\t_game_bet_log_0702_0704_test.xlsx')
    #print(first_judge_df_RTP_and_NW(df,score_threshold=5000,RTP_threshold=1.1))
    print(judge_history_RTP(df))