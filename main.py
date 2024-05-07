import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

executable_path = "/Users/tonimoreira/Projects/contab-dte/chromedriver"
os.environ["webdriver.chrome.driver"] = executable_path

chrome_options = Options()
chrome_options.add_extension('./Web-PKI.crx')

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://dte.sefaz.al.gov.br/dte/login/?redirect=/dte/client/nucleo/nova-base/public/#/")

selectButton = WebDriverWait(driver, 100).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div/div/form/div[1]/div/div/div/div'))
)

selectButton.click()

certs = WebDriverWait(driver, 100).until(
    EC.presence_of_all_elements_located((By.XPATH, './/*[contains(concat(" ",normalize-space(@class)," ")," rc-virtual-list-holder-inner ")]/div'))
)
for certIndex in range(0, len(certs)):
    if certIndex != 0:
        # Faz logout
        driver.delete_all_cookies()
        driver.get("https://dte.sefaz.al.gov.br/dte/login/?redirect=/dte/client/nucleo/nova-base/public/#/")

        selectButton = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div/div/form/div[1]/div/div/div/div'))
        )

        selectButton.click()
        certs = WebDriverWait(driver, 100).until(
            EC.presence_of_all_elements_located((By.XPATH, './/*[contains(concat(" ",normalize-space(@class)," ")," rc-virtual-list-holder-inner ")]/div'))
        )

    cert = certs[certIndex]
    cert.click()
    driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/form/div[2]/div/div/div/button').click()
    companies = WebDriverWait(driver, 100).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.SelecionarContratoHonorario__List > div'))
    )
    companiesLen = len(companies)
    for companyIndex in range(0, companiesLen):
        if companyIndex != 0:
            # Faz logout
            driver.delete_all_cookies()
            driver.get("https://dte.sefaz.al.gov.br/dte/login/?redirect=/dte/client/nucleo/nova-base/public/#/")

            selectButton = WebDriverWait(driver, 100).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[2]/div/div/form/div[1]/div/div/div/div'))
            )

            selectButton.click()
            certs = WebDriverWait(driver, 100).until(
                EC.presence_of_all_elements_located((By.XPATH, './/*[contains(concat(" ",normalize-space(@class)," ")," rc-virtual-list-holder-inner ")]/div'))
            )
            certs[certIndex].click()
            driver.find_element(By.XPATH, '//*[@id="root"]/div/div[2]/div/div/form/div[2]/div/div/div/button').click()
            companies = WebDriverWait(driver, 100).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.SelecionarContratoHonorario__List > div'))
            )

        company = companies[companyIndex]
        companyName = company.get_attribute('textContent')
        company.click()
        driver.find_element(By.CSS_SELECTOR, '.SelecionarContratoHonorario__Button').click()

        # Espera carregar
        iframe = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '.Audora__Body > iframe'))
        )
        driver.switch_to.frame(iframe)
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.XPATH , '/html/body/div[1]/div/div[3]/div/div[1]/a[2]/span'))
        )
        
        # Printa
        print('Screenshot')
        sleep(2)
        screenshotPath = os.path.join('./output', companyName + '.png')
        driver.get_screenshot_as_file(screenshotPath)