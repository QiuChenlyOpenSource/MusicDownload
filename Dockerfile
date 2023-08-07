FROM python:3.11-slim-buster

LABEL name="QQFlacMusicDownloader"

ENV TZ Asia/Shanghai
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN     apt-get update && apt-get install -y \
        gcc g++ libjpeg-dev zlib1g-dev \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /workspace

COPY ./ .

RUN pip3 install --no-cache-dir --upgrade pip -i https://mirrors.bfsu.edu.cn/pypi/web/simple && \
    pip3 install --no-cache-dir -r requirements.txt -i https://mirrors.bfsu.edu.cn/pypi/web/simple

EXPOSE 8899

CMD ["python3", "MainServer.py"]
