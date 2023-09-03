#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : qiuchenly@outlook.com
#  @文件         : 项目 [qqmusic] - App.py
#  @修改时间    : 2023-07-28 10:52:00
#  @上次修改    : 2023/7/28 下午10:52
import json
import os.path
import time
from concurrent.futures import Future

from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from flaskSystem.src.Common.Concurrency import Downloader

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
    savelyric = jsn['lyric']
    save_config(location,num,savelyric)
    return {
        'code': 200
    }
    
def save_config(location,num,savelyric):
    c.set_folder(location)
    c.initPool(num)
    c.set_lyric(savelyric)
    with open("config.cfg", "w+") as cfg:
        cfg.write(json.dumps({
            "thread_num": num,
            "download_locate": location,
            "save_lyric": savelyric
        }))
        cfg.flush()


@app.get("/getConfig")
def getConfig():
    return {
        'num': c.getCurrentResize(),
        'folder': c.get_folder(),
        'lyric': c.get_lyric()
    }


@app.post("/download")
def add():
    from flaskSystem.src.Common.Tools import downSingle
    print("准备开始下载任务")
    jsn = request.get_json()
    music = jsn['music']
    config = jsn['config']
    # downSingle(jsn)
    c.addTask(done, downSingle, music, c.get_folder(), config)
    return {
        'code': 200
    }


c = Downloader()

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


# SocketIO

socketio = SocketIO()
socketio.init_app(app, cors_allowed_origins='*')

namespace = "qiuchenly"
@socketio.on('connect',namespace=namespace)
def connected_msg(socket):
    print(f"Client connected",socket)
    
@socketio.on('disconnect', namespace=namespace)
def disconnect_msg():
    print('client disconnected.')

@socketio.on('my_event', namespace=namespace)
def mtest_message(message):
    print(message)
    emit('my_response', {'data': message['data'], 'count': 1})

@app.after_request
def add_header(response):
    if 'text/plain' in response.headers['Content-Type']:
        response.headers['Content-Type'] = 'application/javascript; charset=utf-8'
    return response


def Start(port):
    c.initPool(16)
    if os.path.exists("config.cfg"):
        with open("config.cfg", "r") as cfg:
            cfg = cfg.read()
            cfg = json.loads(cfg)
            c.initPool(int(cfg['thread_num']))
            if os.path.exists(cfg['download_locate']):
                c.set_folder(cfg['download_locate'])
            else:
                print("路径不存在，使用默认下载目录:", c.get_folder())
                save_config(c.get_folder(),c.getCurrentResize())


    app.run(
        '0.0.0.0',
        port,
        debug=False
    )
    socketio.run(app, host='0.0.0.0', port=port)
