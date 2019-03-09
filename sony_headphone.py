import requests
from selenium import webdriver
import selenium as se
from selenium.common.exceptions import NoSuchElementException  
import time
from time import sleep
from random import randint

post_params = { 'bot_id' : 'botID', 'text': "starting product bot" }
requests.post('https://api.groupme.com/v3/bots/post', params = post_params)

options = se.webdriver.ChromeOptions()

# chrome is set to headless
options.add_argument('headless')

driver = se.webdriver.Chrome(options=options)

# The Amazon product you want to track
driver.get("https://www.amazon.com/Sony-Noise-Cancelling-Headphones-WH1000XM3/dp/B07G4MNFS1/ref=sr_1_2?crid=N5OCS4NJDH4M&keywords=sony+wh-1000xm3&qid=1551040801&s=gateway&sprefix=sony+%2Caps%2C120&sr=8-2")

# sets base price once
global_base_price = driver.find_element_by_xpath('//*[@id="priceblock_ourprice"]').text

def check_change_by_xpath(xpath, base_price):
    try:
        # refreshes the page, finds the price
        # if the price changed, the current price is returned
        driver.refresh
        current_price = driver.find_element_by_xpath('//*[@id="priceblock_ourprice"]').text
        if current_price != base_price:
            return current_price
    except requests.exceptions.RequestException as e:
        #Sends an error message and waits another 60 seconds
        post_params = { 'bot_id' : 'botID', 'text': str(e) }
        requests.post('https://api.groupme.com/v3/bots/post', params = post_params)
        sleep(60)
    return False

while True:
    current_state = check_change_by_xpath('//*[@id="priceblock_ourprice"]', global_base_price)
    print("curr state ", current_state)
    if current_state != False:
        global_base_price = current_state
        post_params = { 'bot_id' : 'botID', 'text': check_change_by_xpath('//*[@id="priceblock_ourprice"]',global_base_price).text }
        requests.post('https://api.groupme.com/v3/bots/post', params = post_params)
    sleep(randint(3,5))