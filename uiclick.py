# -*- encoding: utf-8 -*-
'''
Created on 2018年12月01日

@author: linhuajian
'''
import threading
import io
from appium import webdriver
import time
import datetime
import  demo
import serial
import subprocess
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '9'
desired_caps['deviceName'] = 'RFCMA04RH8L'
desired_caps['appPackage'] = 'com.tcl.superapp'
desired_caps['appActivity'] = 'com.tcl.tsmart.main.StartActivity'
# desired_caps['appPackage'] = 'com.tcl.tclhome'
# desired_caps['appActivity'] = 'com.tcl.tclhome.ui.activities.SplashActivity'
# desired_caps['appPackage']='com.huawei.android.launcher'

# 断电测试
def clickCzButton(port_log_path='',code_log_path=''):
    u''' 点击插座按钮  '''
    driver  =  webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)
    time.sleep(15)
    while True:
        #关闭开关
        time.sleep(1)
        try:
            driver.find_element_by_xpath("//android.view.ViewGroup[@index='0']/android.widget.ImageView[@index='3']").click()
        except:
            ss= "click open fail"
            with io.open(code_log_path,"a+",encoding='utf-8') as f:
                f.write(u'{}\n'.format(ss))
            print("定位开关失败")
            driver.quit()
            driver  =  webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)
        this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        ss= this_date+'OFF'
        with io.open(code_log_path,"a+",encoding='utf-8') as f:
            f.write(u'{}\n'.format(ss))
        print('断电')
        b=''
        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        time.sleep(40)
        for  i in range(90):
            try:
                b= driver.find_elements_by_name("离线")
            except:
                pass
            if b!=[] :
                break
            sx = x * 0.35
            sy = y * 0.45
            ex = 0
            ey = y * 0.75
            driver.swipe(sx, sy, ex, ey,1000)
            time.sleep(4) 
        if b!=[]:
            this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            ss= this_date+'offline___pass'
            with io.open(code_log_path,"a+",encoding='utf-8') as f:
                f.write(u'{}\n'.format(ss))
            print("空调离线了")
        elif b=='':
            this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            ss= this_date+' yichang___fail'
            with io.open(code_log_path,"a+",encoding='utf-8') as f:
                f.write(u'{}\n'.format(ss))
            print('异常了')
        else:
            this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            ss= this_date+' online___fail'
            with io.open(code_log_path,"a+",encoding='utf-8') as f:
                f.write(u'{}\n'.format(ss))
            print("空调在线")
            
            
            
        #打开开关
        driver.find_element_by_xpath("//android.view.ViewGroup[@index='0']/android.widget.ImageView[@index='3']").click()
        this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        ss= this_date+'on'
        with io.open(code_log_path,"a+",encoding='utf-8') as f:
            f.write(u'{}\n'.format(ss))
        print('开电')
        time.sleep(40)
        b=''
        for  i in range(190):
            try:
                b= driver.find_elements_by_name("离线")
            except:
                pass
            if b==[] :
                break
            driver.swipe(sx, sy, ex, ey,1000)
            time.sleep(4) 
        if b!=[]:
            this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            ss= this_date+'offline___fail'
            with io.open(code_log_path,"a+",encoding='utf-8') as f:
                f.write(u'{}\n'.format(ss))
            print("空调离线了")
        elif b=='':
            this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            ss= this_date+'yichang___fail'
            with io.open(code_log_path,"a+",encoding='utf-8') as f:
                f.write(u'{}\n'.format(ss))
            print('异常了')
        else:
            this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            ss= this_date+' online___pass'
            with io.open(code_log_path,"a+",encoding='utf-8') as f:
                f.write(u'{}\n'.format(ss))
            print("空调在线")
    try:
        driver.quit()
    except:
        pass
#被run()方法调用，没有用到
def clickTclHome():
    #Thome测试
    driver  =  webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)
    #driver.find_element_by_id("com.tcl.tclhome:id/dialog_ad_close").click()
    time.sleep(20)
    a=''
    try:
        a=driver.find_elements_by_name("OFFLine")
    except:
        pass
    try:   
        b= driver.find_elements_by_name("ON")
    except:
        pass
    try:   
        c= driver.find_elements_by_name("OFF")
    except:
        pass
    if a!=[]:
        this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        ss= this_date+'offline'
        with io.open('./log',"a+",encoding='utf-8') as f:
            f.write(u'{}\n'.format(ss))
        print("空调离线了")
    elif a=='':
        this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        ss= this_date+'yichang'
        with io.open('./log',"a+",encoding='utf-8') as f:
            f.write(u'{}\n'.format(ss))
        print("异常了")
    else:
        this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        ss= this_date+'online'
        with io.open('./log',"a+",encoding='utf-8') as f:
            f.write(u'{}\n'.format(ss))
        print("空调在线")
    time.sleep(3)
    try:
        driver.quit()
    except:
        pass
#没有用到
def run():
    clickTclHome()
    this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
    ss= this_date+'change net'
    with io.open('./log',"a+",encoding='utf-8') as f:
        f.write(u'{}\n'.format(ss))
    print("改变网络状态")
    demo.open_falogin()

#有网，判断在线
def clickSmartTY(code_log_path=''):
    #断网测试
    b=''
    driver  =  webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    time.sleep(20)
    for  i in range(390):
        try:
            b= driver.find_elements_by_name("离线")
        except:
            pass
        if b==[] :
            break
        sx = x * 0.35
        sy = y * 0.45
        ex = 0
        ey = y * 0.75
        #从（sx,sy）滑动到(ex,ey),滑动时间1s
        try:
            driver.swipe(sx, sy, ex, ey,1000)
        except:
            try:
                driver.quit()
            except:
                pass
            driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
        time.sleep(4) 
    if b!=[]:
        this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        ss= this_date+'offline___fail'
        with io.open(code_log_path,"a+",encoding='utf-8') as f:
            f.write(u'{}\n'.format(ss))
        print("空调离线了")
    elif b=='':
        this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        ss= this_date+'yichang___fail'
        with io.open(code_log_path,"a+",encoding='utf-8') as f:
            f.write(u'{}\n'.format(ss))
        print("异常了")
    #b=[]
    else:
        this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        ss= this_date+' online___pass'
        with io.open(code_log_path,"a+",encoding='utf-8') as f:
            f.write(u'{}\n'.format(ss))
        print("空调在线")
    time.sleep(1)
    try:
        driver.quit()
    except:
        pass
#断网，判断离线
def clickSmartTN(code_log_path=''):
    b=''
    driver  =  webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)
    x = driver.get_window_size()['width']
    y = driver.get_window_size()['height']
    time.sleep(20)
    for  i in range(390):
        try:
            b= driver.find_elements_by_name("离线")
        except:
            pass
        if b!=[] :
            break
        sx = x * 0.35
        sy = y * 0.45
        ex = 0
        ey = y * 0.75
        driver.swipe(sx, sy, ex, ey,1000)
        time.sleep(4) 
    if b!=[]:
        this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        ss= this_date+'offline___pass'
        with io.open(code_log_path,"a+",encoding='utf-8') as f:
            f.write(u'{}\n'.format(ss))
        print("空调离线了")
    elif b=='':
        this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        ss= this_date+'yichang___fail'
        with io.open(code_log_path,"a+",encoding='utf-8') as f:
            f.write(u'{}\n'.format(ss))
        print("异常了")
    else:
        this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        ss= this_date+'onlinie___fail'
        with io.open(code_log_path,"a+",encoding='utf-8') as f:
            f.write(u'{}\n'.format(ss))
        print("空调在线")
    time.sleep(1)
    try:
        driver.quit()
    except:
        pass

#断路由测试，未使用
def dly(port_log_path='',code_log_path=''):
    driver  =  webdriver.Remote('http://localhost:4723/wd/hub',desired_caps)
    time.sleep(15)
    while True:
        #关闭无线
        time.sleep(1)
        demo.open_falogin_OFF()
        this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        ss= this_date+'OFF  not net'    
        with io.open(code_log_path,"a+",encoding='utf-8') as f:
            f.write(u'{}\n'.format(ss))
        print("断路由")
        b=''
        x = driver.get_window_size()['width']
        y = driver.get_window_size()['height']
        time.sleep(40)
        for  i in range(190):
            try:
                b= driver.find_elements_by_name("离线")
            except:
                pass
            if b!=[] :
                break
            sx = x * 0.35
            sy = y * 0.45
            ex = 0
            ey = y * 0.75
            driver.swipe(sx, sy, ex, ey,1000)
            time.sleep(4) 
        if b!=[]:
            this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            ss= this_date+'offline___pass'
            with io.open(code_log_path,"a+",encoding='utf-8') as f:
                f.write(u'{}\n'.format(ss))
            print("空调离线了")
        elif b=='':
            this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            ss= this_date+'yichang___fail'
            with io.open(code_log_path,"a+",encoding='utf-8') as f:
                f.write(u'{}\n'.format(ss))
            print("异常了")
        else:
            this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            ss= this_date+'onlinie___fail'
            with io.open(code_log_path,"a+",encoding='utf-8') as f:
                f.write(u'{}\n'.format(ss))
            print("空调在线")
            
            
        #打开无线
        demo.open_falogin_OFF()
        this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        ss= this_date+'on  havenet'
        with io.open(code_log_path,"a+",encoding='utf-8') as f:
            f.write(u'{}\n'.format(ss))
        print("开无线")
        time.sleep(40)
        b=''
        for  i in range(190):
            try:
                b= driver.find_elements_by_name("离线")
            except:
                pass
            if b==[] :
                break
            driver.swipe(sx, sy, ex, ey,1000)
            time.sleep(4) 
        if b!=[]:
            this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            ss= this_date+'offline___fail'
            with io.open(code_log_path,"a+",encoding='utf-8') as f:
                f.write(u'{}\n'.format(ss))
            print("空调离线了")
        elif b=='':
            this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            ss= this_date+'yichang___fail'
            with io.open(code_log_path,"a+",encoding='utf-8') as f:
                f.write(u'{}\n'.format(ss))
            print("异常了")
        else:
            this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
            ss= this_date+'onlinie___pass'
            with io.open(code_log_path,"a+",encoding='utf-8') as f:
                f.write(u'{}\n'.format(ss))
            print("空调在线")
    try:
        driver.quit()
    except:
        pass
    
#获取设备串口日志
def getportlog(port_log_path):
    ser = serial.Serial('COM3', 115200, timeout=100)
    while True:
        date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
        ss= ser.readline().decode("ISO-8859-1")                
        ss=date+"---"+ss.lstrip()
        with io.open(port_log_path,"a+",encoding='utf-8') as f:
            f.write(u'{}'.format(ss))
            
#点击手机APP
def runST(code_log_path=''):
    #有网，判断在线
    clickSmartTY(code_log_path)
    this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
    ss= this_date+'Network unavailable'
    with io.open(code_log_path,"a+",encoding='utf-8') as f:
        f.write(u'{}\n'.format(ss))
    print("断网")
    demo.open_falogin()
    time.sleep(200)
    #断网，判断离线
    clickSmartTN(code_log_path)
    this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
    ss= this_date+'network avalible'
    with io.open(code_log_path,"a+",encoding='utf-8') as f:
        f.write(u'{}\n'.format(ss))
    print("打开网络")
    demo.open_falogin()
    time.sleep(200)
if __name__ == "__main__":
    this_date= datetime.datetime.today().strftime("%Y_%m_%d_%H_%M_%S")
    port_log_path="./"+this_date+'_port.log'
    code_log_path="./"+this_date+'code.log'
    adb_log_path="./"+this_date+'adb.log'
    threading.Thread(target=getportlog,args=(port_log_path,)).start()
    with open(adb_log_path, 'w') as f:
        order='adb logcat '
        poplog=subprocess.Popen(order, stdout=f)
    #断网测试循环500次
    for i in range(500):
        # 点击手机APP
        runST(code_log_path)
        time.sleep(10)
#断电测试
#clickCzButton(port_log_path,code_log_path)
#断路由器测试
    #dly(port_log_path,code_log_path)    
#     for i in range(500):
#         t=threading.Thread(target=runST,args=(code_log_path,))
#         t.start()
#         time.sleep(10)
        