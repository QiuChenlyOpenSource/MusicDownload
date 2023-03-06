# 项目介绍

Create & Design By QiuChenly.

这是一个批量下载 QQ 音乐/酷我音乐/网易云会员无损音质歌曲的脚本,技术含量并不是很大,仅供参考。

提示：由于QQ音乐接口访问频率限制 有时候歌曲获取不到 多刷新几次就好了

```
前端技术: Vue3+TS+Pinia+ElementUI Plus

后端技术: Python3.9 + Flask + Concurrency协程
```

# 使用方法

[//]: # (为确保账户安全，用户token本地按需保留。且线上服务使用扫码登录。)

[//]: # (![img_3.png]&#40;md/media/img_3.png&#41;)

### 如果你需要生成 requirements.txt 文件

```bash
pip install pipreqs # 安装
pipreqs ./ --encoding=utf8 --force # 在文件夹中执行
```

### 1. 安装环境

首先安装最新的 python3 到你的操作系统里。

以下所有操作皆默认假设当前目录在(Windows) D:/Downloads/QQFlacDownloader/ 或者(Unix/Linux) ~/Download/QQFlacDownloader/

如果安装依赖包出现 404 错误或者太慢，可以用下面的代码切换到清华大学服务器安装。

```bash
# 设置python的依赖安装镜像服务器为清华大学服务器
# 
pip3 config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

```bash
pip3 install -r requirements.txt # 安装软件依赖必须包
```

### 2. 进入软件包目录下启动软件

终端/控制台 进入到本文件所在的目录 执行以下指令:

```bash
python3 MainServer.py
```

启动后应该能看到这些信息，即表示你启动成功。
![img_1.png](img_1.png)

然后google chrome之类的浏览器打开[http://127.0.0.1:8899](http://127.0.0.1:8899)即可打开新世界

# 新特性

| 功能                | 状态  | 附加说明                                                 |
|-------------------|-----|------------------------------------------------------|
| 网易云会员歌曲解析下载       | 已完成 | 版权问题灰色歌曲没有CDN资源缓存 无法下载                               |
| 酷我音乐无损音质下载        | 已完成 | 部分没有flac音质版本的歌曲可能无法下载                                |
| QQ音乐无损会员/高解析度无损下载 | 已完成 | 第三方服务器好像已经挂了 估计这个服务器qq被封了 暂时用不了 搜索不到歌曲的话多搜索几次或者换酷我接口 |

基于web的友好界面出来啦

![img_2.png](md/media/img_2.png)
![img_3.png](md/media/img_3.png)
![img_1.png](md/media/img_1.png)
---

# 声明

本代码 GPLV3 授权使用，禁止商业用途，仅供研究学习 python 技术使用，不得使用本代码进行任何形式的牟利/贩卖/传播，禁止在 qq
群传播，本项目仅供个人私下研究学习使用，请支持 QQ 正版音乐！

下载的音乐文件在试听后请在 24 小时内删除，谢谢！
仅限在中国大陆的宪法许可情况下使用，用户造成的一切法律责任与后果都由您自己独自承担，作者概不负责！

本项目仅限研究交流学习使用。

# 其他资料

[早期接口 QMD Apk的逆向过程](./md/README.md)