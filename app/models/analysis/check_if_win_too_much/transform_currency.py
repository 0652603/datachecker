import pandas as pd
from get_DB_data import get_t_company_info,get_t_currency_math_info
import re

def contains_hash_like_strings(my_string):
    # 定义要匹配的模式
    pattern = re.compile(r'hash|哈希|haxi', re.IGNORECASE)
    # 搜索模式
    if pattern.search(my_string):
        return True
    else:
        return False
def trans_form_hash_currency_to_USD(host_id='10.97.74.214',databse_name='usercenter',table_name='t_company'):
    t_company_info=get_t_company_info(host_id=host_id,databse_name=databse_name,table_name=table_name)
    for index in range(t_company_info.shape[0]):
        if contains_hash_like_strings(t_company_info.loc[index,'company_name']):
            #print(index)
            #print(t_company_info.loc[index,'company_name'])
            t_company_info.loc[index,'currency']='USD'
    return  t_company_info    

           
def get_currency_rate(path='app\\static\\',filename='company.xlsx'):
    t_company_info=trans_form_hash_currency_to_USD(host_id='10.97.74.214',databse_name='usercenter',table_name='t_company')
    company_currency    = t_company_info
    currency_rate       = get_t_currency_math_info(host_id='10.97.74.214',databse_name='usercenter')
    currency_rate       = currency_rate[['currency','currency_scale_value']]
    currency_list       = currency_rate['currency'].tolist()
    currency_value_list = currency_rate['currency_scale_value'].tolist()
    company_currency    = company_currency[['company_id','currency']]
    company_currency['currency_rate'] = 'NaN'
    
    for index in range(company_currency.shape[0]):
        for currency_list_index in range(len(currency_list)):
            if company_currency.loc[index,'currency']==currency_list[currency_list_index]:
                company_currency.loc[index,'currency_rate']=currency_value_list[currency_list_index]
    return company_currency

def get_transform_all_to_CNY_df(df):
    company_currency      = get_currency_rate()
    company_id_list       = company_currency['company_id'].tolist()
    currency_rate_list    = company_currency['currency_rate'].tolist()
    df_company_id_list    = df['companyId'].tolist()
    df_currency_rate_list = [0]*len(df_company_id_list)

    for index in range(len(company_id_list)):
            for df_company_id_list_index in range(len(df_company_id_list)):
                if (company_id_list[index])==(df_company_id_list[df_company_id_list_index]):
                    df_currency_rate_list[df_company_id_list_index]=(currency_rate_list[index])
    
    df['currency_rate'] = df_currency_rate_list
    df['validBet']      = df['validBet'].astype(float)/df['currency_rate'].astype(float)
    df['score']         = df['score'].astype(float)/df['currency_rate'].astype(float)
    df.to_csv('app\\static\\data.csv')
    
    return df