#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : 1925374620@qq.com
#  @文件         : 项目 [qqmusic] - App.py
#  @修改时间    : 2023-03-04 09:26:31
#  @上次修改    : 2023/3/4 下午9:26
import concurrent
import time
from concurrent.futures import Future

from flask import Flask, Response, request
from flask_cors import CORS
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from src.Common.Concurrency import Downloader

app: Flask = Flask(__name__, static_url_path="")

CORS(app, resources=r'/*')


@app.get("/")
def index():
    """
    返回主页面
    Returns:

    """
    return app.redirect("/index.html")


@app.get("/status")
def appState():
    return {
        'code': 200
    }


@app.post("/config")
def configSave():
    jsn = request.get_json()
    num = int(jsn['num'])
    location = jsn['folder']
    c.set_folder(location)
    c.initPool(num)
    return {
        'code': 200
    }


@app.get("/getConfig")
def getConfig():
    return {
        'num': c.getCurrentResize(),
        'folder': c.get_folder()
    }


@app.post("/download")
def add():
    from src.Common.Tools import downSingle
    print("准备开始下载任务")
    jsn = request.get_json()
    music = jsn['music']
    config = jsn['config']
    # downSingle(jsn)
    c.addTask(done, downSingle, music, c.get_folder(), config['onlyMatchSearchKey'], config['classificationMusicFile'])
    return {
        'code': 200
    }


c = Downloader()
c.initPool(16)
from web.API.qq import QQApi


def done(ret: Future):
    ret = ret.result()
    print(f"download over {ret}")


def executeFn(a1: str, a2: bool):
    time.sleep(4)
    return a1 + "a2 True" if a2 else "a2 False"


def Start():
    app.run(
        '0.0.0.0',
        8899,
        debug=True
    )
