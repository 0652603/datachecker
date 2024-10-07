#get chat id
import requests
import json

from tabulate import tabulate
import asyncio
from aiogram import Bot
import logging
class Send_message:
    # 构造函数，初始化实例属性
    def __init__(self):
        #self.webhook_url = 'https://open.larksuite.com/open-apis/bot/v2/hook/733ed977-254b-49d7-97b2-f06c066da81f' #for 黑名單群組
        self.webhook_url = 'https://open.larksuite.com/open-apis/bot/v2/hook/a343077c-ee8c-4980-a8ad-0512668f373a' #for 風控問題群組

    def get_chat_id_by_log(self):
         # 配置日志
        logging.basicConfig(level=logging.INFO, format='%(message)s')
        # 替換成你自己的 bot_token
        bot_token = '7533948035:AAHz4p_-o-Nd3B9cGk14ilIgwlcXD9dz_6w'
        url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
        # 發送 GET 請求
        response = requests.get(url)
        # 檢查請求是否成功
        if response.status_code == 200:
            updates = response.json()
            
            # 确保是字典
            if isinstance(updates, dict):
                updates_list = list(updates.items())  # 将字典转换为键值对的列表
                logging.info(updates_list[-10:])      # 输出最后 10 条记录
            else:
                logging.info(updates[-10:])  # 如果是列表，仍然可以使用负索引
        else:
            logging.error(f"Failed to get updates, status code: {response.status_code}")

    def get_TG_chat_id(self):
       
        # 替換成你自己的 bot_token
        bot_token = '7533948035:AAHz4p_-o-Nd3B9cGk14ilIgwlcXD9dz_6w'
        url = f'https://api.telegram.org/bot{bot_token}/getUpdates'

        # 發送 GET 請求
        response = requests.get(url)

        # 檢查請求是否成功
        if response.status_code == 200:
            # 解析 JSON 數據
            updates = response.json()

            # 顯示更新的數據
            print(updates)
            # 将字典保存为文本文件
            with open('test.txt', 'w', encoding='utf-8') as f:
                for key, value in updates.items():
                    f.write(f"{key}: {value}\n")  # 写入每个键值对
                    # 使用 \r 覆盖之前的輸出
                    #print(f"\r{updates}", end='', flush=True)
        else:
            print(f"Failed to get updates, status code: {response.status_code}")

    def check_request(self):
        # 检查请求是否成功
        if self.response.status_code == 200:
            print("Message sent successfully!")
        else:
            print(f"Failed to send message. Status code: {self.response.status_code}, response: {self.response.text}")
    
    def send_message_lark(self):
        df=self.judge.main()
        if df is not None:
            if not df.empty:
                part_of_df=df[['third_account','agent','company_key','gameName','black_list_info','statement']]
                # 将 DataFrame 转换为 Markdown 表格
                message_text = "| 玩家                       | 代理ID    | company_key | 遊戲         | 黑名單     | 設置原因                                                        |\n"
                message_text +="| -------------------------| ------------| ----------------  |------------- |------------  |------------------------------------------------------------|\n"
                for index, row in part_of_df.iterrows():
                    message_text += f"| {row['third_account']} | {row['agent']}  | {row['company_key']} | {row['gameName']} | {row['black_list_info']}  | {row['statement']} |\n"
            else:
                message_text="->  昨日無贏錢玩家，無須設置黑名單"
        else:
            message_text="->  昨日無贏錢玩家，無須設置黑名單"

        # 要发送的消息内容
        message = {
            "msg_type": "text",
            "content": {
                "text": f"Rudy的機器人發訊息做黑名單設置\n\n{message_text}"
            }
        }
        self.response = requests.post(self.webhook_url, headers={'Content-Type': 'application/json'}, data=json.dumps(message))
        self.check_request()
    def send_message_TG(self,result):
        #   alert(result["trigger_time"],result["source"],result["event"],result["info"],result["url"])
        message_text=""
        if result is not None:
            keys_to_keep = ['trigger_time', 'source','  event','info']  # 你想要保留的键
            new_result = {key: result[key] for key in keys_to_keep if key in result}  
            # 遍历 result 字典的每个键值对
            for key, value in new_result.items():
                # 确保 value 是一个字典并包含所需的键
                if isinstance(value, dict):
                    message_text += f"source: {value.get('source', 'N/A')}\n" \
                                    f"event: {value.get('event', 'N/A')}\n" \
                                    f"info: {value.get('info', 'N/A')}\n" \
                                    "-------------------------------------------------------------------------------------------------------------------------------------------------\n"
                else:   
                    message_text += f"{key},{value}\n"
                
        # 要发送的消息内容
        message = {
            "msg_type": "text",
            "content": {
                "text": f"風控告警 \n\n{message_text}"
            }
        }
        #self.response = requests.post(self.webhook_url, headers={'Content-Type': 'application/json'}, data=json.dumps(message))

        # 设置你的机器人 Token 和聊天ID（你要发送消息的目标）
        bot_token = '7533948035:AAHz4p_-o-Nd3B9cGk14ilIgwlcXD9dz_6w' #機器人的token
        #chat_id = '6681028339'  # 機器人自己的
        #chat_id =-1002378501406  # TG風控維護群的
        #chat_id =-1002313031217  # test群組的
        chat_id =-1002316141152 #風控告警
        bot = Bot(token=bot_token)
        async def send_message():
            await bot.send_message(chat_id=chat_id, text=message_text)
        asyncio.run(send_message())
    


if __name__ == "__main__":
    send_message = Send_message()
    send_message.send_message_TG()