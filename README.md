# 后端 + Redis + Poker

1. 后端：[FastAPI](https://fastapi.tiangolo.com/)
2. Poker：https://github.com/feymanpaper/Poker
3. Python 版本：3.10
4. 依赖环境：运行 `pip install -r requirements.txt` 构建[环境](requirements.txt)
5. 存储环境：[Redis](https://redis.io/)

## FastAPI

后端采用 FastAPI 框架搭建，详细代码见 [backend_api](backend_api/)。

## Poker

Poker 包装成 CLI，后端调用收集数据，详细代码见 [poker_engine.py](poker/poker_engine.py)。

## Redis

该项目未使用关系数据库进行存储（理论上关系数据库就足够应对），采用了 Redis 简单进行存储。

## 运行

> 此处采用了 [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main) 构建虚拟环境 `poker` 进行，因此首先运行 `conda activate poker` 激活虚拟环境 
>
> 初次运行前请配置好 Redis 环境。

1. 安装 Docker

    ```bash
    # 检查 Docker 是否已安装
    docker --version
    # 如果没有，请安装 Docker 
    ```

2. 启动 Redis

    ```bash
    docker run -d --name redis-server -p 6379:6379 redis:latest
    ```

3. 创建 .env 文件。在 [backend_api](backend_api/) 目录中创建 `.env` 文件。设置 Redis 等配置信息。例如：

   ```
   # Redis 配置
   REDIS_URL=redis://localhost:6379/0
   # REDIS_PASSWORD=your_password_here  # 如果需要密码
   TASK_TTL=86400  # 任务数据保留时间（秒）
   ```

4. 前 3 步在初次运行时配置好。后面再运行后端。使用 FastAPI 直接开启后端服务即可。

    ```bash
    cd backend_api/
    fastapi dev app_main.py
    # 或者运行 uvicorn app_main:app --reload
    ```