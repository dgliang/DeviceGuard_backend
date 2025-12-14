import subprocess
import os
import re
import sys

def get_app_name_from_package(package_name):
    """
    根据包名获取应用名称
    
    Args:
        package_name: 应用包名，如 com.ss.android.article.news
    
    Returns:
        应用名称，如 今日头条
    """
    try:
        # 1. 获取 APK 路径
        print(f"正在查找包 {package_name} 的路径...")
        result = subprocess.run(
            ['adb', 'shell', 'pm', 'path', package_name],
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode != 0:
            print(f"错误: 未找到包 {package_name}")
            return None
        
        # 解析 APK 路径
        apk_path = result.stdout.strip()
        if apk_path.startswith('package:'):
            apk_path = apk_path[8:]  # 移除 'package:' 前缀
        
        print(f"找到 APK 路径: {apk_path}")
        
        # 2. 拉取 APK 到本地
        local_apk = 'temp_app.apk'
        print(f"正在拉取 APK 到本地...")
        subprocess.run(
            ['adb', 'pull', apk_path, local_apk],
            capture_output=True
        )
        
        if not os.path.exists(local_apk):
            print("错误: APK 拉取失败")
            return None
        
        # 3. 使用 aapt 解析 APK
        print("正在解析 APK...")
        result = subprocess.run(
            ['aapt', 'dump', 'badging', local_apk],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='ignore'  # 忽略编码错误
        )
        
        # 4. 提取应用名称
        output = result.stdout
        
        # 查找 application-label 或 application-label-zh-CN
        patterns = [
            r"application-label-zh-CN:'([^']+)'",  # 中文标签
            r"application-label-zh:'([^']+)'",      # 中文标签
            r"application-label:'([^']+)'",         # 默认标签
        ]
        
        app_name = None
        for pattern in patterns:
            match = re.search(pattern, output)
            if match:
                app_name = match.group(1)
                break
        
        # 5. 清理临时文件
        if os.path.exists(local_apk):
            os.remove(local_apk)
            print("临时文件已清理")
        
        if app_name:
            print(f"\n应用名称: {app_name}")
            return app_name
        else:
            print("错误: 未能提取应用名称")
            return None
            
    except FileNotFoundError as e:
        print(f"错误: 未找到命令 (adb 或 aapt)，请确保它们在系统 PATH 中")
        return None
    except Exception as e:
        print(f"发生错误: {str(e)}")
        return None


def main():
    """主函数"""
    # 设置控制台编码为 UTF-8 (Windows)
    if sys.platform == 'win32':
        os.system('chcp 65001 > nul')
    
    # 示例使用
    package_name = 'com.ss.android.article.news'
    
    if len(sys.argv) > 1:
        package_name = sys.argv[1]
    
    print(f"=" * 50)
    print(f"开始获取应用名称")
    print(f"包名: {package_name}")
    print(f"=" * 50)
    
    app_name = get_app_name_from_package(package_name)
    
    if app_name:
        print(f"\n✓ 成功获取应用名称: {app_name}")
    else:
        print(f"\n✗ 获取应用名称失败")


if __name__ == '__main__':
    main()