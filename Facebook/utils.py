from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import pandas as pd
import os
from bs4 import BeautifulSoup



def log_into_facebook(email, password):
	# code to ignore browser notifications
	chrome_options = webdriver.ChromeOptions()
	prefs = {"profile.default_content_setting_values.notifications" : 2}
	chrome_options.add_experimental_option("prefs",prefs)

	# open the browser
	driver = webdriver.Chrome('F:/chromedriver.exe',chrome_options=chrome_options)
	# go to the webpage
	driver.get("https://wwww.facebook.com/")
	# target username
	username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
	password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))
	# enter username and password
	username.clear()
	username.send_keys(email)
	password.clear()
	password.send_keys(password)

	# target the login button and click it
	time.sleep(5)
	button = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

	# logged in!
	print("Logged in")



def crawl_friends_list(profile="https://mbasic.facebook.com/USERNAME"):
	root_url = "https://mbasic.facebook.com"
	url = os.path.join(profile, 'friends')

	friends = []
	idx = 0

	while True:
	    time.sleep(5)

	    driver.get(url)
	    html = driver.page_source
	    html = BeautifulSoup(html)
	    names = html.find_all(class_ = "w t")
	    
	    for name in names:
	        friend = name.text.split('1')[0]
	        friends.append(friend)
	        print(idx, friend)
	        idx += 1
	    
	    next_page_url = html.find_all("a")
	    next_page_url = next_page_url[-8]['href']
	    url = root_url + next_page_url
	    
	    if len(url) < 150:
	        break

	return pd.DataFrame({"Name": friends})