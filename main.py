import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import sys
import pyautogui

def allowCert():
    sleep(3)
    width, height = pyautogui.size()
    pyautogui.moveTo(width/2, height/2 + 100)
    pyautogui.click()

executable_path = "C:\\Users\\nataniel\\Desktop\\AutomacoesDPI\\contab-dte-main\\chromedriver.exe"

os.environ["webdriver.chrome.driver"] = executable_path

chrome_options = Options()
chrome_options.add_extension('./Web-PKI.crx')

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://dte.sefaz.al.gov.br/dte/login/?redirect=/dte/client/nucleo/nova-base/public/#/")

selectButton = WebDriverWait(driver, 100).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div/div/form/div[1]/div/div/div/div'))
)

selectButton.click()

i = 0
certs = WebDriverWait(driver, 100).until(
    EC.presence_of_all_elements_located((By.XPATH, './/*[contains(concat(" ",normalize-space(@class)," ")," rc-virtual-list-holder-inner ")]/div'))
)
failed = 0
for certIndex in range(0, len(certs)):
    if certIndex != 0 or failed == 1:
        # Faz logout
        failed = 0
        try:
            print('Logout because fail or index +1')
            driver.delete_all_cookies()
            driver.get('about:blank')
            driver.get("https://dte.sefaz.al.gov.br/dte/login/?redirect=/dte/client/nucleo/nova-base/public/#/")

            selectButton = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div/div/form/div[1]/div/div/div/div'))
            )

            selectButton.click()
            certs = WebDriverWait(driver, 100).until(
                EC.presence_of_all_elements_located((By.XPATH, './/*[contains(concat(" ",normalize-space(@class)," ")," rc-virtual-list-holder-inner ")]/div'))
            )
        except Exception as e:
            print('Falha ao logout')

    cert = certs[certIndex]
    companyName = 'Não identificada'
    try:
        companyName = cert.get_attribute('textContent')
        print(companyName)
        print('Cert clicking')
        cert.click()
        driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/form/div[2]/div/div/div/button').click()
        allowCert()
        companiesLen = 1
        try:
            print('Getting companies')
            companies = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.SelecionarContratoHonorario__List > div'))
            )
            companiesLen = len(companies)
        except:
            companiesLen = 1
        for companyIndex in range(0, companiesLen):
            if companyIndex != 0:
                # Faz logout
                print('Logout')
                driver.delete_all_cookies()
                driver.get('about:blank')
                driver.get("https://dte.sefaz.al.gov.br/dte/login/?redirect=/dte/client/nucleo/nova-base/public/#/")

                selectButton = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div/div/form/div[1]/div/div/div/div'))
                )
                WebDriverWait(driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[2]/div/div/form/div[1]/div/div/div/div'))
                )
                selectButton.click()
                certs = WebDriverWait(driver, 30).until(
                    EC.presence_of_all_elements_located((By.XPATH, './/*[contains(concat(" ",normalize-space(@class)," ")," rc-virtual-list-holder-inner ")]/div'))
                )
                certs[certIndex].click()
                driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/form/div[2]/div/div/div/button').click()
                allowCert()
                companies = WebDriverWait(driver, 30).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.SelecionarContratoHonorario__List > div'))
                )

            if companiesLen != 1:
                company = companies[companyIndex]
                companyName = company.get_attribute('textContent')
                print('Is more than one company')
                company.click()
                driver.find_element(By.CSS_SELECTOR, '.SelecionarContratoHonorario__Button').click()

            # Espera carregar
            iframe = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.Audora__Body > iframe'))
            )
            driver.switch_to.frame(iframe)
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH , '/html/body/div[1]/div/div[3]/div/div[1]/a[2]/span'))
            )
            
            # Printa
            print('Screenshot')
            sleep(2)
            i = i + 1
            screenshotPath = os.path.realpath(os.path.join('output', companyName[:32].replace(':', '') + str(i) + '.png'))
            print(screenshotPath)
            driver.get_screenshot_as_file(screenshotPath)
    except Exception as e:
        failed = 1
        print(companyName + ' Failed')
        print(e)
sys.exit(42)