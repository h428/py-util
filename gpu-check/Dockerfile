FROM python:3.7

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 文件到镜像
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt --extra-index-url https://download.pytorch.org/whl/cu117

# 拷贝当前目录下的源码到 Docker 镜像
COPY ./app /app

# 添加数据卷以暴露源码
VOLUME [ "/app" ]

# 指定 Docker 容器启动时的默认命令
CMD ["python", "/app/main.py"]