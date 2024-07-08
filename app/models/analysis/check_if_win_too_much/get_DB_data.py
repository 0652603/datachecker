import pandas as pd
import pymysql
import pymysql.cursors
from datetime import datetime, timedelta
our_company_id_tuple=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 
                      27, 28, 29, 30, 31, 32, 33, 34, 35, 40, 41, 42, 43, 105, 109, 110, 111, 112, 113, 114, 115, 117, 
                      122, 125, 126, 127, 129, 132, 201, 202, 203, 204, 205, 301, 302, 303, 304, 305, 306, 307, 308, 
                      309, 310, 311, 312, 313, 314, 315, 316, 320, 323, 324, 801, 802, 803, 804, 901, 902, 903, 904)
def get_conn_cursor(host_id):
    conn = pymysql.connect(host = host_id, port = 3310, user = 'query1', password = 'query666!!P', 
                        database = 'log', charset = 'utf8mb4', autocommit = True)
    cursor = conn.cursor(cursor = pymysql.cursors.DictCursor)
    return conn,cursor

def get_DB_5_min_info(host_id,now):
    #now = datetime.now()
    time_minus_5_minutes = now - timedelta(minutes=5)
    current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    time_minus_5_minutes_str = time_minus_5_minutes.strftime("%Y-%m-%d %H:%M:%S")
    conn,cursor=get_conn_cursor(host_id)
    query = (
    "SELECT uid, companyId, agent, validBet, score, add_time, gameName,gameId,roundId "
    "FROM t_game_bet_log "
    "WHERE add_time >= '{time_minus_5_minutes_str}' "
    "AND add_time <= '{current_time_str}'"
    "AND gameId IN {our_company_id_tuple}"

     ).format(
    time_minus_5_minutes_str=time_minus_5_minutes_str,
    current_time_str=current_time_str,
    our_company_id_tuple=our_company_id_tuple
     )
    #print(query)
    cursor.execute(query)
    result=cursor.fetchall()  
    conn.close()
    cursor.close()
    result=pd.DataFrame(result)
    return result
def get_one_user_DB_14_days_info(host_id,uid,gameName,now):
    #now = datetime.now()
    start_of_today = datetime(now.year, now.month, now.day)
    start_of_14_days_ago = start_of_today - timedelta(days=14)
    current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    start_of_14_days_ago_str = start_of_14_days_ago.strftime("%Y-%m-%d %H:%M:%S")
    conn,cursor=get_conn_cursor(host_id)
    # 构建 SQL 查询
    query = (
        "SELECT uid, companyId, agent, validBet, score, add_time, gameName,gameId,roundId "
        "FROM t_game_bet_log "
        "WHERE add_time >= '{start_of_14_days_ago_str}' "
        "AND add_time <= '{current_time_str}' "
        "AND uid = '{uid}'"
        "AND gameName = '{gameName}'"
        "AND gameId IN {our_company_id_tuple}"
    ).format(
        start_of_14_days_ago_str=start_of_14_days_ago_str,
        current_time_str=current_time_str,
        uid=uid,
        gameName=gameName,
        our_company_id_tuple=our_company_id_tuple
    )
    cursor.execute(query)
    result=cursor.fetchall()  
    conn.close()
    cursor.close()
    result=pd.DataFrame(result)
    return result

def get_one_user_DB_history_info(host_id,uid,gameName):
    conn,cursor=get_conn_cursor(host_id)
    # 构建 SQL 查询
    query = (
        "SELECT uid, companyId, agent, validBet, score, add_time, gameName,gameId,roundId "
        "FROM t_game_bet_log "
        "WHERE uid = '{uid}'"
        "AND gameName = '{gameName}'"
        "AND gameId IN {our_company_id_tuple}"
    ).format(
        uid=uid,
        gameName=gameName,
        our_company_id_tuple=our_company_id_tuple
    )
    cursor.execute(query)
    result=cursor.fetchall()  
    conn.close()
    cursor.close()
    result=pd.DataFrame(result)
    return result

def build_sql_query(row):
    uid = row['uid']
    gameName = row['gameName']
    roundId_tuple = row['roundId']
    query = (
        "SELECT uid, companyId, agent, validBet, score, add_time, gameName, gameId, roundId "
        "FROM log.t_game_bet_log "
        "WHERE uid = '{uid}' "
        "AND gameName = '{gameName}' "
        "AND roundId IN {roundId_tuple}"
    ).format(
        uid=uid,
        gameName=gameName,
        roundId_tuple=roundId_tuple
    )
    return query

if __name__ == "__main__":
    print(get_one_user_DB_14_days_info(host_id='10.97.74.214',uid=793166,gameName='麻將胡了2'))