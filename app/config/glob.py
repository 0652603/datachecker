from datetime import datetime


# 唯一全局變量 用來做執行時間測試! 勿修改
sync_once_last_execute_time = datetime.now()

# 檢查間隔配置
check_interval = 15 # 幾秒檢查一次
check_buffer = 300 # 幾秒鐘緩衝

