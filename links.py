from bs4 import BeautifulSoup as bs
import random
from selenium import webdriver
import constants

from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType

constants.__init__()

class links(object):
    def __init__(self):
        self.chromedriver_path = str(constants.DRIVER_PATH)
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--incognito")
        self.prox = Proxy()
        self.prox.proxy_type = ProxyType.MANUAL
        self.prox.socks5_proxy = constants.PROXY['https']
        self.capabilities = webdriver.DesiredCapabilities.CHROME
        self.prox.add_to_capabilities(self.capabilities)
        self.driver = webdriver.Chrome(executable_path=self.chromedriver_path, options=self.chrome_options,desired_capabilities=self.capabilities )
        self.main = constants.LINK
        #self.driver = webdriver.Safari()
        self.league = []
        self.game_links = []
        self.pst_links = []

    def getLeagues(self):
        self.driver.get(self.main)
        content = self.driver.page_source
        soup = bs(content, features='lxml')
        links = soup.findAll("li", {'class': 'hover-target'})
        for i in range(0, len(links)):
            self.league.append(self.main + links[i].find("a")['href'])
        return self.league

    def getIn(self, url):
        self.driver.get(url)
        sleep(random.randint(2, 3))

    def accept(self):
        WebDriverWait(self.driver, random.randint(3,10)).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'))).click()

    def table(self):
        content = self.driver.page_source
        soup = bs(content, features='lxml')
        table = soup.find("div", {'id': 'tournament-fixture',
                                  'class': 'col12-lg-12 col12-m-12 col12-s-12 col12-xs-12 divtable'})
        return table

    def linkgetter(self):
        for j in range(2,4):
            table = self.table()
            for i in range(0,1):
                for k in table.findAll('a',{'class':'stacked-match-link result-1'}):
                    try:
                        self.game_links.append(self.main+ k['href'])
                        print(self.main+k['href'])
                    except:
                        continue
                self.driver.find_element_by_xpath('//*[@id="date-controller"]/a[1]').click()
                sleep(3)
                table = self.table()
                sleep(3)
            self.driver.find_element_by_xpath('//*[@id="seasons"]/option[{}]'.format(j)).click()
        self.driver.quit()
        return self.game_links



