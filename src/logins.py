'''
Created on May 22, 2017
Handles different logins to Exchange Instances
'''
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#EXCHANGE_DASH_DEV_BOUNDLESSPS_URL = r'exchange-dev.boundlessps.com/account/login/?next=/'
DEV_EXCHANGE_BOUNDLESSPS_URL = r'https://dev.exchange.boundlessps.com/account/login/?next=/'
EXCHANGE_GEOINTSERVICES_IO_URL = r'https://exchange.geointservices.io/account/login/?next=/'
EXCHANGE_GVSLABS_URL = r'https://exchange.gvslabs.com'
#EXCHANGEDEV_GVSLABS_URL = r'https://exchangedev.gvslabs.com'
#EXCHANGE_BOUNDLESSGEO_IO = r'https://exchange.boundlessgeo.io/account/login/?next=/'

class BexLogins(object):
    '''
    class to manage all the BEX sites and logins
    '''
    def __init__(self, browser):
        '''
        BexLogins(seleniumDriverObj)
        '''
        self.browser = browser
        self.usr = None
        self.pwd = None
        self.usr_element = None
        self.pwd_element = None
        self.btn_element = None
        self.profile = None
    
    
    def login_dev_dot_exchange_boundlessps_usingConnect(self, user=None, pwd=None):
        '''
        login_dev_dot_exchange_boundlessps_usingConnect(user=None, pwd=None)
        Login to https://dev.exchange.boundlessps.com/account/login/?next=/
        via connect credentials 
        Cache needs to be cleared to run multiple tests
        '''
        self.usr = user
        self.pwd = pwd
        self.browser.get(DEV_EXCHANGE_BOUNDLESSPS_URL)
        btn = self.browser.find_element_by_css_selector('a.btn-auth0')
        btn.click()
        WebDriverWait(self.browser, 10).until(
            EC.title_contains('Sign In'))
        
        self.browser.implicitly_wait(10)
        self.usr_element = self.browser.find_element_by_id('a0-signin_easy_email')
        self.usr_element.send_keys(self.usr)
        
        self.pwd_element = self.browser.find_element_by_id('a0-signin_easy_password')
        self.pwd_element.send_keys(self.pwd)
        
        self.btn_element = self.browser.find_element_by_css_selector('button.a0-primary')
        self.btn_element.click()
        return
    
    def login_dev_dot_exchange_boundlessps(self, user='usr', pwd='pwd'):
        '''
        login_dev_dot_exchange_boundlessps(self, user=None, pwd=None)
        Log into https://dev.exchange.boundlessps.com
        '''
        
        self.usr = user
        self.pwd = pwd
        
        self.browser.get(DEV_EXCHANGE_BOUNDLESSPS_URL)
        WebDriverWait(self.browser, 10).until(
            EC.title_contains('Exchange'))
        
        self.usr_element = self.browser.find_element_by_id('id_username')
        self.usr_element.send_keys(self.usr)
        
        self.pwd_element = self.browser.find_element_by_id('id_password')
        self.pwd_element.send_keys(self.pwd)
        
        self.btn_element = self.browser.find_element_by_css_selector('button.btn')
        self.btn_element.click()
        return
    
    def login_with_usr_pwd(self, url=None, user='usr', pwd='pwd'):
        '''
        login_with_usr_pwd(self, url=None, user=user, pwd=pwd):
        
        Generic login using username and password
        '''
  
        self.usr = user
        self.pwd = pwd       
        self.browser.get(url)
        
        WebDriverWait(self.browser, 10).until(
            EC.title_contains('Exchange'))
        
        self.usr_element = self.browser.find_element_by_id('id_username')
        self.usr_element.send_keys(self.usr)
        
        self.pwd_element = self.browser.find_element_by_id('id_password')
        self.pwd_element.send_keys(self.pwd)
        
        self.btn_element = self.browser.find_element_by_css_selector('button.btn')
        self.btn_element.click()
        return
    
    def login_exchange_dot_gvslabs(self, ffprofile):
        '''
        login_exchange_dot_gvslabs()
        login for https://exchange.gvslabs.com
        requires issued certificate from GVS
        uses ffprofile with cert added, profile config has one cert, and auto picks it
        so login happens without a specific action
        '''
        
        self.profile = ffprofile
        
        self.browser.get(EXCHANGE_GVSLABS_URL)
        
        self.assertIn('Welcome! - GEOINT Exchange', self.browser.title)   
        WebDriverWait(self.browser, 10).until(
            EC.title_contains("Welcome! - GEOINT Exchange"))
        
if __name__ == '__main__':
    # Example usage    

    profile = webdriver.FirefoxProfile()
    profile.set_preference("browser.cache.disk.enable", False)
    profile.set_preference("browser.cache.memory.enable", False)
    profile.set_preference("browser.cache.offline.enable", False)
    profile.set_preference("network.http.use-cache", False)
    
    browser = webdriver.Firefox()   
    LogIns = BexLogins(browser)
    LogIns.login_dev_dot_exchange_boundlessps(user='admin', pwd='exchange')
    
    time.sleep(10)
    print 'browser will close in 10 seconds'
    browser.close()
        