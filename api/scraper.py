import time
from .drivers import Selenium_Driver, Captcha
from .utils.catpcha import solve_captcha
from .utils.storage import upload_to_gcs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from tender.settings.base import DOWNLOAD_DIRECTORY, GCS_TENDER_ZIP_BUCKET

driver = Selenium_Driver.get_driver()
solver = Captcha.get_solver()
wait = WebDriverWait(driver, 3)

def wait_for_download_completion(download_dir):
    while any([filename.endswith(".crdownload") for filename in os.listdir(download_dir)]):
        time.sleep(1)

def get_latest_file(download_dir):
    files = os.listdir(download_dir)
    paths = [os.path.join(download_dir, file) for file in files if not file.startswith('.')]
    print(paths)
    a = max(paths, key=os.path.getctime)
    print(a)
    return a

def handle_zip_captcha(url, tender_id):
    print("getting that page");
    driver.get(url)
    solve_captcha(driver, solver)
    submit = driver.find_element(By.XPATH, value='//*[@id="Submit"]').click()
    try:
        zip_download = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="DirectLink_7"]')))
    except:
        try:
            zip_download = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="DirectLink_8"]')))
        except:
            print("Captcha failed")
            return False
        else:
            print("Zip download found from 7")
            zip_download.click()
            return True
    else:
        print("Zip download found from 7")
        zip_download.click()
    wait_for_download_completion(DOWNLOAD_DIRECTORY)
    return upload_to_gcs(get_latest_file(DOWNLOAD_DIRECTORY), GCS_TENDER_ZIP_BUCKET , f"{tender_id}.zip")

def scrape_data():
    driver.get("https://eprocure.gov.in/eprocure/app?page=FrontEndAdvancedSearch&service=page")

    try:
        while True:
            filter_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submit"]')))
            Select(driver.find_element(By.ID, value="TenderType")).select_by_value("1")
            solve_captcha(driver, solver)
            
            filter_button.click()
            time.sleep(3)       
            try:
                search_result_check = driver.find_element(By.XPATH, value='//*[@id="AdvancedSearch"]')
                break
            except:
                print("Captcha failed, retrying")
                continue

        detail_pages = []
        for _ in range(1):
            for tender in range(-1, 19):
                xpath = "DirectLink_0"
                if tender != -1:
                    xpath += f"_{tender}"
                link = driver.find_element(By.XPATH, value=f'//*[@id="{xpath}"]')
                detail_pages.append(link.get_attribute('href'))
            next_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="linkFwd"]')))
            next_button.click()
        
        details = []
        for link in detail_pages[:3]:
            tender = {}
            top_base_path = "/html/body/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/"
            driver.get(link)

            for i in range(3):
                tender[driver.find_element(By.XPATH, value=top_base_path + f"tr[{i+1}]/td[1]/b").text] = driver.find_element(By.XPATH, value=top_base_path + f"tr[{i+1}]/td[2]/b").text
            try:
                tender["zip"] = driver.find_element(By.XPATH, value='//*[@id="DirectLink_8"]').get_attribute("href")
            except:
                print(f"Documents not available for {tender.get('Tender Reference Number')}")
                tender["zip"] = None
            details.append(tender)
        print(details)
        return True, details
    
    except Exception as e:
        print(e)
        return False, e


    #Organisation Chain:      /html/body/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/b
    #Chain:                   /html/body/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/b
    #Tender Reference Number: /html/body/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td[1]/b
    #Ref no:                  /html/body/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/b
    #tender ID:               /html/body/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td[1]/b
    #ID:                      /html/body/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/b


    #error box for documents: /html/body/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table[2]/tbody/tr/td/table/tbody/tr[6]/td/b