# Task 1: Login to Linkedin
from selenium import webdriver
from time import sleep

def loginLinkedin(driver, f_credential):

    # Import username and password
    credential = open(f_credential)
    line = credential.readlines()
    username = line[0]
    password = line[1]

    # Key in login credentials
    email_field = driver.find_element_by_id('username').send_keys(username)
    password_field = driver.find_element_by_name('session_password').send_keys(password)
    print('- Finish keying in the credentials')
    sleep(2)

    # Click the Login button
    signin_field = driver.find_element_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[3]/button').click()
    print('- Finish logging in to Linkedin')