from flaskSystem.App import app
from flaskSystem.App import c
@app.get("/files/getAllFileList")
def getAllFileList():
    return {
        'code': 200,
        'list': [],
        'locate':c.get_folder(),
        'threadNumber':c.getCurrentResize(),
        'page': 1
    }


def init():
    pass
