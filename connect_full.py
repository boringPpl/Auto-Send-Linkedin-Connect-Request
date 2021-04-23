# selenium imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

# google sheets imports
import gspread
import time
import os
from oauth2client.service_account import ServiceAccountCredentials

# linkedIn email and password
USER_email = "youremail"
USER_password = "yourpassword"

# define range from the excel sheet
FROM = 56 # row -1
TO = 80 # exact row

# fetch data from google sheets
scope = ['https://spreadsheets.google.com/feeds']
creds = ServiceAccountCredentials.from_json_keyfile_name('gspread_credential.json',scope)
gc = gspread.authorize(creds)
sh = gc.open_by_key("1HljzxrENkmhhj3pUvCCxhYh61pgkPD6OwWK4PB-drSU")
outreachList = sh.get_worksheet(0)
user_name = outreachList.col_values(2)
user_link = outreachList.col_values(3)

# setup selenium webdriver
opt = webdriver.ChromeOptions()
#opt.add_extension("Block-image_v1.1.crx")
opt.add_argument('--disable-gpu')
opt.add_argument("--window-size=1920,1080")
opt.add_argument("--start-maximized")
opt.add_argument('--disable-dev-shm-usage')
opt.add_argument('--no-sandbox')
opt.add_argument('--ignore-certificate-errors')
#opt.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36")
driver = webdriver.Chrome(options=opt)

# setup wait
wait = WebDriverWait(driver, 10)

# login
driver.get("https://www.linkedin.com/login")
time.sleep(2)
usernameInput = driver.find_element_by_id("username")
usernameInput.send_keys(USER_kai)
time.sleep(3)
passwordInput = driver.find_element_by_id("password")
passwordInput.send_keys(PWD_kai)
time.sleep(1)
passwordInput.send_keys(Keys.RETURN)
def alert_out_of_invitation():
    print("****** Out of invitations. Please remove unreplied invitations on linkedIn website! ******")
    os.system('say "Out of invitations"')
    print('\a\a\a')
def check_exists_by_xpath(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

# Close the message box
time.sleep(3)
chatBox = driver.find_elements_by_xpath("//button[@class='msg-overlay-bubble-header__control msg-overlay-bubble-header__control--new-convo-btn artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--1 artdeco-button--tertiary ember-view']")
chatBox[1].click()

# connect to profiles
for i in range(FROM, TO):
    # go to profile page
    driver.get(user_link[i])
    NAME = user_name[i]
    print(NAME)
    FIRST_NAME = NAME.split()[0]
    NOTE = f"Hi {FIRST_NAME}, we are putting together a hand-picked class of learners interested in breaking into Data science. Your experience looks like a good fit. We will like to invite you for a 15 min conversation to discuss your current goals and obstacles. Will you open to this?"
    time.sleep(2)
    # if Pending or Restricted profile move to next profile
    if driver.find_elements_by_xpath("//*[contains(text(), 'Pending')]") or (NAME == "LinkedIn Member"):
        continue
    # click connect button
    connectBtn = driver.find_elements_by_xpath("//button[@class='pv-s-profile-actions pv-s-profile-actions--connect ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")
    if connectBtn:
        connectBtn[0].click()
        time.sleep(2)
    else:
        # Open the More... dropdown
        moreBtn = driver.find_elements_by_xpath("//button[@class='ml2 pv-s-profile-actions__overflow-toggle artdeco-button artdeco-button--muted artdeco-button--2 artdeco-button--secondary artdeco-dropdown__trigger artdeco-dropdown__trigger--placement-bottom ember-view']")
        moreBtn[0].click()
        time.sleep(2)
        # driver.execute_script("arguments[0].click();", moreBtn)
        # If already connected move to next profile
        if driver.find_elements_by_xpath("//span[contains(text(), 'Remove Connection')]") or driver.find_elements_by_xpath("//span[contains(text(), 'Unfollow')]"):
            continue
        # wait for the connect button to appear
        connectBtn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Connect')]/ancestor::li")))
        if connectBtn:
            connectBtn.click()
            # skip if user require email to connect
            if driver.find_elements_by_xpath("//input[@name='email']"):
                continue
    # click add note button
    addNoteBtn = driver.find_elements_by_xpath("//button[@aria-label='Add a note']")[0]
    addNoteBtn.click()
    time.sleep(2)
    # fill in the note message
    noteInput = driver.find_elements_by_xpath("//*[@id='custom-message']")[0]
    noteInput.send_keys(NOTE)
    time.sleep(2)
    # Send note message
    if driver.find_elements_by_xpath("//button[@aria-label='Send invitation']"):
        driver.find_elements_by_xpath("//button[@aria-label='Send invitation']")[0].click()
    else :
        driver.find_elements_by_xpath("//button[@aria-label='Send now']")[0].click()
    # If out of inviations
    time.sleep(1)
    if check_exists_by_xpath("//h2[@id = 'ip-fuse-limit-alert__header']"):
        alert_out_of_invitation()
        break
        
# driver.close()