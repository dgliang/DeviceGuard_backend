# producer.py
import json
import os
import subprocess
import threading
import time
from queue import Queue
from run_config import get_OS_type
from get_urls import get_pp_from_app_store, get_pkg_names_from_input_list


def producer_thread(queue, data):
    # 模拟保存数据到队列
    print("Adding data to queue:", data)
    time.sleep(2)  # 模拟保存操作耗时
    # 将数据放入队列中
    queue.put(data)


def consumer_thread(queue):
    processed_pp = set()

    while True:
        # 从队列中获取数据
        print('consumer thread waiting for data...')
        data = queue.get()
        print("Processing data:", data)
        # 缓冲5s，等待隐私政策URL被写入
        time.sleep(5)
        # 进行相应的处理操作
        pp_url_path, pkgName_appName = data.split('||')
        pkgName, appName = pkgName_appName.split('|')
        # 判断之前是否已经处理完成这个app的隐私政策，如果已经处理完成过，就没有必要继续重新处理
        if pkgName in processed_pp:
            print(f"{pkgName} has been processed before...")
            continue
        # 在这里进行其他处理操作
        app_pp = {}
        flag = True
        while flag:
            try:
                with open(pp_url_path, 'r', encoding='utf-8') as f:
                    content = f.readlines()
                    content = [item.strip('\n') for item in content]
                    print('content in txt file of PrivacyPolicy', content)
                    flag = False
            except FileNotFoundError:
                # 说明还没有写入文件系统
                time.sleep(5)
                print('try again.')

        pp_url = content
        print('pp_url:', pp_url)
        if len(pp_url) == 1:
            if 'html' in pp_url[0]:
                app_pp[pkgName] = [pp_url[0][:pp_url[0].index('html') + 4]][:]
            elif 'htm' in pp_url[0]:
                app_pp[pkgName] = [pp_url[0][:pp_url[0].index('htm') + 3]][:]
            else:
                if pp_url[0].endswith('.1.1'):
                    # 只有这一个结果，还是不合格的，视为没找到隐私政策
                    print('privacy policy not in ', pkgName)
                    pp_urls, missing_urls = get_pp_from_app_store(
                        get_pkg_names_from_input_list([pkgName]))
                    app_pp.update(pp_urls)
                else:
                    app_pp[pkgName] = pp_url[:]

        elif len(pp_url) > 1:
            app_pp[pkgName] = pp_url[:]
        # 将最终输出给隐私政策分析模块的文件修改为 包名:[应用名，[url列表]]的形式
        if type(app_pp[pkgName]) == list:
            app_pp[pkgName] = [appName, app_pp[pkgName][:]]
        else:
            app_pp[pkgName] = [appName, [app_pp[pkgName][:]]]

        with open(os.path.join('..', 'Privacy-compliance-detection-2.1', 'core', 'pkgName_url.json'), 'w',
                  encoding='utf-8') as f:
            json.dump(app_pp, f, indent=4, ensure_ascii=False)
        # 调用隐私政策处理模块
        os_type = get_OS_type()
        print('call pp analysis module in consumer_thread!')
        if os_type == 'win':
            subprocess.run(['python', 'privacy-policy-main.py','y'],
                           cwd=os.path.join('..', 'Privacy-compliance-detection-2.1', 'core'),
                           timeout=600)
        elif os_type in ['linux', 'mac']:
            subprocess.run(['python3', 'privacy-policy-main.py','y'],
                           cwd=os.path.join('..', 'Privacy-compliance-detection-2.1', 'core'),
                           timeout=600)
        print('call privacy-policy-main.py done.')
        files_in_privacy_policy_save_dir = os.listdir(
            os.path.join('..', 'Privacy-compliance-detection-2.1', 'core', 'PrivacyPolicySaveDir'))
        if pkgName + '.json' in files_in_privacy_policy_save_dir and pkgName + '_sdk.json' in files_in_privacy_policy_save_dir:
            with open('successful_analysis_pp.txt', 'a', encoding='utf-8') as f:
                f.write(pkgName + '\n')
            processed_pp.add(pkgName)
            print('pp analysis in consumer done.')

            # 继续使用大模型分析隐私政策文本
            # 不启用大模型

            # if f"{pkgName}.txt" in os.listdir(os.path.join('..', 'Privacy-compliance-detection-2.1', 'core', 'Privacypolicy_txt')):
            #     print('start try query llm...')
            #     if os_type == 'win':
            #         subprocess.run(['python', 'compliance_query.py', pkgName,'n'],
            #                        cwd=os.path.join('..', 'Privacy-compliance-detection-2.1', 'core'),
            #                        timeout=600)
            #         subprocess.run(['python', 'permission_query.py', pkgName,'n'],
            #                        cwd=os.path.join('..', 'Privacy-compliance-detection-2.1', 'core'),
            #                        timeout=600)
            #     elif os_type in ['linux', 'mac']:
            #         subprocess.run(['python3', 'compliance_query.py', pkgName,'n'],
            #                        cwd=os.path.join('..', 'Privacy-compliance-detection-2.1', 'core'),
            #                        timeout=600)
            #         subprocess.run(['python3', 'permission_query.py', pkgName,'n'],
            #                        cwd=os.path.join('..', 'Privacy-compliance-detection-2.1', 'core'),
            #                        timeout=600)
            #     files_in_permission_query_res_save_dir = os.listdir(os.path.join('..', 'Privacy-compliance-detection-2.1', 'core', 'permission_query_res_save_dir'))
            #     files_in_compliance_query_res_save_dir = os.listdir(os.path.join('..', 'Privacy-compliance-detection-2.1', 'core', 'compliance_query_res_save_dir'))
            #     if pkgName + '_compliance_query_result.json' in files_in_compliance_query_res_save_dir:
            #         print(f'{pkgName} compliance query done.')
            #         with open('successful_query_compliance.txt', 'a', encoding='utf-8') as f:
            #             f.write(pkgName + '\n')
            #     if pkgName + '_permission_query_result.json' in files_in_permission_query_res_save_dir:
            #         print(f'{pkgName} permission query done.')
            #         with open('successful_query_permission.txt', 'a', encoding='utf-8') as f:
            #             f.write(pkgName + '\n')



def main_thread():
    # 创建一个阻塞队列
    queue = Queue()

    # 创建守护线程
    consumer = threading.Thread(target=consumer_thread, args=(queue,))
    consumer.daemon = True
    consumer.start()

    # 在主线程中调用生产者方法
    producer_thread(queue, "Hello, world!")


if __name__ == '__main__':
    main_thread()
