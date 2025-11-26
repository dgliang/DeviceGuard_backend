# 后端 + Poker

1. 后端：[FastAPI](https://fastapi.tiangolo.com/)
2. Poker：https://github.com/feymanpaper/Poker
3. Python 版本：3.10
4. 依赖环境：运行 `pip install -r requirements.txt` 构建[环境](requirements.txt)

## FastAPI

后端采用 FastAPI 框架搭建，详细代码见 [backend_api](backend_api/)。

## Poker

Poker 包装成 CLI，后端调用收集数据，详细代码见 [poker_engine.py](poker/poker_engine.py)。

## 运行

> 此处采用了 [Miniconda](https://www.anaconda.com/docs/getting-started/miniconda/main) 构建虚拟环境 `poker` 进行，因此首先运行 `conda activate poker` 激活虚拟环境

1. 运行后端。使用 FastAPI 直接开启后端服务即可。

    ```bash
    cd backend_api/
    fastapi dev app_main.py
    ```