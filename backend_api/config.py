import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Redis 配置
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)
    TASK_TTL = int(os.getenv("TASK_TTL", 86400))  # 24小时
    
    # 如果需要密码认证
    @classmethod
    def get_redis_url(cls):
        if cls.REDIS_PASSWORD:
            # redis://:password@host:port/db
            base_url = cls.REDIS_URL.replace("redis://", "")
            return f"redis://:{cls.REDIS_PASSWORD}@{base_url}"
        return cls.REDIS_URL
