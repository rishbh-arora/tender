import time
from .drivers import Selenium_Driver, Captcha
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = Selenium_Driver.get_driver()
solver = Captcha.get_solver()

def scrape_data():
    driver.get("https://eprocure.gov.in/eprocure/app?page=FrontEndAdvancedSearch&service=page")

    captcha_base64 = driver.find_element(By.XPATH, value='//*[@id="captchaImage"]').screenshot_as_base64

    options = {
        "phrase": False,
        "caseSensitive": True,
        "numeric": 0,
        "calc": False,
        "minLength": 1,
        "maxLength": 5,
        "hintText": "enter the text you see on the image",
        "language": "en"
    }

    try:
        while True:
            # result = {"code": input()}
            result = solver.normal(captcha_base64, **options)

            wait = WebDriverWait(driver, 3)
            filter_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="submit"]')))

            captchaText = driver.find_element(By.XPATH, value='//*[@id="captchaText"]')
            Select(driver.find_element(By.ID, value="TenderType")).select_by_value("1")
            captchaText.send_keys(result['code'])
            
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
        for link in detail_pages[:10]:
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
        return True, details
    
    except Exception as e:
        return False, e
    
    finally:
        driver.quit()


    #Organisation Chain:      /html/body/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td[1]/b
    #Chain:                   /html/body/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[1]/td[2]/b
    #Tender Reference Number: /html/body/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td[1]/b
    #Ref no:                  /html/body/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[2]/td[2]/b
    #tender ID:               /html/body/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td[1]/b
    #ID:                      /html/body/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table[2]/tbody/tr/td/table/tbody/tr[2]/td/table/tbody/tr[3]/td[2]/b


    #error box for documents: /html/body/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[4]/td/table[2]/tbody/tr/td/table/tbody/tr[6]/td/b