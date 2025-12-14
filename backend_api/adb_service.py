import subprocess
import os
import re
from typing import List, Dict, Optional
from logger import logger


class ADBAppManager:
    """管理通过 ADB 获取 Android 应用信息的类"""
    
    TEMP_APK_FILE = 'temp_app.apk'
    
    @staticmethod
    def _run_adb_command(command: List[str], check: bool = True) -> subprocess.CompletedProcess:
        try:
            return subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore',
                check=check
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"ADB 命令执行失败: {' '.join(command)}\n错误: {e}")
            raise
        except FileNotFoundError:
            logger.error("错误: 未找到 adb 命令，请确保 Android SDK 已安装并在 PATH 中")
            raise
    
    @staticmethod
    def get_third_party_packages() -> List[str]:
        try:
            result = ADBAppManager._run_adb_command(
                ['adb', 'shell', 'pm', 'list', 'packages', '-3']
            )
            
            packages = [
                line.replace('package:', '').strip()
                for line in result.stdout.strip().split('\n')
                if line.startswith('package:')
            ]
            
            return packages
        
        except Exception as e:
            logger.error(f"获取第三方包列表失败: {e}")
            return []
    
    @staticmethod
    def _get_apk_path(package_name: str) -> Optional[str]:
        result = ADBAppManager._run_adb_command(
            ['adb', 'shell', 'pm', 'path', package_name],
            check=False
        )
        
        if result.returncode != 0:
            logger.error(f"错误: 未找到包 {package_name}")
            return None
        
        apk_path = result.stdout.strip()
        if apk_path.startswith('package:'):
            apk_path = apk_path[8:]
        
        return apk_path
    
    @staticmethod
    def _pull_apk(apk_path: str, local_path: str) -> bool:
        try:
            ADBAppManager._run_adb_command(
                ['adb', 'pull', apk_path, local_path],
                check=False
            )
            return os.path.exists(local_path)
        except Exception as e:
            logger.error(f"拉取 APK 失败: {e}")
            return False
    
    @staticmethod
    def _extract_app_name_from_apk(apk_path: str) -> Optional[str]:
        try:
            result = subprocess.run(
                ['aapt', 'dump', 'badging', apk_path],
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='ignore'
            )
            
            # 按优先级查找应用名称标签
            patterns = [
                r"application-label-zh-CN:'([^']+)'",
                r"application-label-zh:'([^']+)'",
                r"application-label:'([^']+)'",
            ]
            
            for pattern in patterns:
                match = re.search(pattern, result.stdout)
                if match:
                    return match.group(1)
            
            return None
            
        except FileNotFoundError:
            logger.error("错误: 未找到 aapt 命令，请确保 Android SDK Build-tools 已安装")
            return None
        except Exception as e:
            logger.error(f"解析 APK 失败: {e}")
            return None
    
    @staticmethod
    def get_app_name(package_name: str, verbose: bool = False) -> Optional[str]:
        try:
            if verbose:
                logger.info(f"正在查找包 {package_name} 的路径...")
            
            # 1. 获取 APK 路径
            apk_path = ADBAppManager._get_apk_path(package_name)
            if not apk_path:
                return None
            
            if verbose:
                logger.info(f"找到 APK 路径: {apk_path}")
                logger.info("正在拉取 APK 到本地...")
            
            # 2. 拉取 APK 到本地
            if not ADBAppManager._pull_apk(apk_path, ADBAppManager.TEMP_APK_FILE):
                logger.error("错误: APK 拉取失败")
                return None
            
            if verbose:
                logger.info("正在解析 APK...")
            
            # 3. 解析 APK 获取应用名称
            app_name = ADBAppManager._extract_app_name_from_apk(ADBAppManager.TEMP_APK_FILE)
            
            # 4. 清理临时文件
            if os.path.exists(ADBAppManager.TEMP_APK_FILE):
                os.remove(ADBAppManager.TEMP_APK_FILE)
                if verbose:
                    logger.info("临时文件已清理")
            
            if app_name and verbose:
                logger.info(f"\n应用名称: {app_name}")
            elif not app_name:
                logger.error("错误: 未能提取应用名称")
            
            return app_name
            
        except Exception as e:
            logger.error(f"获取应用名称时发生错误: {e}")
            # 确保清理临时文件
            if os.path.exists(ADBAppManager.TEMP_APK_FILE):
                os.remove(ADBAppManager.TEMP_APK_FILE)
            return None
    
    @staticmethod
    def get_all_third_party_apps(verbose: bool = False) -> List[Dict[str, str]]:
        packages = ADBAppManager.get_third_party_packages()
        
        if not packages:
            logger.warning("未找到第三方应用")
            return []
        
        if verbose:
            logger.info(f"\n找到 {len(packages)} 个第三方应用，开始获取应用名称...\n")
        
        apps = []
        for i, package in enumerate(packages, 1):
            if verbose:
                logger.info(f"[{i}/{len(packages)}] 处理: {package}")
            
            app_name = ADBAppManager.get_app_name(package, verbose=False)
            
            apps.append({
                'package_name': package,
                'app_name': app_name if app_name else '未知'
            })
            
            if verbose:
                logger.info(f"  -> {app_name if app_name else '未知'}\n")
        
        return apps
    
    @staticmethod
    def connect_device():
        try:
            result = ADBAppManager._run_adb_command(
                ['adb', 'devices'],
                check=False
            )
            
            if result.returncode != 0:
                logger.error("ADB 命令执行失败")
                return False
            
            # 解析输出,查找连接的设备
            lines = result.stdout.strip().split('\n')
            logger.info(f"adb devices 输出:\n{result.stdout}")
            
            # 跳过第一行 "List of devices attached"
            devices = [line for line in lines[1:] if line.strip()]
            
            if devices:
                logger.info(f"检测到 {len(devices)} 个设备已连接")
                return True
            else:
                logger.warning("未检测到已连接的设备")
                return False
                
        except FileNotFoundError:
            logger.error("错误: 未找到 adb 命令,请确保 Android SDK 已安装并在 PATH 中")
            return False
        except Exception as e:
            logger.error(f"检查设备连接时发生错误: {e}")
            return False

# if __name__ == '__main__':
#     # 方式1: 获取所有第三方应用（推荐）
#     print("=" * 50)
#     print("获取所有第三方应用信息")
#     print("=" * 50)
#     apps = ADBAppManager.get_all_third_party_apps(verbose=True)
    
#     print("\n" + "=" * 50)
#     print("结果汇总:")
#     print("=" * 50)
#     for app in apps:
#         print(f"包名: {app['package_name']}")
#         print(f"应用名: {app['app_name']}")
#         print("-" * 50)
    
#     # 方式2: 仅获取包名列表
#     # packages = ADBAppManager.get_third_party_packages()
#     # print(f"第三方应用包名: {packages}")
    
#     # 方式3: 获取单个应用名称
#     # app_name = ADBAppManager.get_app_name('com.example.app', verbose=True)
#     # print(f"应用名称: {app_name}")