import pandas as pd

def get_currency_rate(path='app\\static\\',filename='company.xlsx'):
    company_currency    = pd.read_excel(path+filename,sheet_name='公司幣別表')
    currency_rate       = pd.read_excel(path+filename,sheet_name='幣別')
    currency_rate       = currency_rate[['幣別代碼','實際幣值']]
    currency_list       = currency_rate['幣別代碼'].tolist()
    currency_value_list = currency_rate['實際幣值'].tolist()
    company_currency    = company_currency[['company_id','幣別代碼']]
    company_currency['currency_rate'] = 'NaN'
    
    for index in range(company_currency.shape[0]):
        for currency_list_index in range(len(currency_list)):
            if company_currency.loc[index,'幣別代碼']==currency_list[currency_list_index]:
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