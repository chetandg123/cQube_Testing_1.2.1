






import csv
import os
import time

from selenium.webdriver.support.select import Select

from Data.parameters import Data
from get_dir import pwd
from reuse_func import GetData


class textbook_districtwise_lastday_records():
    def __init__(self,driver):
        self.driver = driver

    def test_each_districts(self):
        self.data = GetData()
        self.p = pwd()
        count = 0
        self.driver.find_element_by_xpath(Data.hyper_link).click()
        self.data.page_loading(self.driver)
        content = Select(self.driver.find_element_by_id('chosse_collection'))
        content.select_by_visible_text(' Textbook ')
        self.data.page_loading(self.driver)
        times = Select(self.driver.find_element_by_name('timePeriod'))
        times.select_by_visible_text(' Last Day ')
        time.sleep(2)
        districts  =Select(self.driver.find_element_by_id('choose_dist'))
        i = 0
        for x in range(1,len(districts.options)):
            time.sleep(1)
            districts.select_by_index(x)
            name = districts.options[x].text
            names = name.strip()
            self.data.page_loading(self.driver)
            if  "No data found" in self.driver.page_source:
                print(districts.options[x].text ," does not last day records")
            else:
                self.driver.find_element_by_id(Data.Download).click()
                time.sleep(3)
                self.filename = self.p.get_download_dir() + "/Diksha_"+names+"_Dist_Data_last_day.csv"
                file = os.path.isfile(self.filename)
                self.data.page_loading(self.driver)
                with open(self.filename) as fin:
                    csv_reader = csv.reader(fin, delimiter=',')
                    header = next(csv_reader)
                    data = list(csv_reader)
                    row_count = len(data)
                    print(row_count)
                os.remove(self.filename)
                tablecount = self.driver.find_elements_by_tag_name('tr')
                records = int(len(tablecount)) - 2
                time.sleep(2)
                if row_count!= records:
                    print(districts.options[x].text ,"records count mismatch in downloaded file and table records")
                    count = count + 1
                i = i + 1
        return count