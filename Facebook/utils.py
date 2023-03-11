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



def extract_reactions(url, react='love', post_title='dpAtAirport'):
	# it takes the url to list of love/like/wow/care reaction of a post/photo, not the url to post/photo
	# e.g. url = "https://mbasic.facebook.com/ufi/reaction/profile/browser/fetch/?ft_ent_identifier=pfbid02tLqD2SL6dbugRWM4XgZwjgrnxEEJUChbj3wTCoMbtEM9HShv7MHjEa8R3aUpqAYEl&limit=10&reaction_type=16&reaction_id=613557422527858&total_count=2&paipv=0&eav=AfbNJlNIXZ7t0QFf-4_o60AhFfAomLRc3vdoKXhveAQAkaJQmi9__4J4IRKlHvbnZGA"

	root_url = "https://mbasic.facebook.com"

	friends_reacted = []
	# idx = 1

	while True:
	    time.sleep(5)
	    driver.get(url)
	    html = driver.page_source
	    html = BeautifulSoup(html)
	    names = html.find_all(class_ = "bj")
	    for name in names:
	        friend = name.text.split('1')[0]
	        friends_reacted.append(friend)
	        # print(idx, friend)
	        # idx += 1
	    
	    next_page_url = html.find_all("a")
	    next_page_url = next_page_url[-1]['href']
		# print(next_page_url)
	    url = root_url + next_page_url
	    
		# print(url)
	    
	    if len(url) < 150:
	        break

	df = pd.DataFrame({
	    "Name": list(set(friends_reacted)), 
	    "Reaction": [react for _ in range(len(list(set(friends_reacted))))],
	    "Post_Type": [post_title for _ in range(len(list(set(friends_reacted))))],
	})

	return df