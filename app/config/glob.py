from datetime import datetime


# 唯一全局變量 用來做執行時間測試! 勿修改
sync_once_last_execute_time = datetime.now()

# 檢查間隔配置
check_interval = 5*60    # 幾分鐘檢查一次
#check_interval = 15 # test
check_buffer = 5*60 # 幾分鐘緩衝


# bot webhook:
lark_webhook_url = 'https://open.larksuite.com/open-apis/bot/v2/hook/f1444632-a83c-44c8-9576-6d444e2c5428'

