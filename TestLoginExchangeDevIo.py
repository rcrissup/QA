'''
Test for logging into exchange
'''
from selenium import webdriver
from selenium.webdriver.firefox.webdriver import FirefoxProfile
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import os
import unittest

URL = r'https://exchange-dev.boundlessgeo.io/account/login/?next=/'
EMAIL = '<enter email>'
PWD = '<enter password>'

class TestLogInExchangeDevIo(unittest.TestCase):
    def setUp(self):
        '''
        '''
        self.browser = webdriver.Firefox()

    def test_log_in(self):
        '''
        '''
        self.browser.get(URL)
        
        connectButton = self.browser.find_element_by_class_name('btn-auth0')
        connectButton.click()
        
        self.browser.implicitly_wait(3)
        
        email = self.browser.find_element_by_id('a0-signin_easy_email')
        email.send_keys(EMAIL)
        
        pwd = self.browser.find_element_by_id('a0-signin_easy_password')
        pwd.send_keys(PWD)

        loginButton = self.browser.find_element_by_class_name('a0-primary')    
        loginButton.click()
            
        WebDriverWait(self.browser, 20).until(
            EC.title_contains('Welcome! - Boundless Exchange')
        )
        
        self.assertIn("Welcome! - Boundless Exchange", self.browser.title)
               

    def tearDown(self):
        self.browser.quit()

if __name__ == "__main__":
    unittest.main()