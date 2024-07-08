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

def judge_bet_count(df):
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
        df['add_time'] = pd.to_datetime(df['add_time'])
        df_top3 = df.groupby(['uid', 'gameName'], group_keys=False).apply(lambda x: x.nlargest(3, 'score'))
        df_aggregated = df_top3.groupby(['uid', 'gameName'])['roundId'].agg(tuple).reset_index()
        unique_df = df.loc[df.groupby(['uid', 'gameName'])['add_time'].idxmax()]
        unique_df = df.drop_duplicates(subset=['uid', 'gameName'])
        unique_df=unique_df[['add_time','uid','agent','gameName','gameId','companyId']]
        unique_df = pd.merge(unique_df, df_aggregated[['uid','gameName','roundId']], on=['uid', 'gameName'], how='left')
        return unique_df
    else:
        print('no data')


def judge_abnormal_player(df,now):
    is_alert = False
    trigger_time = now
    source = ""
    event = ""
    info = ""
    url = None

    if df is not None and not df.empty:
        unique_df=get_df_return_abnormal_info(df)
        dict = unique_df.to_dict(orient='list')

        if unique_df.shape[0]>5:
            #print('all abnormal players data')

            unique_df['sql_query'] = unique_df.apply(build_sql_query, axis=1)   
            #print(unique_df)
            #json_result = unique_df.to_json(orient="records", force_ascii=False, date_format="iso")
            #print(json_result)
            is_alert = True
            source = "全平台"
            event="最近5分鐘\nRTP高於110% 且\n贏分高於5,000CNY\n玩家數量超過5人"
            info += "---------------\n"
            info += "總共{count}人\n".format(count= unique_df.__len__())
            info += "---------------\n"
            for i in range(unique_df.__len__()):
                info += "[玩家{ct}]{uid}\n[遊戲]{gamename}\n[水池]{agent}\n---------------\n".format(ct= i+1,uid= unique_df.loc[i,"uid"],agent= unique_df.loc[i,"agent"],gamename= unique_df.loc[i,"gameName"])
            return is_alert,trigger_time,source,event,info,url 
        elif unique_df.shape[0]>0 and unique_df.shape[0]<5 :
            #print('14 days data of some players')
            abnormal_user_dict={
                'uid':[],
                'gameName':[],
                'abnormal_info':[]
            }
            for index in range(len(dict['uid'])):
                host_id,uid,gameName='10.97.74.214',dict['uid'][index],dict['gameName'][index]
                print(f'uid : {uid}')
                
                one_user_DB_14_days_info=get_one_user_DB_14_days_info(host_id,uid,gameName,now)
                one_user_DB_14_days_info=get_game_type(one_user_DB_14_days_info)
                '''
                test_df=pd.read_excel('D:\\Rudy\\Nex\\風控自動化\\data\\t_game_bet_log_0702_0704_test.xlsx')
                one_user_DB_14_days_info=test_df
                one_user_DB_14_days_info=get_game_type(one_user_DB_14_days_info)
                '''
                if judge_bet_count(one_user_DB_14_days_info):
                    one_user_win_days_rate_info=judge_win_days_rate(one_user_DB_14_days_info)
                    if not (one_user_win_days_rate_info[0]):
                        one_user_win_rate_info=judge_win_rate(one_user_DB_14_days_info)
                        if not (one_user_win_rate_info[0]):
                            #one_user_history_RTP_info=judge_history_RTP(test_df)
                            one_user_history_RTP_info=judge_history_RTP(get_one_user_DB_history_info(host_id,uid,gameName))
                            if not (one_user_history_RTP_info[0]):
                                print('normal player : win days rate,win rate,history RTP is OK!!!')
                            else:
                                abnormal_user_dict['uid'].append(uid)
                                abnormal_user_dict['gameName'].append(gameName)
                                abnormal_user_dict['abnormal_info'].append(f'history RTP:{one_user_history_RTP_info[1]}')
                        else:
                            abnormal_user_dict['uid'].append(uid)
                            abnormal_user_dict['gameName'].append(gameName)
                            abnormal_user_dict['abnormal_info'].append(f'win rate:{one_user_win_rate_info[1]}')
                    else:
                        abnormal_user_dict['uid'].append(uid)
                        abnormal_user_dict['gameName'].append(gameName)
                        abnormal_user_dict['abnormal_info'].append(f'win days rate:{one_user_win_days_rate_info[1]}')
                else:
                    print('normal player : bet count is OK!!!')
            if abnormal_user_dict['uid']:
                filtered_df = unique_df[unique_df['uid'].isin(abnormal_user_dict['uid'])& unique_df['gameName'].isin(abnormal_user_dict['gameName'])]
                df_abnormal_info=pd.DataFrame(abnormal_user_dict)
                filtered_df = pd.merge(filtered_df, df_abnormal_info, on=['uid', 'gameName'], how='left')
                #print(abnormal_user_dict)
                #print(filtered_df)
                filtered_df['sql_query'] = filtered_df.apply(build_sql_query, axis=1) 
                
                is_alert = True
                event="players between 0 and 5"
                info=filtered_df
                #json_result = filtered_df.to_json(orient="records", force_ascii=False, date_format="iso")
                #print(json_result)
        else:
            print('no abnormal user data')
    else:
        print('no abnormal user data')
    
    return is_alert,trigger_time,source,event,info,url


if __name__ == "__main__":
    df=pd.read_excel('D:\\Rudy\\Nex\\風控自動化\\data\\t_game_bet_log_0702_0704_test.xlsx')
    #print(first_judge_df_RTP_and_NW(df,score_threshold=5000,RTP_threshold=1.1))
    print(judge_history_RTP(df))