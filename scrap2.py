import json

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from fpdf import FPDF
import pdfkit
from PyPDF2 import PdfFileMerger
import shutil

UPHF_USERNAME = ""
UPHF_MDP = ""
DOWNLOAD_PATH = r"D:\Ebook"
GECKODRIVER_PATH = r"C:\geckodriver.exe"

if not os.path.isdir(DOWNLOAD_PATH):
    os.mkdir(DOWNLOAD_PATH)
    os.mkdir(DOWNLOAD_PATH + "\dl_dir")

if not os.path.isfile(DOWNLOAD_PATH + "\list.json"):
    with open("list.json", encoding='utf-8') as file:
        jsonData = json.load(file)
    file.close()
else:
    with open(DOWNLOAD_PATH + "\list.json", encoding='utf-8') as file:
        jsonData = json.load(file)
    file.close()


def candl(name, jsond, path):
    res = False
    for j in jsond:
        if 'Rubrique' in j and j['Rubrique'] == name and j['Type'] == 1:
            res = True
            path.insert(0, j['Rubrique'])
            break
        elif 'Book' in j and len(j['Book']) > 0 and j['Type'] == 0:

            res, path = candl(name, j['Book'], path)
            if res:
                path.insert(0, j['Rubrique'])
                break
        else:
            res = False
    return res, path


def addjson(po, jsond, path, num):
    res = ""
    for j in jsond:
        if 'Rubrique' in j and j['Rubrique'] == path[num] and num == len(path) - 1:
            j['Book'].append(po)
            res = j
            break
        elif 'Rubrique' in j and j['Rubrique'] == path[num] and num < len(path):
            j['Book'].append(addjson(po, j['Book'], path, num + 1))
            res = j
            break
    return res


def makepath(path):
    pa = "\\"
    for p in path:
        pa = pa + "\\" + p
        pa = pa.replace("/", "")
        pa = pa.replace(":", "")
        pa = pa.replace("*", "")
        pa = pa.replace("?", "")
        pa = pa.replace("\"", "")
        pa = pa.replace("<", "")
        pa = pa.replace(">", "")
        pa = pa.replace("|", "")

        if not os.path.isdir(DOWNLOAD_PATH + pa):
            os.mkdir(DOWNLOAD_PATH + pa)

    return pa


profile = webdriver.FirefoxOptions()
profile.set_preference("browser.download.folderList", 2)
profile.set_preference("browser.download.manager.showWhenStarting", False)
profile.set_preference("browser.download.dir", DOWNLOAD_PATH + "\dl_dir")
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
profile.set_preference("pdfjs.disabled", True)


def prog():
    s = Service(GECKODRIVER_PATH)

    driver = webdriver.Firefox(options=profile, service=s)
    driver.get('https://cas.uphf.fr/cas/login?service=https://portail.uphf.fr/uPortal/Login')

    try:
        page_login = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login")))
        page_login.find_element(By.ID, "username").send_keys(UPHF_USERNAME)
        page_login.find_element(By.ID, "password").send_keys(UPHF_MDP)
        page_login.find_element(By.NAME, "submit").click()

        driver.get('https://portail.uphf.fr/uPortal/p/scd-BeL.ctf3/max/render.uP')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="portletContent_ctf3"]/div/form/table/tbody/tr[8]/td[2]/button'))).click()
        time.sleep(1)
        window_after = driver.window_handles[0]
        driver.switch_to.window(window_after)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="portletContent_ctf3"]/div/table[2]/tbody/tr[5]/td[2]/li/strong/a'))).click()
        time.sleep(1)
        window_after = driver.window_handles[1]
        driver.switch_to.window(window_after)
        ok = False
        while not ok:
            try:

                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="navbarNavAltMarkup"]/ul/li[1]/button'))).click()
                time.sleep(1)
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="dropdown-menu-197"]/div/a'))).click()
                ok = True
            except:
                time.sleep(5)
                print("probleme a")
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                        '//*[@id="main-content"]/app-content/div/div[1]/div[1]/div/div/app-options/div/div[1]/div'))).click()
        time.sleep(1)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                        '//*[@id="main-content"]/app-content/div/div[1]/div[1]/div/div/app-options/div/div[2]/div[1]/label[1]/div'))).click()

        time.sleep(1)
        total_book = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="main-content"]/app-content/div/div[1]/div[2]/app-header/div[2]/div[1]/span'))).text

        cpt = int(jsonData['Total'])
        while cpt != int(total_book):
            #try:
            shutil.rmtree(DOWNLOAD_PATH+'\dl_dir')
            os.mkdir(DOWNLOAD_PATH + "\dl_dir")
            open(DOWNLOAD_PATH + "\dl_dir\export.pdf","w+").close()
            # Retour a 0
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="navbarNavAltMarkup"]/ul/li[1]/button'))).click()
            time.sleep(0.5)
            ok = False
            while not ok:
                try:
                    WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.XPATH, '//*[@id="dropdown-menu-197"]/div/a'))).click()
                    ok = True
                    time.sleep(0.5)
                except:
                    print("probleme a")
                    time.sleep(5)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                            '//*[@id="main-content"]/app-content/div/div[1]/div[1]/div/div/app-options/div/div[1]/div'))).click()
            time.sleep(0.2)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                            '//*[@id="main-content"]/app-content/div/div[1]/div[1]/div/div/app-options/div/div[2]/div[1]/label[1]/div'))).click()
            time.sleep(0.2)
            rebrique_div = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                (By.XPATH,
                 '//*[@id="main-content"]/app-content/div/div[1]/div[1]/div/div/app-options/div/div[2]/div[3]')))
            rubriques = rebrique_div.find_elements(By.CLASS_NAME, "control-checkbox")
            rubriques = rubriques[:-3]

            nb_book_max_ru = 0
            stop = False
            for i in range(0, len(rubriques)):

                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

                # click pour clear
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                '//*[@id="main-content"]/app-content/div/div[1]/div[1]/div/div/app-options/div/div[1]/div'))).click()


                # filtre que livre
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,
                                                                                '//*[@id="main-content"]/app-content/div/div[1]/div[1]/div/div/app-options/div/div[2]/div[1]/label[1]/div'))).click()
                # click sur la rubrique
                rubriques[i].click()
                time.sleep(1)
                # nb livre de la rubrique
                nb_book_ru = int(WebDriverWait(driver, 10).until(EC.presence_of_element_located(
                    (By.XPATH,
                     '//*[@id="main-content"]/app-content/div/div[1]/div[2]/app-header/div[2]/div[1]/span'))).text)

                # si rubrique racine
                res, path = candl(rubriques[i].text, jsonData['Book'], [])

                if res:

                    nb_book_max_ru = nb_book_max_ru + nb_book_ru
                    print(nb_book_max_ru, path)
                    if nb_book_max_ru > cpt:
                        nb_book = nb_book_max_ru - nb_book_ru
                        # créer le fichier
                        file_path = makepath(path)

                        books = driver.find_elements(By.TAG_NAME, 'app-resource')
                        # trouve la bonne page

                        while cpt > nb_book + len(books) - 1:
                            print("passage de page")
                            nb_book = nb_book + len(books)
                            driver.find_element(By.XPATH, "//*[contains(text(),'Suivant')]").click()
                            books = driver.find_elements(By.TAG_NAME, 'app-resource')


                        book = books[cpt - nb_book]

                        name = book.find_elements(By.TAG_NAME, 'div')[3].text
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
                        time.sleep(1)
                        try :
                            book.find_element(By.TAG_NAME, 'a').click()
                        except:
                            book.find_element(By.XPATH,"//*[contains(text(),'Consulter')]").click()
                        print(name+"...")
                        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,
                                                                                       '//*[@id="tabSumm"]/app-summary/div/span[1]'))).click()
                        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,
                                                                                       '//*[@id="tabSumm"]/app-summary/perfect-scrollbar/div/div[1]/div/accordion/accordion-group[1]/div/div[2]/div/div/div/div/a'))).click()

                        #WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,
                         #                                                              '//*[@id="main-content"]/app-header/div/div/div/div[2]/span[1]'))).click()

                        time.sleep(1)
                        img_src = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,
                                                                                       '//*[@id="main-content"]/app-header/div/div/div/div[3]/app-cover/div/img')))
                        with open(DOWNLOAD_PATH + "\dl_dir\\" +'couverture.png', 'wb') as file:
                            file.write(img_src.screenshot_as_png)
                        file.close()
                        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,
                                                                                       '//*[@id="main-content"]/app-header/div/app-infos/div/div/div/span[1]'))).click()

                        end_book = False
                        page = 0
                        while not end_book:
                            try:


                                # DL
                                time.sleep(1)
                                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,
                                                                                               '//*[@id="main-content"]/div/app-tools/div[2]/span'))).click()

                                tcpt = 0
                                while not os.path.isfile(DOWNLOAD_PATH + "\dl_dir\\" + 'export(' + str(page+1) + ').pdf'):
                                    time.sleep(0.2)
                                    tcpt=tcpt+1
                                    print(tcpt)
                                    if tcpt == 1700:
                                        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,
                                                                                                       '//*[@id="main-content"]/div/app-tools/div[2]/span'))).click()
                                # next page
                                WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,
                                                                                               '//*[@id="main-content"]/div/div[1]/app-content/app-book-page/div/div/div[1]/div[2]/app-previous-next/div/span'))).click()


                                page = page + 1
                            except:
                                try:
                                    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,
                                                                                                   '//*[@id="quiz-content"]/div/div/div[1]/app-start-page/div/div/div/div/button[2]'))).click()
                                    driver.refresh()
                                    WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,
                                                                                                   '//*[@id="main-content"]/div/div[1]/app-content/app-book-page/div/div/div[1]/div[1]/app-previous-next/div/span'))).click()
                                    try:
                                        t = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH,
                                                                                                           '//*[@id="quiz-content"]/div/div/div[1]/app-start-page/div/div/div/div/button[2]'))).text
                                        if 'Non' in t:
                                            end_book = True
                                    except:
                                        print("")

                                except:
                                    try:
                                        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,
                                                                                                       '//*[@id="quiz-content"]/div/div/div[1]/app-end-page/div/app-report-autoevaluation/div[1]/div/button[1]'))).click()
                                        driver.refresh()
                                        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH,
                                                                                                       '//*[@id="main-content"]/div/div[1]/app-content/app-book-page/div/div/div[1]/div[1]/app-previous-next/div/span'))).click()

                                        try:
                                            t = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH,
                                                                                                           '//*[@id="quiz-content"]/div/div/div[1]/app-start-page/div/div/div/div/button[2]'))).text
                                            if 'Non' in t:
                                                end_book = True
                                        except:
                                            print("")

                                    except:
                                        end_book = True
                        try:
                            pdfs = []
                            for pf in range (1,page):

                                pdfs.append(DOWNLOAD_PATH+'\dl_dir\export('+str(pf)+').pdf')


                            merger = PdfFileMerger()

                            for pdf in pdfs:
                                print(pdf)
                                merger.append(pdf)

                            name = name.replace("/", "")
                            name = name.replace(":", "")
                            name = name.replace("*", "")
                            name = name.replace("?", "")
                            name = name.replace("\"", "")
                            name = name.replace("<", "")
                            name = name.replace(">", "")
                            name = name.replace("|", "")
                            merger.write(DOWNLOAD_PATH+'\dl_dir\\'+name+'.pdf')
                            merger.close()

                            os.rename(DOWNLOAD_PATH+'\dl_dir\\'+name+'.pdf', DOWNLOAD_PATH+file_path+'\\'+str(cpt)+"_"+name+'.pdf')
                            os.rename(DOWNLOAD_PATH + '\dl_dir\couverture.png',DOWNLOAD_PATH + file_path + '\\' + str(cpt)+"_"+name +'_couverture'+ '.png')
                            for pzs in pdfs:
                                os.remove(pzs)

                            jsonData['info_livre'].append({'Name': name, 'Path': file_path,'couverture_name':name +'_couverture'+ '.png', 'Page': page})
                            print(str(cpt), '/', total_book, "\t", name, file_path, 'NB_Page :', page)

                            cpt = cpt + 1

                            jsonData['Total'] = cpt


                            with open(DOWNLOAD_PATH + "\list.json", "w") as file:
                                json.dump(jsonData, file, indent=4)
                            file.close()

                        except:
                            print("fat error")

                        stop = True

                if stop:
                    break
            #except Exception as e:
                #print("error",cpt, e)


    finally:
        driver.quit()


while True:
    try:
        prog()
    except:
        time.sleep(20)
        print("very fat error")



