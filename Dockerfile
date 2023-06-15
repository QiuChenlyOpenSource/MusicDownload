FROM python:3.9-slim-buster

WORKDIR /workspace

ADD ./ /workspace

RUN pip3 install --no-cache-dir --upgrade pip  -i https://mirrors.bfsu.edu.cn/pypi/web/simple && \
        pip3 install --no-cache-dir -r /workspace/requirements.txt -i https://mirrors.bfsu.edu.cn/pypi/web/simple

EXPOSE 8899

CMD ["python3", "MainServer.py"]