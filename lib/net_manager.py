#! encoding:utf-8

import nmap 
_up_host=dict()
def up_host_scan(local_ip):
    """ 
    存活主机发现，
    参数是local_ip，将给定ip经过处理，检测该网段下所有ip
    运行结果返回一个列表，样例：{'192.168.100.1': 'up', '192.168.100.103': 'up', '192.168.100.106': 'up', '192.168.100.105': 'up'} 
    """
    local_ip=''.join(i+'.' for i in ip_parse(local_ip)[0:3])
    global _up_host
    nm=nmap.PortScanner()
    nm.scan(hosts='{}0/24'.format(local_ip),arguments='-sn -PE')
    hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
    for host, status in hosts_list:
        if status=='up':
            _up_host[host]=status
        else :
            pass
    return _up_host

def ip_parse(ip):
    """ 
    ip解析，将ip分解成四部分，然后全部填入列表
    返回一个ip解析列表
    """
    return [i for i in ip.split(".")]

if __name__ == "__main__":
    listt=up_host_scan('192.168.100.1')
    print listt