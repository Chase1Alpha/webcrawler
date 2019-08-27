# -*- coding:utf-8 -*-

from selenium import webdriver
import time
import js2py

import urllib
import urllib2
from bs4 import BeautifulSoup

from HTMLParser import HTMLParser

import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )


def main():

# ******************  selenium Operations ***********************
    driver = webdriver.Chrome()
    driver.get("http://www.rufa.gov.cn/fxweb/subpage/legalpublicity/fx_regulations.html?objId=1136428890002169856")

    def get_contents():
        result_raw = driver.page_source
        result_soup = BeautifulSoup(result_raw, 'html.parser')

        result_bf = result_soup.prettify()

        # ****************   Store raw data file   *****************************************
        with open("./output/fkrawfile/raw_result.txt", 'a') as fks:
            fks.write(result_bf)
        fks.close()
        print "Store raw data successfully!!!"

        # ****************   Find all nodes that we want   *****************************************
        with open("./output/fkrawfile/noscript_meta.txt", 'a') as noscript_meta:
            noscript_nodes = result_soup.find_all('pre', attrs={'class': 'regulationContent'})
            noscript_inner_all = ""
            for noscript in noscript_nodes:
                noscript_inner = noscript.get_text('\n')
                noscript_inner_all += noscript_inner + "\n"

            h = HTMLParser()
            noscript_all = h.unescape(noscript_inner_all)
            noscript_meta.write(noscript_all)

        noscript_meta.close()
        print "Store noscript meta data successfully!!!"

# ****************** Scroll to the bottom, and do it 10 times *********
    def execute_times(times):

        for i in range(times + 1):
            get_contents()
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
            try:
                if i == 7:
                    with open("./dlfz.js", 'r') as js:
                        js2py.eval_js(js)
                        driver.find_element_by_css_selector('a.next').click()
                        print "page" + str(i)
                        time.sleep(1)
                else:
                    driver.find_element_by_css_selector('a.next').click()
                    print "page" + str(i)
                    time.sleep(1)
            except:
                break

    execute_times(47)


if __name__ == "__main__":

    main()

