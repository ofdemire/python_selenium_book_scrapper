from config2 import keys
from selenium import webdriver
import time
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import csv
from urllib.error import HTTPError
from urllib.error import URLError
import time
import sys
import random
import os



books=[]


with open('input_2.txt', 'r') as csv_file:
	csv_reader = csv.reader(csv_file)

	
	for line in csv_reader:
		if(line != []):
			books.append(line)


def exclude_data(objects, sy):
	excluded_data = objects.findAll("td",{"class" : "results-table-center"})
	inn=0
	excluded_list=[]

	for index in excluded_data:
		if(inn%3==1):
			excluded_list.append(index)
		inn =inn+1

	temp =excluded_list[sy].findAll("span",{"class" : "results-explanatory-text-Logo"})
	if(len(temp) >= 2):
		if "Usa Mart" in temp[0].get_text():
			return 0
		elif(("Canada" not in temp[2].get_text()) and ("United States" not in temp[2].get_text())):	
			return 0

	return 1



def clean_up_csv(mini, maxi ):


	with open("input_2.txt", "r") as f:
		data = list(csv.reader(f))

	data.reverse()

	with open("input_2.txt","w",newline='') as f:
		writer = csv.writer(f)
		for row in data:
			writer.writerow(row)
			mini = mini +1
			if(maxi < mini):
				break;


def order(k):
	Global_counter = 0
	driver.get(k['product_url'])
	array = []
	total_num=0

	var = int(random.random()*10000)

	kal = 'to_write' + str(var)
	print(kal)

	with open( kal +'.csv', 'w', newline = '') as f:
		thewriter = csv.writer(f, quoting = csv.QUOTE_ALL)

		for index in books:
			try:
				print(index)
				Global_counter = Global_counter +1
				driver.find_element_by_xpath('//*[@id="header-search-form-input"]').send_keys(index)
				driver.find_element_by_xpath('//*[@id="header-search-form"]/div/button').click()
				time.sleep(1)
				html = urlopen(driver.current_url)
				bsObj = BeautifulSoup(html, "lxml")
				nameList = bsObj.findAll("table", {"class": "results-table-Logo"})
				my_list = nameList[1].findAll("img")
				priceList = nameList[1].findAll("span" , {"class": "results-price"})
				

				Amazon_price = 0
				price_index = 0
				count=0
				current_price=0
				current_index=0
				counter=0

				difference=0


				if(my_list[0]['title'] != "Amazon.com" and my_list[0]['title']!= "Amazon.com (Prime)"):
					for line in my_list:
						if(line['title'] == "Amazon.com" or line['title'] == "Amazon.com (Prime)"):
							price_index = count
							break
							
						
						count = count+1
						
					Amazon_price = priceList[price_index].get_text()

					flag=0

					for line in my_list:
						if "Amazon.ca" in line["title"]:
							if(exclude_data(nameList[1], counter) == 0):
								counter=counter+1
								continue

							flag=1
							current_index = counter
							break

						counter=counter+1




					current_price = priceList[current_index].get_text()

					temp = re.findall(r"$\d*\.\d+|\d+", Amazon_price)
					Amazon_price = float(temp[0]) + float(temp[1])/100

					temp = re.findall(r"$\d*\.\d+|\d+", current_price)
					current_price = float(temp[0]) + float(temp[1])/100

					if(flag == 0):
						current_price = 999

					difference = Amazon_price - current_price

					print("first price:", current_price)
					print("amazon price:",Amazon_price)
					print("difference:", difference)
					print("You collected total:", total_num)

					if((difference/current_price) >= 1 ):
						print("PRINTED")
						total_num =total_num+1
						thewriter.writerow([index])
						thewriter.writerow([difference])
						thewriter.writerow([current_price])


			except AttributeError as e:
				print(e)
			except HTTPError as e:
				print("HTTPError")
			except URLError as e:
				print("URLError")
			except Exception as e:
				try:
					print(e, "---> OTHER EXCEPTION ")
					driver.execute_script("window.open('https://www.bookfinder.com/search/?ac=sl&st=sl&ref=bf_s2_a1_t1_1&qi=a8n.Ajge,brF5LCeKgMmkGPRT3c_1497963026_1:1:2&bq=author%3Ddon%2520tapscott%26title%3Dblockchain%2520revolution%2520how%2520the%2520technology%2520behind%2520bitcoin%2520and%2520other%2520cryptocurrencies%2520is%2520changing%2520the%2520world','new window')")
					driver.switch_to_window(driver.window_handles[1])
					continue
				
				except Exception as e:
					f.close()
					clean_up_csv(0,len(books) - Global_counter)
					print(e, "---> RESTART THE PROGRAM FROM SCRACH")
					os.execl(sys.executable, sys.executable, *sys.argv)
					


if (__name__ == '__main__'):

	print(len(books))
	chromeOptions = webdriver.ChromeOptions()

	# chromeOptions.add_argument("--headless")

	prefs = {'profile.managed_default_content_settings.images':2}

	chromeOptions.add_experimental_option("prefs", prefs)

	driver = webdriver.Chrome('./chromedriver', chrome_options=chromeOptions)
	order(keys)