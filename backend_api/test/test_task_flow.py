import requests
import time
import json

BASE_URL = "http://localhost:8000"

def test_task_flow():
    print("1. 提交任务...")
    response = requests.post(
        f"{BASE_URL}/api/run",
        json={"pkg": "com.test", "app": "TestApp"}
    )
    print(f"   响应: {response.json()}")
    task_id = response.json()["task_id"]
    
    print("\n2. 查询任务状态...")
    for i in range(10):
        time.sleep(2)
        response = requests.get(f"{BASE_URL}/api/task/{task_id}/status")
        status = response.json()
        print(f"   [{i+1}] 状态: {status['status']}, 进度: {status['progress']}")
        
        if status['status'] in ['completed', 'failed']:
            break
    
    print("\n3. 健康检查...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"   响应: {json.dumps(response.json(), indent=2)}")
    
    print("\n4. 列出所有任务...")
    response = requests.get(f"{BASE_URL}/api/tasks")
    print(f"   响应: {response.json()}")

if __name__ == "__main__":
    test_task_flow()