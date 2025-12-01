import argparse
from stop_and_run_uiautomator import rerun_uiautomator2
from run_config import (
    get_config_settings, 
    get_OS_type, 
    clear_app_cache, 
    execute_cmd_with_timeout
)


def main():
    parser = argparse.ArgumentParser(description="Single App Engine Runner")
    parser.add_argument("--pkg", required=True)
    parser.add_argument("--app", required=True)
    parser.add_argument("--config", default="config.ini")
    parser.add_argument("--task_id", required=True)

    args = parser.parse_args()

    config_settings = get_config_settings(args.config)
    os_type = get_OS_type()

    pkgName = args.pkg
    appName = args.app

    print(f'{pkgName}, {appName}')

    print(f"[ENGINE] Start processing {pkgName} | {appName}")

    try:
        if config_settings['clear_cache'] == 'true':
            clear_app_cache(pkgName)

        # 重启 uiautoamtor2
        if config_settings['rerun_uiautomator2'] == 'true':
            rerun_uiautomator2()

        timeout = int(config_settings['dynamic_run_time']) + 120

        # 给 run_task.py 写入配置
        with open("run_config_task.txt", "w", encoding="utf8") as f:
            f.write(
                f"{pkgName},{appName},"
                f"{config_settings['dynamic_ui_depth']},"
                f"{config_settings['dynamic_run_time']},"
                f"{config_settings['searchprivacypolicy']},"
                f"{config_settings['screenuidrep']},"
                f"{args.task_id}"
            )

        # 执行 run_task.py
        if os_type == "win":
            execute_cmd_with_timeout("python run_task.py", timeout)
        else:
            execute_cmd_with_timeout("python3 run_task.py", timeout)

    except Exception as e:
        print(f"[ENGINE] ERROR: {e}")

    finally:
        execute_cmd_with_timeout(f"adb shell am force-stop {pkgName}")
        print(f"[ENGINE] Completed {pkgName}")


if __name__ == "__main__":
    main()
    '''
    python poker_engine.py --pkg com.xxx --app "名字" --task_id 任务ID
    '''
