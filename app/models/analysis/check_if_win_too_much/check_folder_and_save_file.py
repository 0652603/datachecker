import os
import shutil
from datetime import datetime, timedelta
# 示例 DataFrame
import pandas as pd
# 配置路径
base_path = 'app\\static'  # 替换为你的基础路径

def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

def get_current_date_folder(base_path):
    today = datetime.now().strftime('%Y-%m-%d')
    return os.path.join(base_path, today)

def save_dataframe_to_csv(df, base_path):
    current_time_str = datetime.now().strftime('%H-%M-%S')
    date_folder = get_current_date_folder(base_path)
    
    create_folder_if_not_exists(date_folder)
    
    csv_file_path = os.path.join(date_folder, f"data_{current_time_str}.csv")
    df.to_csv(csv_file_path, index=False)
    #print(f"DataFrame has been saved as {csv_file_path}")

def delete_old_folders(base_path, days_to_keep=3):
    today = datetime.now()
    cutoff_date = today - timedelta(days=days_to_keep)
    
    for folder_name in os.listdir(base_path):
        folder_path = os.path.join(base_path, folder_name)
        
        if os.path.isdir(folder_path):
            try:
                folder_date = datetime.strptime(folder_name, '%Y-%m-%d')
                if folder_date < cutoff_date:
                    shutil.rmtree(folder_path)
                    print(f"Deleted old folder: {folder_path}")
            except ValueError:
                # Skip non-date folders
                pass
def save_and_delete_folder_file(df):
    # 保存 DataFrame 到 CSV 文件
    save_dataframe_to_csv(df, base_path)
    # 获取当前时间
    now = datetime.now()
    # 检查当前时间是否在00:00:00到00:00:10之间
    if now.hour == 0 and now.minute < 10 and now.second < 60:
        delete_old_folders(base_path)
