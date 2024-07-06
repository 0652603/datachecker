import uvicorn

# source .venv/Scripts/activate
# python main.py
# --------- API ---------
# localhost:8000/start
# localhost:8000/shutdown
# localhost:8000/isalive


# 是否需要做reload(動態更新:當服務on起時每次更新儲存專案都會刷新服務)
is_reload = True

# 程序外部入口點，呼叫APP內的run啟動服務
if __name__ == "__main__" :
    uvicorn.run("app.run:app", host= "0.0.0.0", port= 8000, reload= is_reload)
    