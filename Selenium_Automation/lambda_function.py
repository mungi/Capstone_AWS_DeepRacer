import os, time, json

from datetime import datetime, timedelta
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium import webdriver

MODEL_NAME = "Capstone-T1008-A7-A6"
SUBMIT_URL = "https://console.aws.amazon.com/deepracer/home?region=us-east-1#competition/arn%3Aaws%3Adeepracer%3A%3A968005369378%3Aleaderboard%2F35b3d210-5aca-4f4e-8247-89f19fbf4d4a/submitModel"


def get_driver():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1280x720')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--hide-scrollbars')
    chrome_options.add_argument('--enable-logging')
    chrome_options.add_argument('--log-level=0')
    chrome_options.add_argument('--v=99')
    chrome_options.add_argument('--single-process')
    chrome_options.add_argument('--homedir=/tmp')
    chrome_options.add_argument('--user-data-dir=/tmp/user-data')
    chrome_options.add_argument('--data-path=/tmp/data-path')
    chrome_options.add_argument('--disk-cache-dir=/tmp/cache-dir')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36')
    chrome_options.binary_location = "/opt/python/bin/headless-chromium"

    driver = webdriver.Chrome('/opt/python/bin/chromedriver', chrome_options=chrome_options)
    return driver


# Login AWS Console URL with IAM ID
def login_aws_console(browser):
    with open("AWS_credentials.txt", 'r') as f:
        [aws_id, username, password] = f.read().splitlines()
        
    aws_id = str(aws_id)
    url = "https://%s.signin.aws.amazon.com/console" % aws_id

    browser.get(url)
    browser.refresh()
    time.sleep(3)

    usernameInput = browser.find_elements_by_css_selector('form input')[1]
    passwordInput = browser.find_elements_by_css_selector('form input')[2]

    usernameInput.send_keys(username)
    passwordInput.send_keys(password)
    passwordInput.send_keys(Keys.ENTER)
    time.sleep(2)

    print(f"Successfully logged in to AWS account number {aws_id} with username {username}")


# Submit deepracer model to community races
def submit_model_to_community(browser):

    browser.get( SUBMIT_URL )
    browser.refresh()
    time.sleep(8)
    
    browser.find_element_by_xpath('//*[@id="awsui-select-0-textbox"]' ).click()
    time.sleep(2)
    browser.find_element_by_xpath("//span[contains(@class, 'awsui-select-option-label') and text() = '"+MODEL_NAME+"']").click()
    time.sleep(1)
    
    submitModelButton = browser.find_element_by_xpath('//button[@type="submit"]/*[text()="Submit model"]')

    re_press_submit = 5
    while re_press_submit > 0:
        try:
            submitModelButton.click()
            re_press_submit -= 1
            time.sleep(2)
        except:
            # If click failed, means that submit was successful and we got re-routed to Event starting screen
            re_press_submit = 0

    time.sleep(3)
    print(f"[{(datetime.now() + timedelta(hours=9)).strftime('%Y-%m-%d %H:%M:%S')}] Submitted model : {MODEL_NAME}")
    

def lambda_handler(event, context):
    print(" ================ Starting Function ================ ")

    browser = get_driver()

    login_aws_console(browser)
    submit_model_to_community(browser)

    browser.quit()

    return {
        'statusCode': 200,
        'body': json.dumps('Submitted model' + MODEL_NAME)
    }
