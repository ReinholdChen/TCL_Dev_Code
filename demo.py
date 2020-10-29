#coding:utf-8
'''
Created on 2018年8月6日
@author: linhuajian
'''
import time
from selenium import webdriver
#from airtest.core.api import sleep
def open_falogin():
    u'''  开断网操作 ''' 
    driver = webdriver.Chrome("D:\chromedriver_win32\chromedriver_win32_new\chromedriver")
    url = "http://www.tendawifi.com/"
    #url = "http://tplogin.cn/"
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(20)
    driver.find_element_by_xpath('//*[@id="logInput"]').clear()
    driver.find_element_by_xpath('//*[@id="logInput"]').send_keys("test1234")
    #driver.find_element_by_xpath(' //*[@id="loginSub"]/i').click()
    driver.find_element_by_xpath('//*[@id="bntLogin"]').click()
    time.sleep(2)
    #点击行为管理
    #driver.find_element_by_xpath('//*[@id="headFunc"]/li[2]/span').click()
    driver.find_element_by_xpath('//*[@id="nav-list"]/li[6]/h3/a/label').click()
    #点击MAC地址过滤
    driver.find_element_by_xpath('//*[@id="behavior"]/li[2]/a').click()
    time.sleep(2)
    #点击开关
    driver.find_element_by_xpath('//*[@id="macTable"]/tbody/tr/td[6]/div/div/label').click()
    #driver.find_element_by_xpath('//*[@id="module-save"]').click()
    time.sleep(3)
    driver.close()
#没有用到
def open_falogin_OFF():
    u'''  开断路由器操作 ''' 
    driver = webdriver.Chrome("F:\Google\Chrome\Application\chromedriver.exe")
    url = "http://falogin.cn/"
    driver.get(url)
    driver.maximize_window()
    driver.implicitly_wait(20)
    driver.find_element_by_xpath('//*[@id="pcPassword"]').clear()
    driver.find_element_by_xpath('//*[@id="pcPassword"]').send_keys("test1234")
    driver.find_element_by_xpath('//*[@id="loginBtn"]').click()
    time.sleep(1)
    #点击高级设置
    driver.find_element_by_xpath('//*[@id="headFunc"]/li[2]/span').click()
    time.sleep(1)
    #点击无线设置
    driver.find_element_by_xpath('//*[@id="wifiSet_menu"]/label').click()
    time.sleep(1)
    #点击主人网络
    driver.find_element_by_xpath('//*[@id="wifiSet_menu0"]/label').click()
    time.sleep(1)
    #点击开关
    driver.find_element_by_xpath('//*[@id="switchCon"]/i[2]').click()
    time.sleep(1)
    driver.close()    

if __name__ == "__main__":
    open_falogin()
    #open_falogin_OFF()
    
    
    