# DeviceGuard_backend

1. 后端：[FastAPI](https://fastapi.tiangolo.com/)
2. Poker：https://github.com/feymanpaper/Poker
3. GKD：https://github.com/feymanpaper/GKD_subscription
4. ADB：https://developer.android.com/tools/adb?hl=zh-cn
5. AAPT：https://developer.android.com/tools/aapt2?hl=zh-cn
6. Python 版本：3.10，Node 版本：22.14
7. 依赖环境：运行 `pip install -r requirements.txt` 构建[Python 环境](requirements.txt)
8. 存储环境：[Redis](https://redis.io/)

## FastAPI

后端采用 FastAPI 框架搭建，详细代码见 [backend_api](backend_api/)。

## Poker

Poker 包装成 CLI，后端调用收集数据，详细代码见 [poker_engine.py](poker/poker_engine.py)。

## GKD

GKD 同样包装成 CLI，后端收集数据后进行调用生成消融规则，详细代码见 [run_match_ele.py](gkd_subscription/run_match_ele.py)

## Redis

该项目未使用关系数据库进行存储（理论上关系数据库就足够应对），采用了 Redis 简单进行存储。

## ADB + AAPT

项目中使用了 ADB 和 AAPT 工具与 Android 设备进行连接交互，工具代码见 [adb_service.py](backend_api/adb_service.py)

## 运行

> 此处采用了 [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main) 构建虚拟环境 `poker` 进行，因此首先运行 `conda activate poker` 激活虚拟环境 
>
> 初次运行前请配置好 Redis 环境。
> 
> 运行前请确保提前安装好了 ADB 工具和 AAPT 工具。
> 
> - ADB 的下载链接：https://blog.csdn.net/x2584179909/article/details/108319973
> 
> - AAPT 的下载链接：https://aaptdownload.com/

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

4. 配置 GKD 环境

    ```bash
    cd gkd_subscription
    pnmp install
    ```

    > 注意这里需要提前配置好 `pnmp` 环境。可参考 [GKD_subscription](https://github.com/feymanpaper/GKD_subscription) 进行环境配置

5. **前 4 步在初次运行时配置好**。后面再运行后端。使用 FastAPI 直接开启后端服务即可。

    ```bash
    cd backend_api/
    fastapi dev app_main.py
    # 或者运行 uvicorn app_main:app --reload
    ```

## 弹框消融规则订阅链接

> GKD 原本的订阅链接如下，如果需要稳定的弹框消融规则推荐使用下面的链接
>
> ```
> https://fastly.jsdelivr.net/gh/feymanpaper/GKD_subscription@main/dist/gkd.json5
> ```
>

但为了方便后端开发，我们将 **feymanpaper** 的 GKD_subscription 进行了 Fork 后得到了新的订阅链接：

```
https://fastly.jsdelivr.net/gh/dgliang/GKD_subscription@main/dist/gkd.json5
```