'''
Created on Aug 10, 2017
Get the contents from elastic for an Exchange Instance
Useful for testing

'''
import os
import sys
import time
import json
from urlparse import urljoin
from selenium import webdriver
from logins import BexLogins

HOST = 'https://exchange-qa.boundlessgeo.io/'
USR = 'test' 
PWD = 'QATESTING!'
OUTPUT_LOG_PATH = None


class ReadElastic():
    ''' 
    Class created for reading elastic contents, enabeling a log to be created
    reporting the number of items contained in Registry and Exchange
    This is to help monitor reports of content not showing up and 
    for general debug/troubleshooting
    
    Currently only working properly with the safari web driver
    '''
    def __init__(self, host, usr, pwd, output_log_path):
        '''
        ReadElastic(host, usr, pwd, output_log_path)
        Create the web driver and login
        
        Uses logins class for authenticating to various BEX instances
        '''
        self.host = host
        self.usr = usr
        self.pwd = pwd

        if output_log_path:
            self.outPath = output_log_path
        else:
            self.outPath = os.path.join(
                os.path.dirname(sys.argv[0]), 'BEX_content_report.log') 
        
        self.searchurl = r'/api/base/search/?limit=100&offset=0'
        self.url = urljoin(self.host, self.searchurl)
        print self.url 
        
        self.data = {}
        
        self.browser = webdriver.Safari()
        self.browser.implicitly_wait(5)
        logins = BexLogins(self.browser)
        
        logins.login_with_usr_pwd(self.url, self.usr, self.pwd)
        time.sleep(3)

    def getContents(self):
        '''
        getContents()
        getContents from base api as json and
        load into dictionary 
        '''
        text_contents = self.browser.find_element_by_tag_name('body').text
        print text_contents
        _json = json.loads(text_contents)
        print _json
        
        self.data['total_count'] = _json['meta']['total_count']
        self.data['reg_count'] = _json['meta']['facets']['_index']['registry']    
        self.data['ex_count'] = _json['meta']['facets']['_index']['exchange']
        self.data['alltypes'] = _json['meta']['facets']['alltypes']
        return     
    
    def writeLog(self):
        '''
        writeLog()
        write contents in dict from elastic to 
        a file for logging
        '''
        
        with open(self.outPath, 'ab') as f:
            f.write('*' * 10)
            f.write('\n')
            f.write(time.asctime())
            f.write('\n\n')
            f.write('Total count    = ' + str(self.data['total_count']) + '\n')
            f.write('Registry count = ' + str(self.data['reg_count']) + '\n')
            f.write('Exchange count = ' + str(self.data['ex_count']) + '\n' + '\n')
            f.write('Details:\n')
            for item in self.data['alltypes'].iteritems():
                f.write(str(item[1]))
                f.write('\tof type ' + item[0] + '\n')
            
            f.write('*' * 10)
        return
        
    
    def __del__(self):
        ''' close browser on object delete ''' 
        self.browser.close()
        try:
            self.browser.quit()
        except:
            pass #hide selenium message when trying to quit
            
if __name__ == '__main__':
    ContentReport = ReadElastic(HOST, USR, PWD, OUTPUT_LOG_PATH)
    ContentReport.getContents()
    ContentReport.writeLog()
    