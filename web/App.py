#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : 1925374620@qq.com
#  @文件         : 项目 [qqmusic] - App.py
#  @修改时间    : 2023-03-05 10:51:25
#  @上次修改    : 2023/3/5 下午10:51
import time
from concurrent.futures import Future

from flask import Flask, request
from flask_cors import CORS

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
    platform = jsn['platform']
    config = jsn['config']
    # downSingle(jsn)
    c.addTask(done, downSingle, music, platform, c.get_folder(), config['onlyMatchSearchKey'],
              config['classificationMusicFile'])
    return {
        'code': 200
    }


c = Downloader()
c.initPool(16)


def done(ret: Future):
    """
    得到下载返回结果
    Args:
        ret:

    Returns:

    """
    excepts = ret.exception()
    ret = ret.result()
    if ret['code'] != 200 or excepts:
        print(f"下载失败," + ret['msg'], excepts)
    else:
        print(f"下载成功。")


def executeFn(a1: str, a2: bool):
    """
    测试线程池函数 实际上没有被调用
    Args:
        a1:
        a2:

    Returns:

    """
    time.sleep(4)
    return a1 + "a2 True" if a2 else "a2 False"


def Start():
    app.run(
        '0.0.0.0',
        8899,
        debug=False
    )
