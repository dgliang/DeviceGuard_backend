import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Redis 配置
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
    TASK_TTL = int(os.getenv("TASK_TTL", 86400))  # 24小时

    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    GITHUB_OWNER = os.getenv("GITHUB_OWNER", "dgliang")
    GITHUB_REPO = os.getenv("GITHUB_REPO", "GKD_subscription")
    GITHUB_MAIN_BRANCH = os.getenv("GITHUB_MAIN_BRANCH", "main")
    GITHUB_WORKFLOW_FILE = os.getenv("GITHUB_WORKFLOW_FILE", "build_release.yml")
    GITHUB_API_BASE = os.getenv("GITHUB_API_BASE", "https://api.github.com")
    GKD_REPO_PATH = os.getenv("GKD_REPO_PATH", "../GKD_subscription")

    # 数据收集路径
    COLLECTED_BASE_DIR = os.getenv("COLLECTED_BASE_DIR", "../poker/collectData")

    # 如果需要密码认证
    @classmethod
    def get_redis_url(cls):
        if cls.REDIS_PASSWORD:
            # redis://:password@host:port/db
            base_url = cls.REDIS_URL.replace("redis://", "")
            return f"redis://:{cls.REDIS_PASSWORD}@{base_url}"
        return cls.REDIS_URL
