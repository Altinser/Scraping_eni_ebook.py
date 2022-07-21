
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from fpdf import FPDF
import pdfkit

profile = webdriver.FirefoxProfile()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", "D:\ebook\Systeme_et_reseau")
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
profile.set_preference("pdfjs.disabled", True)

driver = webdriver.Firefox(firefox_profile=profile,executable_path=r'C:\Program Files (x86)\geckodriver.exe')

driver.get('https://cas.uphf.fr/cas/login?service=https://portail.uphf.fr/uPortal/Login')


try:
    page_login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login")))
    page_login.find_element_by_id("username").send_keys("")
    page_login.find_element_by_id("password").send_keys("")
    page_login.find_element_by_name("submit").click()

    driver.get('https://portail.uphf.fr/uPortal/p/scd-BeL.ctf3/max/render.uP')
    time.sleep(3)
    driver.find_element_by_xpath('//*[@id="portletContent_ctf3"]/div/form/table/tbody/tr[8]/td[2]/button').click()
    time.sleep(3)
    window_after = driver.window_handles[0]
    driver.switch_to.window(window_after)
    driver.find_element_by_xpath('//*[@id="portletContent_ctf3"]/div/table[2]/tbody/tr[3]/td[2]/li/strong/a').click()
    time.sleep(5)
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)
    driver.find_element_by_xpath('/html/body/app-root/app-home/div/div[2]/div[2]/div[1]/app-categories/div/div/div[1]').click()
    time.sleep(3)
    window_after = driver.window_handles[1]
    driver.switch_to.window(window_after)

    premiere_page = True

    nb_page = 1
    while nb_page!= 17:
        if premiere_page:
            premiere_page = False
        else:
            driver.find_element_by_xpath('//*[@id="main-content"]/app-content/div/div[1]/div[1]/div[2]/app-paging/pagination/ul/li[9]/a').click()

        for j in range(1,16):
            window_after = driver.window_handles[1]
            driver.switch_to.window(window_after)
            driver.find_element_by_xpath('//*[@id="main-content"]/app-content/div/div[1]/div[1]/div[1]/div/div['+str(j)+']').click()
            time.sleep(3)

            cpt = 0
            premiere_page_livre = True
            while(driver.find_element_by_xpath('//*[@id="main-content"]/div/app-content/div/div/app-book-page/div/div/div[1]/div[2]/app-previous-next/div/span').is_enabled()):
                window_after = driver.window_handles[1]
                driver.switch_to.window(window_after)
                time.sleep(1)
                if premiere_page_livre:
                    titre = driver.find_element_by_xpath('//*[@id="content-presentation"]/h1')
                    titre = titre.text
                    os.mkdir('D:\\ebook\\Systeme_et_reseau\\'+titre)
                    time.sleep(2)
                    driver.profile.set_preference("browser.download.dir", 'D:\\ebook\\Systeme_et_reseau\\'+titre+'\\')
                    premiere_page_livre = False
                driver.find_element_by_xpath('//*[@id="main-content"]/div/app-tools/div[2]/span').click()
                time.sleep(2)
                driver.find_element_by_xpath('//*[@id="main-content"]/div/app-content/div/div/app-book-page/div/div/div[1]/div[2]/app-previous-next/div/span').click()
                time.sleep(2)
                cpt = cpt+1

            for i in range(0,cpt):
                driver.back()
        nb_page = nb_page+1

    time.sleep(10)
finally:
    driver.quit()
