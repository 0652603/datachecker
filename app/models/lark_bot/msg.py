from datetime import datetime
import pytz
import requests
import json

def alert(msg:str,msg2:str):
    now_local = datetime.now(pytz.timezone('Asia/Taipei'))
    url = 'https://open.larksuite.com/open-apis/bot/v2/hook/f1444632-a83c-44c8-9576-6d444e2c5428'
    header = {"Content-Type": "application/json"}
    body = body_maker(msg,msg2,now_local)
    requests.post(url, headers=header, data=json.dumps(body))

def body_maker(msg, msg2,now_local):
    return {
        "msg_type": "post",
        "content": {
                "post": {
                        "zh_cn": {
                                "title": "【🌟風控告警🌟】",
                                "content": [
                                            [   
                                                {
                                                            "tag": "at",
                                                            "user_id": "all",
                                                            "user_name": "所有人"
                                                },  
                                                {
                                                        "tag": "text",
                                                        "text": "\n✴發生時間 :\n{dt}".format(dt= now_local.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
                                                },
                                                {
                                                        "tag": "text",
                                                        "text": "\n✴事件來源 :\n平台A"
                                                },
                                                {
                                                        "tag": "text",
                                                        "text": "\n✴觸發事件 :\n{t}".format(t= msg)
                                                },
                                                {
                                                        "tag": "text",
                                                        "text": "\n✴事件內容 :\n{t}".format(t= msg2)
                                                },
                                                {
                                                        "tag": "a",
                                                        "text": "\n请查看",
                                                        "href": "https://open.larksuite.com/document/client-docs/bot-v3/add-custom-bot"
                                                },
                                                    
                                            ]
                                ]
                        }
                }
        }
}