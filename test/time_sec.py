#! encoding:utf-8

import time
def time_clock(timer):
    """ 计时器，
    参数timer单位为秒，一分钟是60，一小时是3600，一天是86400，使用该函数时建议以天为逻辑单位，避免闰月/大小月等情况
    时间到了返回True
     """
    first_time=time.time();
    secend_time=first_time+timer
    while True:
        time.sleep(5)
        if time.time()>=secend_time:
            return True
            break
        else:pass

if __name__ == "__main__":
    time_clock(120)