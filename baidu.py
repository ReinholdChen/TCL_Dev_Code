from selenium import webdriver
import time


driver = webdriver.Chrome()
driver.get('https://www.baidu.com')

print(driver.title)

driver.quit()