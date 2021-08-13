import time	
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def driver1_setup(driver, driver2, total_price):
	driver.get("https://www.easports.com/fifa/ultimate-team/web-app/")

	time.sleep(12)
	
	login_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "btn-standard.call-to-action")))
	# driver.find_element_by_class_name('btn-standard.call-to-action')

	login_button.click()

	email_box = driver.find_element_by_id("email")

	email_box.send_keys("tynous2011@yahoo.com")
	# email_box.send_keys("shivaumkumar1@gmail.com")
	# email_box.send_keys("rishi852@gmail.com")

	password_box = driver.find_element_by_id("password")

	password_box.send_keys("Rahs4032255")
	# password_box.send_keys("Hariom$0108")
	# password_box.send_keys("Pokemon@00")

	password_box.send_keys(Keys.ENTER)

	time.sleep(60)

	transfer_button = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "ut-tab-bar-item.icon-transfer")))
	# driver.find_element_by_class_name("ut-tab-bar-item.icon-transfer")
	# time.sleep(3)
	transfer_button.click()

	# time.sleep(5)

	transfer_list = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "tile.col-1-2.ut-tile-transfer-list")))
	# driver.find_element_by_class_name("tile.col-1-2.ut-tile-transfer-list")
	transfer_list.click()

	player_lists =  WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "sectioned-item-list")))
	# driver.find_elements_by_class_name("sectioned-item-list")
	relist_player_lists = player_lists[1].text.split("\n")
	player_lists = player_lists[2].text.split("\n")
	del relist_player_lists[0:2]
	del player_lists[0:2]
	total_num_of_players = int(len(player_lists) / 15) + int(len(relist_player_lists) / 15)

	while(total_num_of_players > 1):
		player_lists =  WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "sectioned-item-list")))
		# driver.find_elements_by_class_name("sectioned-item-list")
		relist_player_lists = player_lists[1].text.split("\n")
		player_lists = player_lists[2].text.split("\n")
		del relist_player_lists[0:2]
		del player_lists[0:2]
		total_num_of_players = int(len(player_lists) / 15) + int(len(relist_player_lists) / 15)
		time.sleep(5)
		all_buttons = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "btn-standard.call-to-action")))
		# driver.find_elements_by_class_name("btn-standard.call-to-action")
		found_sold_button = False
		if "Clear Sold" in all_buttons[0].text:
			found_sold_button = True
		found_list_button = False
		# if "Re-list All" in all_buttons[1].text:
		# 	found_list_button = True

		if found_sold_button:
			all_buttons[0].click()
		# elif found_list_button:
		# 	all_buttons[1].click()
		else:
			bio = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "more")))
			# driver.find_element_by_class_name("more")
			bio.click()

			player_name = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "h2")))
			# driver.find_elements_by_css_selector("h2")
			web_type = player_name[5].text
			web_name = player_name[6].text
			web_country = player_name[13].text
			web_club = player_name[14].text
			web_league = player_name[15].text

			web_stats = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "player-stats-data-component")))
			# driver.find_element_by_class_name("player-stats-data-component")
			web_stats = web_stats.text.split('\n')
			web_pac = web_stats[1]
			web_shot = web_stats[3]
			web_pass = web_stats[5]
			web_dri = web_stats[-5]
			web_def = web_stats[-3]
			web_phy = web_stats[-1]

			# time.sleep(3)

			item = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ut-navigation-button-control")))
			# driver.find_elements_by_class_name("ut-navigation-button-control")[1]
			item[1].click()

			# time.sleep(5)

			list_on_market = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "accordian")))
			
			# driver.find_element_by_class_name("accordian")
			list_on_market.click()

			player_price = driver2_setup(driver2, web_name, web_pac, web_shot, web_pass, web_dri, web_def, web_phy, web_country, web_club, web_league)
			total_price = set_prices_and_list(driver, player_price, web_type, total_price)
			print("Players left: " + str(total_num_of_players))
	return total_price

def driver2_setup(driver2, web_name, web_pac, web_shot, web_pass, web_dri, web_def, web_phy, web_country, web_club, web_league):
	search_box_name = web_name
	# search_box_name = "Lionel Messi"

	searcher = driver2.find_element_by_id("players_search")

	time.sleep(3)

	searcher.send_keys(search_box_name)

	searcher.send_keys(Keys.ENTER)

	time.sleep(5)

	price_to_set = 0

	player_list = WebDriverWait(driver2, 20).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "tr")))
	# driver2.find_elements_by_css_selector("tr")
	del player_list[0:3]
	del player_list[-1]
	search_name_array = search_box_name.split()
	adder = 0
	if len(search_name_array) > 2:
		adder = 1
	curr_player = 0
	for item in player_list:
		# change element to elements and find all players in table and change club after next player found
		player_infos = WebDriverWait(driver2, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "d-inline.pt-2.pl-3")))
		# driver2.find_elements_by_class_name("d-inline.pt-2.pl-3")
		#player_element = driver2.find_element_by_class_name("d-inline.pt-2.pl-3")
		list_of_elements = player_infos[curr_player].find_elements_by_css_selector("a")
		del list_of_elements[0]
		fut_club = list_of_elements[0].get_attribute("data-original-title")
		fut_country = list_of_elements[1].get_attribute("data-original-title")
		fut_league = list_of_elements[2].get_attribute("data-original-title")
		player_info = []
		temp_player = item.text.split('\ ')
		for information in temp_player:
			player_info.append(information.split())
		fut_overall = player_info[0][2 + adder]
		fut_position = player_info[0][3 + adder]
		fut_type = player_info[0][4 + adder]
		fut_price = player_info[0][-4]
		fut_pac = player_info[1][1]
		fut_shot = player_info[1][2]
		fut_pass = player_info[1][3]
		fut_dri = player_info[1][4]
		fut_def = player_info[1][5]
		fut_phy = player_info[1][6]

		print("FUT club: " + fut_club.strip())
		print("WEB club: " + web_club.strip().split()[0])
		curr_player += 1

		club_check = False

		#FUT club: Tottenham Hotspur
		#WEB club: Spurs
		#FUT club: Olympique de Marseille
		#WEB club: OM

		if ((web_club.strip().split()[0] in fut_club.strip()) or 
		('ASSE' in web_club.strip().split()[0] and 'AS Saint' in fut_club.strip()) or 
		('Wolves' in web_club.strip().split()[0] and 'Wolverhampton' in fut_club.strip()) or 
		('AFC' in web_club.strip().split()[0] and 'Bournemouth' in fut_club.strip()) or 
		('gladbach' in web_club.strip().split()[0] and 'Borussia Mönchengladbach' in fut_club.strip())):
			club_check = True

		if fut_pac == web_pac and fut_shot == web_shot and fut_pass == web_pass and fut_dri == web_dri and fut_def == web_def and fut_phy == web_phy and club_check:
			print("FOUND")
			price_to_set = fut_price

	price_to_set = str(price_to_set)

	if price_to_set[-1] == 'K':
		price_to_set = price_to_set
		price_to_set = float(price_to_set[:-1])
		price_to_set *= 1000
	elif price_to_set[-1] == 'M':
		price_to_set = price_to_set
		price_to_set = float(price_to_set[:-1])
		price_to_set *= 1000000

	price_to_set = int(price_to_set)
	return price_to_set

def set_prices_and_list(driver, price_to_set, web_type, total_price):
	all_buttons = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "btn-standard.call-to-action")))
	# driver.find_elements_by_class_name("btn-standard.call-to-action")
	found_sold_button = False
	if "Clear Sold" in all_buttons[0].text:
		found_sold_button = True

	if found_sold_button:
		all_buttons[0].click()
		list_on_market = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "accordian")))
		# driver.find_element_by_class_name("accordian")
		list_on_market.click()

	found_list_button = False
	# if "Re-list All" in all_buttons[1].text:
	# 	found_list_button = True

	# if found_list_button:
	# 	all_buttons[1].click()
	# 	list_on_market = driver.find_element_by_class_name("accordian")
	# 	list_on_market.click()

	all_buttons = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "btn-standard.call-to-action")))
	# driver.find_elements_by_class_name("btn-standard.call-to-action")
	found_sold_button = False
	if "Clear Sold" in all_buttons[0].text:
		found_sold_button = True

	if found_sold_button:
		all_buttons[0].click()
		list_on_market = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "accordian")))
		# driver.find_element_by_class_name("accordian")
		list_on_market.click()

	# found_list_button = False
	# if "Re-list All" in all_buttons[1].text:
	# 	found_list_button = True

	# if found_list_button:
	# 	all_buttons[1].click()
	# 	list_on_market = driver.find_element_by_class_name("accordian")
	# 	list_on_market.click()

	set_buy_price =  WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "numericInput.filled")))
	# driver.find_elements_by_class_name("numericInput.filled")

	higher_price = price_to_set

	if price_to_set == 0:
		higher_price = set_buy_price[1].get_attribute('value')
		higher_price = higher_price.replace(",", "")
		higher_price = int(higher_price)

	lower_price = int(higher_price) - 300

	min_price = set_buy_price[0].get_attribute('value')
	min_price = min_price.replace(",", "")

	if (lower_price < int(min_price)):
		if "Rare Gold" in web_type:
			lower_price = 700
		if "Common Gold" in web_type:
			lower_price = 350
		if "Rare Silver" in web_type:
			lower_price = 300
		if "Common Silver" in web_type:
			lower_price = 150

	if higher_price <= lower_price:
		higher_price += 100
	total_price += higher_price

	print(lower_price)
	print(higher_price)

	lower_price = str(lower_price)
	higher_price = str(higher_price)

	driver.execute_script("arguments[0].value = arguments[1]", set_buy_price[0], lower_price)
	driver.execute_script("arguments[0].value = arguments[1]", set_buy_price[1], higher_price)
	list_item_list = WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "btn-standard.call-to-action")))
	# driver.find_elements_by_class_name("btn-standard.call-to-action")
	# time.sleep(3)
	list_item_list[-1].click()
	print(total_price)
	return total_price


if __name__ == "__main__": 
	driver = webdriver.Chrome("C:/Users/tynou/googledriver/chromedriver.exe")
	driver2 = webdriver.Chrome("C:/Users/tynou/googledriver/chromedriver.exe")
	# driver = webdriver.Firefox()
	# driver2 = webdriver.Firefox()
	driver2.get("https://www.futbin.com/21/players")
	total_price = 0
	total_price = driver1_setup(driver, driver2, total_price)
	print(total_price)
