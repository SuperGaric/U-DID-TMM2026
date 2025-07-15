FROM ubuntu:latest

# 设置构建参数，用于代理配置
ARG HTTP_PROXY
ARG HTTPS_PROXY

# 设置环境变量以使用代理
ENV http_proxy=${HTTP_PROXY}
ENV https_proxy=${HTTPS_PROXY}

# 使用阿里云的源替换默认的 Ubuntu 源
RUN sed -i 's|http://archive.ubuntu.com/ubuntu/|http://mirrors.aliyun.com/ubuntu/|g' /etc/apt/sources.list

# 更新包列表并安装常用工具
RUN apt-get update && \
    apt-get install -y curl

# 设置工作目录
WORKDIR /root

# 运行一个交互式 shell
CMD ["/bin/bash"]

