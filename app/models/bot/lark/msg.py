from datetime import datetime
import pytz
import requests
import json
import app.config.glob as glob

def alert(trigger_time:datetime, source:str,event:str, info:str, url:str):
    '''
    trigger_time: 檢查時間點
    source: 事件來源(ex: X平台)
    event: 觸發事件(被哪條規則捕獲)
    info: 詳細資訊
    url : (選填) 連結網址
    '''
    header = {"Content-Type": "application/json"}
    body = body_maker(trigger_time,source,event,info,url)
    requests.post(glob.lark_webhook_url, headers=header, data=json.dumps(body))

def body_maker(trigger_time:datetime, source:str,event:str, info:str, url:str =None):
    if url is None:
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
                                                        "text": "\n✴發生時間 :\n{dt}".format(dt= trigger_time.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
                                                },
                                                {
                                                        "tag": "text",
                                                        "text": "\n✴事件來源 :\n{src}".format(src= source)
                                                },
                                                {
                                                        "tag": "text",
                                                        "text": "\n✴觸發事件 :\n{eve}".format(eve= event)
                                                },
                                                {
                                                        "tag": "text",
                                                        "text": "\n✴事件內容 :\n{info}".format(info= info)
                                                },
                                                    
                                            ]
                                ]
                        }
                }
        }
}
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
                                                        "text": "\n✴發生時間 :\n{dt}".format(dt= trigger_time.strftime('%Y-%m-%d %H:%M:%S %Z%z'))
                                                },
                                                {
                                                        "tag": "text",
                                                        "text": "\n✴事件來源 :\n{src}".format(src= source)
                                                },
                                                {
                                                        "tag": "text",
                                                        "text": "\n✴觸發事件 :\n{eve}".format(eve= event)
                                                },
                                                {
                                                        "tag": "text",
                                                        "text": "\n✴事件內容 :\n{info}".format(info= info)
                                                },
                                                {
                                                        "tag": "a",
                                                        "text": "\n请查看",
                                                        "href": url
                                                },
                                                    
                                            ]
                                ]
                        }
                }
        }
}