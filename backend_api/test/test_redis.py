import redis

try:
    client = redis.from_url("redis://localhost:6379/0", decode_responses=True)
    
    client.ping()
    print("Redis 连接成功!")
    
    client.set("test_key", "test_value")
    print("写入测试成功!")
    
    value = client.get("test_key")
    print(f"读取测试成功! 值: {value}")
    
    client.setex("temp_key", 10, "will_expire")
    print("过期时间设置成功!")
    
except redis.ConnectionError as e:
    print(f"Redis 连接失败: {e}")
except Exception as e:
    print(f"错误: {e}")