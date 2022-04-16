FROM ubuntu:latest
LABEL maintainer="jeep.jipu@gmail.com" version="1.0"
WORKDIR /root/
# 换源
# RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak
# COPY ./_mirror_cn/aliyun-sources.list /etc/apt/sources.list
# COPY ./_mirror_cn/pip.conf /root/.pip/pip.conf
# 安装pip
RUN apt update && apt install -y python3-pip && pip install --upgrade pip
# 安装 beancount
RUN pip install beancount fava

# 数据文件
RUN mkdir /root/beancount
COPY beancount/moneybook.bean /root/beancount/moneybook.bean

# 启动脚本
COPY beancount/start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 5000
