from selenium.webdriver.common.by import By

def solve_captcha(driver, solver):
    print("Resolving captcha")
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
    captcha_base64 = driver.find_element(By.XPATH, value='//*[@id="captchaImage"]').screenshot_as_base64
    print(captcha_base64)
    if len(captcha_base64) % 4 != 0:
        captchaText += "=" * (4 - len(captcha_base64) % 4)
    result = solver.normal(captcha_base64, **options)
    captchaText = driver.find_element(By.XPATH, value='//*[@id="captchaText"]')
    captchaText.send_keys(result['code'])