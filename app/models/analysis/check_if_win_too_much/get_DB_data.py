import pandas as pd
import pymysql
import pymysql.cursors
from datetime import datetime, timedelta
import re

our_game_id_tuple=(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 
                      27, 28, 29, 30, 31, 32, 33, 34, 35, 40, 41, 42, 43, 105, 109, 110, 111, 112, 113, 114, 115, 117, 
                      122, 125, 126, 127, 129, 132, 201, 202, 203, 204, 205, 301, 302, 303, 304, 305, 306, 307, 308, 
                      309, 310, 311, 312, 313, 314, 315, 316, 320, 323, 324, 801, 802, 803, 804, 901, 902, 903, 904)
def get_conn_cursor(host_id,databse_name='log'):
    conn = pymysql.connect(host = host_id, port = 3320, user = 'query1', password = 'query666!!P', 
                        database = databse_name, charset = 'utf8mb4', autocommit = True)
    cursor = conn.cursor(cursor = pymysql.cursors.DictCursor)
    return conn,cursor

def contains_like_strings(my_string):
    # 定义要匹配的模式
    pattern = re.compile(r'1971868|1990687|1847665|1784194|2012241', re.IGNORECASE)
    #pattern = re.compile(r'0', re.IGNORECASE)#test
    # 搜索模式
    return bool(pattern.search(my_string))

def get_company_id_tuple(host_id='10.97.74.214',databse_name='usercenter',table_name='t_company'):
    t_company_info = get_t_company_info(host_id=host_id, databse_name=databse_name, table_name=table_name)
    # 过滤掉 `company_key` 中包含特定模式的行
    filtered_t_company_info = t_company_info[~t_company_info['company_key'].apply(contains_like_strings)]
    
    # 提取 `company_id` 列并转换为 tuple
    company_id_tuple = tuple(filtered_t_company_info['company_id'])
    
    return company_id_tuple


def get_DB_5_min_info(host_id,now,company_id_tuple):
    
    #now = datetime.now()
    #now = datetime(2024, 8, 27, 20, 15, 13) #test
    time_minus_5_minutes = now - timedelta(minutes=30)
    #Ztime_minus_5_minutes = now - timedelta(minutes=90)
    #time_minus_5_minutes = now - timedelta(minutes=120)#test
    current_time_str = now.strftime("%Y-%m-%d %H:%M:%S")
    time_minus_5_minutes_str = time_minus_5_minutes.strftime("%Y-%m-%d %H:%M:%S")
    conn,cursor=get_conn_cursor(host_id)
    query = (
    "SELECT uid, companyId, agent, validBet, score, add_time, gameName,gameId,roundId,ip "
    "FROM t_game_bet_log "
    "WHERE add_time >= '{time_minus_5_minutes_str}' "
    "AND add_time <= '{current_time_str}' "
    "AND gameId IN {our_game_id_tuple} "
    "AND companyId IN {company_id_tuple} "

     ).format(
    time_minus_5_minutes_str=time_minus_5_minutes_str,
    current_time_str=current_time_str,
    our_game_id_tuple=our_game_id_tuple,
    company_id_tuple=company_id_tuple
     )
    #print(query)
    cursor.execute(query)
    result=cursor.fetchall()  
    conn.close()
    cursor.close()
    result=pd.DataFrame(result)
    return result
def get_one_user_DB_14_days_info(host_id,uid,gameName,now,company_id_tuple):
    #now = datetime.now()
    #now = datetime(2024, 8, 27, 20, 15, 13) #test
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
        "AND uid = '{uid}' "
        "AND gameName = '{gameName}' "
        "AND gameId IN {our_game_id_tuple} "
        "AND companyId IN {company_id_tuple} "
    ).format(
        start_of_14_days_ago_str=start_of_14_days_ago_str,
        current_time_str=current_time_str,
        uid=uid,
        gameName=gameName,
        our_game_id_tuple=our_game_id_tuple,
        company_id_tuple=company_id_tuple
    )
    cursor.execute(query)
    result=cursor.fetchall()  
    conn.close()
    cursor.close()
    result=pd.DataFrame(result)
    return result

def get_one_user_DB_history_info(host_id,uid,gameName,company_id_tuple):
    conn,cursor=get_conn_cursor(host_id)
    # 构建 SQL 查询
    query = (
        "SELECT uid, companyId, agent, validBet, score, add_time, gameName,gameId,roundId "
        "FROM t_game_bet_log "
        "WHERE uid = '{uid}' "
        "AND gameName = '{gameName}' "
        "AND gameId IN {our_game_id_tuple} "
        "AND companyId IN {company_id_tuple} "

    ).format(
        uid=uid,
        gameName=gameName,
        our_game_id_tuple=our_game_id_tuple,
        company_id_tuple=company_id_tuple
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
        "AND roundId IN {roundId_tuple} "
    ).format(
        uid=uid,
        gameName=gameName,
        roundId_tuple=roundId_tuple
    )
    return query

def get_company_name_info(host_id,databse_name,company_id):
    conn,cursor=get_conn_cursor(host_id,databse_name)
    # 构建 SQL 查询
    query = (
        "SELECT company_name,company_id "
        "FROM t_company "
        "WHERE  company_id= '{company_id}' "
    ).format(
        company_id=company_id,
    )
    cursor.execute(query)
    result=cursor.fetchall()  
    conn.close()
    cursor.close()
    result=pd.DataFrame(result)
    return result

def get_t_company_info(host_id,databse_name,table_name):
    conn,cursor=get_conn_cursor(host_id,databse_name)
    # 构建 SQL 查询
    query = (
        "SELECT company_name,company_key,company_id,currency "
        "FROM {table_name} "
    ).format(
        table_name=table_name
             )
    cursor.execute(query)
    result=cursor.fetchall()  
    conn.close()
    cursor.close()
    result=pd.DataFrame(result)
    return result

def get_t_company_info_to_transform_currency(host_id,databse_name,table_name,company_id_tuple):
    conn,cursor=get_conn_cursor(host_id,databse_name)
    # 构建 SQL 查询
    query = (
        "SELECT company_name,company_key,company_id,currency "
        "FROM {table_name}  "
        "WHERE  company_id IN  {company_id_tuple} "
    ).format(
        table_name=table_name,
        company_id_tuple=company_id_tuple
             )
    cursor.execute(query)
    result=cursor.fetchall()  
    conn.close()
    cursor.close()
    result=pd.DataFrame(result)
    return result

def get_t_currency_math_info(host_id,databse_name):
    conn,cursor=get_conn_cursor(host_id,databse_name)
    # 构建 SQL 查询
    query = (
        "SELECT currency,currency_scale_value "
        "FROM t_currency_math "
    )
    cursor.execute(query)
    result=cursor.fetchall()  
    conn.close()
    cursor.close()
    result=pd.DataFrame(result)
    return result

if __name__ == "__main__":
    print(get_one_user_DB_14_days_info(host_id='10.97.74.214',uid=793166,gameName='麻將胡了2'))