from get_DB_data import get_company_name_info, get_one_user_DB_14_days_info,get_one_user_DB_history_info,build_sql_query
from datetime import datetime, timedelta
import pandas as pd
from check_folder_and_save_file import save_and_delete_folder_file
from transform_currency import get_transform_all_to_CNY_df

def first_judge_df_RTP_and_NW(df,score_threshold=5000,RTP_threshold=1.1):
    #print('RTP_threshold:',RTP_threshold)
    if df is not None and not df.empty:
        grouped_df = df.groupby(['uid', 'gameName'])[['validBet', 'score']].sum().reset_index()
        grouped_df['RTP'] = (grouped_df['score']+grouped_df['validBet'])/grouped_df['validBet']
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
            if df.shape[0]>=50:
            #if df.shape[0]>=30:
            #if df.shape[0]>=0:
                #print('fit bet count condition')
                return True
            else:
                #print('do not fit bet count condition')
                return False    
        elif game_type=='魚機' :
            #if df.shape[0]>=0:
            if df.shape[0]>=300:
            #if df.shape[0]>=30:        
                #print('fit bet count condition')
                return True
            else:
                #print('do not fit bet count condition')
                return False
        elif game_type=='虎機' :
            #if df.shape[0]>=0:
            if df.shape[0]>=500: 
            #if df.shape[0]>=15:    
                #print('fit bet count condition')
                return True
            else:
                #print('do not fit bet count condition')
                return False
    else:
        print('no data')
def is_bet_days_enough(bet_days):
    result=False
    if bet_days>=7:
        result=True
    return result

def judge_win_score_and_RTP(df):
    '''回傳(是否疑似異常)以及(贏錢過多)以及(RTP過高)'''
    if df is not None and not df.empty:
        _14_days_win_score=df['score'].sum() 
        _14_days_validBet=df['validBet'].sum()
        _14_days_RTP=(_14_days_win_score+_14_days_validBet)/_14_days_validBet
        #if _14_days_win_score>1 and _14_days_RTP>1.01:#test
        if _14_days_win_score>=15000 and _14_days_RTP>=1.2:
            return True,_14_days_win_score,_14_days_RTP
        else:
            return False,_14_days_win_score,_14_days_RTP
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
            return True,win_days_rate,win_days,bet_days
        else:
            #print('do not fit win days rate condition')
            return False,win_days_rate,win_days,bet_days
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
        history_RTP=(df['score'].sum()+df['validBet'].sum())/df['validBet'].sum()
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
        df_aggregated = df_top3.groupby(['uid', 'gameName','companyId'])['roundId'].agg(tuple).reset_index()
        unique_df = df.loc[df.groupby(['uid', 'gameName'])['add_time'].idxmax()]
        unique_df = df.drop_duplicates(subset=['uid', 'gameName'])
        unique_df=unique_df[['add_time','uid','agent','gameName','gameId']]
        unique_df = pd.merge(unique_df, df_aggregated[['uid','gameName','companyId','roundId']], on=['uid', 'gameName'], how='left')
        return unique_df
    else:
        print('no data')

# check_if_abnormal_player_over_five 異常玩家數量>=5
def check_if_abnormal_player_over_five(unique_df,trigger_time):
    result = {"is_alert":False, "trigger_time":trigger_time, "source":"","event":"","info":"","url":None}
    if unique_df.shape[0]>5:
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
def check_win_days_rate(unique_df,trigger_time, data,_30min_bet_win_score_RTP):
    result = {"is_alert":False, "trigger_time":trigger_time, "source":"","event":"","info":"","url":None}
    if unique_df.shape[0]>0 :
        for index in range(len(unique_df)):
            # 如果太多天都贏:玩家有問題
            one_user_win_days_rate_info=judge_win_days_rate(data["two_week_data"][index])
            
            # 如果押注數量及天數夠多(有統計意義)才分析
            is_enough = is_bet_count_enough(data["two_week_data"][index]) & is_bet_days_enough(one_user_win_days_rate_info[3]) 
            #is_enough = is_bet_count_enough(data["two_week_data"][index])#test
           
            if is_enough and (one_user_win_days_rate_info[0]):
                mask=_30min_bet_win_score_RTP['uid']==data["uid"][index]
                _30min_uid_data=_30min_bet_win_score_RTP[mask]
                _30min_uid_validBet=_30min_uid_data.iloc[0]['validBet']
                _30min_uid_score=_30min_uid_data.iloc[0]['score']
                _30min_uid_RTP=_30min_uid_data.iloc[0]['RTP']              
                if len(result["source"])>0:
                    result["source"] += ','+data["company_name"][index]
                else:
                    result["source"] += data["company_name"][index]
                result['info'] += "[玩家]{uid}\n[遊戲]{game}\n[天數比例]{abinfo_ratio:.0%}\n[贏錢天數]{abinfo_win_days}\n[下注天數]{abinfo_bet_days}\n [近30分鐘投注額]CNY:{_30min_uid_validBet}\n [近30分鐘淨贏分]CNY:{_30min_uid_score}\n [近30分鐘RTP]{_30min_uid_RTP:.0%}\n------------\n".format(uid= data["uid"][index], game= data["game"][index], abinfo_ratio= one_user_win_days_rate_info[1],abinfo_win_days=one_user_win_days_rate_info[2],abinfo_bet_days=one_user_win_days_rate_info[3],_30min_uid_validBet=_30min_uid_validBet,_30min_uid_score=_30min_uid_score,_30min_uid_RTP=_30min_uid_RTP)
            
        if len(result["info"])>0 :
            result["is_alert"] = True
            result["event"] = "玩家贏錢天數比例太高"
    return result
'''
def check_14_days_score_and_RTP(unique_df,trigger_time, data,_30min_bet_win_score_RTP):
    result = {"is_alert":False, "trigger_time":trigger_time, "source":"","event":"","info":"","url":None}
    if unique_df.shape[0]>0 :
        for index in range(len(unique_df)):
            # 如果近14天贏太多及RTP太高:玩家有問題
            one_user_win_score_and_RTP_info=judge_win_score_and_RTP(data["two_week_data"][index])
            # 如果押注數量夠多(有統計意義)才分析
            is_enough = is_bet_count_enough(data["two_week_data"][index]) 
           
            if is_enough and (one_user_win_score_and_RTP_info[0]):
                mask=_30min_bet_win_score_RTP['uid']==data["uid"][index]
                _30min_uid_data=_30min_bet_win_score_RTP[mask]
                _30min_uid_validBet=_30min_uid_data.iloc[0]['validBet']
                _30min_uid_score=_30min_uid_data.iloc[0]['score']
                _30min_uid_RTP=_30min_uid_data.iloc[0]['RTP']
                if len(result["source"])>0:
                    result["source"] += ','+data["company_name"][index]
                else:
                    result["source"] += data["company_name"][index]
                result['info'] += "[玩家]{uid}\n[遊戲]{game}\n[淨贏分]CNY:{abinfo_win_score}\n[RTP]{abinfo_RTP:.0%}\n [近30分鐘投注額]CNY:{_30min_uid_validBet}\n [近30分鐘淨贏分]CNY:{_30min_uid_score}\n [近30分鐘RTP]{_30min_uid_RTP:.0%}\n------------\n".format(uid= data["uid"][index], game= data["game"][index], abinfo_win_score= one_user_win_score_and_RTP_info[1],abinfo_RTP=one_user_win_score_and_RTP_info[2],_30min_uid_validBet=_30min_uid_validBet,_30min_uid_score=_30min_uid_score,_30min_uid_RTP=_30min_uid_RTP)
            
        if len(result["info"])>0 :
            result["is_alert"] = True
            result["event"] = "玩家近14天贏太多及RTP太高"
    return result

def check_win_rate(unique_df,trigger_time, data,_30min_bet_win_score_RTP):
    result = {"is_alert":False, "trigger_time":trigger_time, "source":"","event":"","info":"","url":None}
    if unique_df.shape[0]>0 :
        for index in range(len(unique_df)):
            # 如果押注數量夠多(有統計意義)才分析
            is_enough = is_bet_count_enough(data["two_week_data"][index])
                
            # 如果太常贏:玩家有問題
            one_user_win_rate_info=judge_win_rate(data["two_week_data"][index])
            if is_enough and (one_user_win_rate_info[0]):
                mask=_30min_bet_win_score_RTP['uid']==data["uid"][index]
                _30min_uid_data=_30min_bet_win_score_RTP[mask]
                _30min_uid_validBet=_30min_uid_data.iloc[0]['validBet']
                _30min_uid_score=_30min_uid_data.iloc[0]['score']
                _30min_uid_RTP=_30min_uid_data.iloc[0]['RTP']
                if len(result["source"])>0:
                    result["source"] += ','+data["company_name"][index]
                else:
                    result["source"] += data["company_name"][index] 
                result['info'] += "[玩家]{uid}\n [遊戲]{game}\n [勝率]{abinfo:.0%}\n [近30分鐘投注額]CNY:{_30min_uid_validBet}\n [近30分鐘淨贏分]CNY:{_30min_uid_score}\n [近30分鐘RTP]{_30min_uid_RTP:.0%}\n------------\n".format(uid= data["uid"][index], game= data["game"][index], abinfo= one_user_win_rate_info[1],_30min_uid_validBet=_30min_uid_validBet,_30min_uid_score=_30min_uid_score,_30min_uid_RTP=_30min_uid_RTP)
            
        if len(result["info"])>0 :
            result["is_alert"] = True
            result["event"] = "玩家贏錢比例太高"
    return result


def check_history_rtp(unique_df,trigger_time, data, host_id,_30min_bet_win_score_RTP,company_id_tuple):
    result = {"is_alert":False, "trigger_time":trigger_time, "source":"","event":"","info":"","url":None}
    if unique_df.shape[0]>0 :
        for index in range(len(unique_df)):
            # 如果押注數量夠多(有統計意義)才分析
            is_enough = is_bet_count_enough(data["two_week_data"][index])
                
            # 如果歷史RTP太高:玩家有問題
            one_user_DB_history_info=get_one_user_DB_history_info(host_id,data["uid"][index],data["game"][index],company_id_tuple)
            one_user_DB_history_info=get_transform_all_to_CNY_df(one_user_DB_history_info,company_id_tuple)
            one_user_history_RTP_info= judge_history_RTP(one_user_DB_history_info)
            if is_enough and (one_user_history_RTP_info[0]):
                mask=_30min_bet_win_score_RTP['uid']==data["uid"][index]
                _30min_uid_data=_30min_bet_win_score_RTP[mask]
                _30min_uid_validBet=_30min_uid_data.iloc[0]['validBet']
                _30min_uid_score=_30min_uid_data.iloc[0]['score']
                _30min_uid_RTP=_30min_uid_data.iloc[0]['RTP'] 
                if len(result["source"])>0:
                    result["source"] += ','+data["company_name"][index]
                else:
                    result["source"] += data["company_name"][index]
                result['info'] += "[玩家]{uid}\n [遊戲]{game}\n [RTP]{abinfo:.0%}\n [近30分鐘投注額]CNY:{_30min_uid_validBet}\n [近30分鐘淨贏分]CNY:{_30min_uid_score}\n [近30分鐘RTP]{_30min_uid_RTP:.0%}\n------------\n".format(uid= data["uid"][index], game= data["game"][index], abinfo= one_user_history_RTP_info[1],_30min_uid_validBet=_30min_uid_validBet,_30min_uid_score=_30min_uid_score,_30min_uid_RTP=_30min_uid_RTP)
            
        if len(result["info"])>0 :
            result["is_alert"] = True
            result["event"] = "玩家歷史RTP過高"
    return result

def check_30min_ip_number(unique_df, trigger_time,data,_30min_bet_win_score_RTP):
    result = {"is_alert":False, "trigger_time":trigger_time, "source":"","event":"","info":"","url":None}
    if unique_df.shape[0]>0 :
        for index in range(len(unique_df)):
            mask=_30min_bet_win_score_RTP['uid']==data["uid"][index]
            ip_numbers= _30min_bet_win_score_RTP[mask]['ip_change_count'].tolist()[0]
            
            if ip_numbers>5:
                mask=_30min_bet_win_score_RTP['uid']==data["uid"][index]
                _30min_uid_data=_30min_bet_win_score_RTP[mask]
                _30min_uid_validBet=_30min_uid_data.iloc[0]['validBet']
                _30min_uid_score=_30min_uid_data.iloc[0]['score']
                _30min_uid_RTP=_30min_uid_data.iloc[0]['RTP'] 
                if len(result["source"])>0:
                    result["source"] += ','+data["company_name"][index]
                else:
                    result["source"] += data["company_name"][index]

                result['info'] += "[玩家]{uid}\n [遊戲]{game}\n [近30分鐘切換IP數量]{abinfo}\n [近30分鐘投注額]CNY:{_30min_uid_validBet}\n [近30分鐘淨贏分]CNY:{_30min_uid_score}\n [近30分鐘RTP]{_30min_uid_RTP:.0%}\n------------\n".format(uid= data["uid"][index], game= data["game"][index], abinfo=ip_numbers,_30min_uid_validBet=_30min_uid_validBet,_30min_uid_score=_30min_uid_score,_30min_uid_RTP=_30min_uid_RTP)
            
        if len(result["info"])>0 :
            result["is_alert"] = True
            result["event"] = "IP頻繁切換"
    return result

# 计算 ip 变化次数的函数
def count_ip_changes(group):
    # 进行时间排序，只在函数内影响分组数据
    group_sorted = group.sort_values(by='add_time')
    # 计算 ip 变化次数
    ip_changes = group_sorted['ip'].ne(group_sorted['ip'].shift()).sum() - 1
    return ip_changes



def get_30min_bet_win_score_RTP(df):
    # 计算每个 uid 和 gameName 下不同的 ip 数量
    #ip_counts = df.groupby(['uid', 'gameName'])['ip'].nunique().reset_index()
    # 计算每个 (uid, gameName) 组的 ip 变化次数
    ip_change_count = df.groupby(['uid', 'gameName']).apply(count_ip_changes).reset_index(name='ip_change_count')
    ip_change_count.rename(columns={'ip': 'ip_change_count'}, inplace=True)
    _30min_bet_win_score_RTP = df.groupby(['uid', 'gameName'])[['validBet', 'score']].sum().reset_index()
    # 合并计算结果
    _30min_bet_win_score_RTP = pd.merge(_30min_bet_win_score_RTP, ip_change_count, on=['uid', 'gameName'])
    _30min_bet_win_score_RTP['score']=round(_30min_bet_win_score_RTP['score'].astype(float),2)
    _30min_bet_win_score_RTP['validBet']=round(_30min_bet_win_score_RTP['validBet'].astype(float),2)
    _30min_bet_win_score_RTP['RTP']=1+round(_30min_bet_win_score_RTP['score']/_30min_bet_win_score_RTP['validBet'],2)
    return _30min_bet_win_score_RTP



def judge_abnormal_player(df,now,company_id_tuple):
    result = {"is_alert":False, "trigger_time":now, "source":"","event":"","info":"","url":None}
    if df is not None and not df.empty:
        #test
        #print(df)
        
        unique_df=get_df_return_abnormal_info(df)
        #計算近30分鐘鐘統計結果
        _30min_bet_win_score_RTP=get_30min_bet_win_score_RTP(df)
        # Step 1 : 判斷是否太多玩家都異常
        
        result = check_if_abnormal_player_over_five(unique_df, now)
        if result["is_alert"] :
            save_and_delete_folder_file(df)
            return result
        
        # Step 1.1 : 玩家數量有限，可以仔細判斷各玩家狀況:
        data = {"uid":[],"game":[],"two_week_data":[],"company_name":[]}
        host_id='10.97.74.214'
        for index in range(unique_df.__len__()):
            uid,gameName,companyId = unique_df.loc[index,'uid'],unique_df.loc[index,'gameName'],unique_df.loc[index,'companyId']
            data["uid"].append(uid)
            data["game"].append(gameName)
            data["company_name"].append(get_company_name_info(host_id,"usercenter",companyId)['company_name'].tolist()[0])
            one_user_DB_14_days_info=get_one_user_DB_14_days_info(host_id,uid,gameName,now,company_id_tuple)
            one_user_DB_14_days_info=get_transform_all_to_CNY_df(one_user_DB_14_days_info,company_id_tuple)
            data["two_week_data"].append(get_game_type(one_user_DB_14_days_info))

        #save_and_delete_folder_file(df)
        # Step 1.2 : IP更換頻繁:玩家有問題
        result = check_30min_ip_number(unique_df, now,data,_30min_bet_win_score_RTP)
        if result["is_alert"] :
            save_and_delete_folder_file(df)
            return result


        
        # Step 2 : 如果近14天贏太多且RTP太高:玩家有問題
        
        result = check_14_days_score_and_RTP(unique_df, now, data,_30min_bet_win_score_RTP)
        if result["is_alert"] :
            save_and_delete_folder_file(df)
            return result
        
        # Step 3 : 如果太多天都贏:玩家有問題
        '''
        result = check_win_days_rate(unique_df, now, data,_30min_bet_win_score_RTP)
        if result["is_alert"] :
            save_and_delete_folder_file(df)
            return result
        '''
        # Step 4 : 如果太常贏:玩家有問題
        result = check_win_rate(unique_df, now, data,_30min_bet_win_score_RTP)
        if result["is_alert"] :
            save_and_delete_folder_file(df)
            return result
        
        # Step 5 : 如果歷史RTP太高:玩家有問題
        result = check_history_rtp(unique_df, now, data, host_id,_30min_bet_win_score_RTP,company_id_tuple)
        if result["is_alert"] :
            save_and_delete_folder_file(df)
            return result
        
        
    return result

if __name__ == "__main__":
    df=pd.read_excel('D:\\Rudy\\Nex\\風控自動化\\data\\t_game_bet_log_0702_0704_test.xlsx')
    #print(first_judge_df_RTP_and_NW(df,score_threshold=5000,RTP_threshold=1.1))
    print(judge_history_RTP(df))