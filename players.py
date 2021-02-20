from bs4 import BeautifulSoup as bs
import pandas as pd
import random
from selenium import webdriver
import constants

from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.proxy import Proxy, ProxyType

constants.__init__()


class player_stats(object):
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

    def get_link(self, link):
        self.driver.get(link)
        sleep(random.randint(2, 4))

    def accept(self):
        button = self.driver.find_element_by_xpath('//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]')
        self.driver.execute_script("arguments[0].click();", button)
        #WebDriverWait(self.driver, random.randint(3, 5)).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]'))).click()

    def get_soup(self):
       # WebDriverWait(self.driver, random.randint(3, 10)).until(
        #    EC.element_to_be_clickable((By.CSS_SELECTOR, '#sub-sub-navigation > ul > li:nth-child(2) > a'))).click()
        #sleep(random.randint(3, 5))
        content = self.driver.page_source
        soup = bs(content, features='lxml')
        return soup

    def team(self, location, soup):
        if location == 'home':
            return soup.findAll('a', {'class': 'team-link'})[0].text
        else:
            return soup.findAll('a', {'class': 'team-link'})[1].text

    def table(self, location, soup, link):

        sleep(3)
        df = pd.DataFrame()
        if location == 'home':
            table = \
            soup.findAll("table", {'id': 'top-player-stats-summary-grid', 'class': 'grid with-centered-columns hover'})[
                0]
        else:
            table = \
            soup.findAll("table", {'id': 'top-player-stats-summary-grid', 'class': 'grid with-centered-columns hover'})[
                1]

        lis = []
        for td in table.findAll('td', {'class': 'col12-lg-2 col12-m-3 col12-s-4 col12-xs-5 grid-abs overflow-text'}):
            lis.append(td.findAll('a'))

        number = []
        position = []
        span = table.findAll('span', {'class': 'player-meta-data'})
        something = [i for i in range(0, len(span)) if i % 2 != 0]
        something_lis = []

        for i in range(0, len(something)):
            if i % 2 == 0:
                something_lis.append(something[i])

        for i in range(0, (len(span))):
            if i % 2 == 0 and len(span[i].text) <= 4:
                number.append(span[i].text)
            elif len(span[i].text) >= 6 and i in something_lis:
                position.append(span[i].text)

        df['player_name'] = [a[0].text for a in lis]
        df['game_id'] = [link for i in df['player_name']]
        df['field'] = location
        df['team'] = [self.team(i, soup) for i in df.field]
        df['position'] = [i for i in position]
        df['ShotsTotal'] = [i.text[0] for i in table.findAll('td', {'class': 'ShotsTotal'})]
        df['ShotOnTarget'] = [i.text[0] for i in table.findAll('td', {'class': 'ShotOnTarget'})]
        df['KeyPassTotal'] = [i.text[0] for i in table.findAll('td', {'class': 'KeyPassTotal'})]
        df['PassSuccessInMatch'] = [int(i.text[0]) / 10 for i in table.findAll('td', {'class': 'PassSuccessInMatch'})]
        df['DuelAerialWon'] = [i.text[0] for i in table.findAll('td', {'class': 'DuelAerialWon'})]
        df['Touches'] = [i.text[0] for i in table.findAll('td', {'class': 'Touches'})]
        df['rating'] = [i.text[0] for i in table.findAll('td', {'class': 'rating'})]
        self.driver.quit()
        return df