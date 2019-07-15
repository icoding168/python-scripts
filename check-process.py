from datetime import datetime

import psutil
import requests
import json
import sys
from apscheduler.schedulers.blocking import BlockingScheduler
import daemon


def convert(s):
    str1 = " "
    return (str1.join(s))


def check_process(process_name,cmd):
    for proc in psutil.process_iter():
        try:
            if process_name.lower() == proc.name().lower():
                if cmd == '':
                    return True
                else:
                    cmdline = convert(proc.cmdline())
                    if cmd.lower() == cmdline.lower():
                        return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;


def handle_check(process_name,cmd):
    if check_process(process_name, cmd):
        print('该进程正在运行中')
    else:
        print('该进程没有运行')

        content = '该进程没有正常运行：' + process_name

        notification(content)


def notification(content):
    headers = {'content-type': 'application/json'}
    url = 'https://oapi.dingtalk.com/robot/send'

    data = {"msgtype": "text",
            "text": {
                "content": content
            }
            }

    params = {'access_token': 'b7bfe6e6e223605d9069162985caadb07040ff9f8f23fc1e924fb3c201083d69'}

    try:
        response = requests.post(url, params=params, data=json.dumps(data), headers=headers,timeout=10)
        print(response.content)
    except:
        print("调用钉钉机器人超时")

def handle_check_remote():
    notification('检测接口状态开始')

    url = 'http://182.61.33.241:8111/league/api/nim/consultant/find'
    try:
        
        requests.post(url, timeout=10)
    except:
        notification('该后台服务没有正常运行：' + url)

    url = 'http://woniujia.juke8.cn/league/api/nim/consultant/find'
    try:
        
        requests.post(url, timeout=10)
    except:
        notification('该后台服务没有正常运行：' + url)

    url = 'https://apis.juke8.cn/dsp/ex/weixin/user/login-by-code'
    try:
        
        requests.post(url, timeout=10)
    except:
        notification('该后台服务没有正常运行：' + url)

    url = 'http://www.juke8.cn:8086/admin/api/project-config/1.0/private/project/list/paging?page_size=10&page=1'
    try:
        
        requests.post(url, timeout=10)
    except:
        notification('该后台服务没有正常运行：' + url)

    url = 'http://dsp.juke8.cn/admin-console/#/projectConfig?p=god_bless_dsp'
    try:
        
        requests.post(url, timeout=10)
    except:
        notification('该后台服务没有正常运行：' + url)

    notification('检测接口状态结束')


def schedule():
    try:
        scheduler = BlockingScheduler()
        # scheduler.add_job(handle_check, 'interval', seconds=3,args=[process_name,cmd])
        scheduler.add_job(handle_check_remote, 'interval', seconds=10)
        scheduler.start()
    except Exception as e:
        print(str(e))

def main():
    process_name = 'testdfdfdf'
    cmd = ''
    try:
        process_name = sys.argv[1]

        length = sys.argv.__len__()

        if length >= 3:
            cmd = sys.argv[2]
    except:
        if not process_name:
            print("请输入进程名称")
            exit()

    print('service started.')

    # with daemon.DaemonContext():
    schedule()

if __name__ == '__main__':
    main()