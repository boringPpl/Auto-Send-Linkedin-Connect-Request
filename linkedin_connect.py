# Standard imports
from selenium import webdriver
from time import sleep
from login import loginLinkedin
import gspread
from google.oauth2.service_account import Credentials
print('- Finish importing standard packages')

# Authorize Google Sheet API 
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    '/Users/admin/opt/anaconda3/lib/python3.7/site-packages/gspread/connectLinkedin.json',
    scopes=scopes
)

gc = gspread.authorize(credentials)
print('- Finish authorizing Google API')

# Task 1: Initialize a browser and Login
driver = webdriver.Chrome()
driver.get("https://www.linkedin.com/login")
login = loginLinkedin(driver, 'credentials.txt')

# Task 2: Load profile URLs and Names from Google sheet
url = 'https://docs.google.com/spreadsheets/d/1HljzxrENkmhhj3pUvCCxhYh61pgkPD6OwWK4PB-drSU/'
workbook = gc.open_by_url(url)
sheet = workbook.worksheet('Sheet63')
user_name = sheet.col_values(1)
user_link = sheet.col_values(2)
print('- Finish loading data from Google Sheet')

# Task 3: Access the profile, Locate & Interact with elements
print('- Start connecting ...')
FROM_ROW = int(input('   - Which profile to start? Enter the row number: '))
TO_ROW = int(input('   - Which profile to end? Enter the row number: '))

for profile in range(FROM_ROW-1, TO_ROW):
    driver.get(user_link[profile])
    print('   - Accessing: ', user_link[profile])
    sleep(2)

    connect_but = driver.find_element_by_xpath("//*[@class='pv-s-profile-actions pv-s-profile-actions--connect ml2 artdeco-button artdeco-button--2 artdeco-button--primary ember-view']")
    connect_but.click()
    sleep(2)

    addnote_but = driver.find_element_by_xpath("//*[@class='mr1 artdeco-button artdeco-button--muted artdeco-button--3 artdeco-button--secondary ember-view']")
    addnote_but.click()
    sleep(2)

    name = user_name[profile].split()[0]
    message = f"Hi {name}, I'm sending this message using Python, which helps Automate the process, Increase the result by 10 times, and Save you 2-3hrs a day. If you're interested in doing the same, check out my tutorial: https://www.youtube.com/channel/UC1Rt70-Gg3ND_zoeYe1cJGA"
    sleep(2)

    message_box = driver.find_element_by_id("custom-message")        
    message_box.send_keys(message)
    sleep(2)

    send_but = driver.find_element_by_xpath("//*[@class='ml1 artdeco-button artdeco-button--3 artdeco-button--primary ember-view']")
    send_but.click()
    print('   - Sent request to: ', user_name[profile])    
    sleep(2)

print('Mission completed!!!')