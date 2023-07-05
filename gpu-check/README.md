# gpu-check

检查 torch cuda 可用性的项目，同时提供了基础的 torch 运行环境，以 docker 镜像形式提供运行环境。

该项目的目的主要是为了快速测试 gpu 版本的 torch 是否可用，同时学习基于 docker 镜像的 Python 工程部署。

## 构建镜像

获取源码后，执行 `docker build -t h428/gpu-check .` 进行构建，相关镜像已经传到 Docker Hub，可以直接 `docker pull h428/gpu-check` 下载镜像。

## 测试镜像

执行 `docker run -it --gpus all h428/gpu-check` 测试在当前机器是否可以基于 docker 虚拟环境做测试，如果不行，说明 nvidia 相关工具没有装好，需要先安装 nvidia docker