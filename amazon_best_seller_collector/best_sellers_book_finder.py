from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random
import csv
import sys
import os
from urllib.error import HTTPError
from urllib.error import URLError

random.seed(datetime.datetime.now())


def getLinks(articleURL, oldBsObj):
	try:
		html = urlopen("https://www.amazon.com"+articleURL)
		bsObj = BeautifulSoup(html, "lxml")
		return bsObj

	except AttributeError as e:
		return oldBsObj
	except HTTPError as e:
		print("HTTPError")
		return oldBsObj
	except URLError as e:
		print("URLError")
		return oldBsObj

def links(articleURL,oldBsObj):
	try:
		html = urlopen(articleURL)
		bsObj = BeautifulSoup(html, "lxml")
		return bsObj
	except Exception as e:
		print("problem inside the Links")
		return oldBsObj


def order(insideObj,index,counter,rank):
	try:
		temp = insideObj.findAll("div",{"class": "content"})
		

		temp_2 = temp[0].findAll("li")
		#because isbn-13 number is at 4. line

		obj = temp[0].findAll("li", {"id" : "SalesRank"})

		char_arr=""
		first_position=0
		last_position=0


		last_position = obj[0].get_text().find(" in Books")
		first_position = obj[0].get_text().find("#")
		first_position=first_position+1

		while(first_position < last_position):
			if(obj[0].get_text()[first_position].isdigit()):
				char_arr += obj[0].get_text()[first_position]
			first_position = first_position+1



		rank[0] = int(char_arr)
		print(rank[0])

		string= temp_2[4].get_text()[8:]

		sayac[0] = 0

		print(string)
		return string

	except Exception as e:
		rank[0]=999999
		sayac[0] = sayac[0] +1
		index[0] = index[0] - 1
		print("couldn't scrape the book", e)
		return "9780385480017"

if (__name__ == '__main__'):

	kitap_liste=[]
	collected_book=0

	with open('input.csv', 'r') as csv_file:
		csv_reader = csv.reader(csv_file)

	
		for line in csv_reader:
			kitap_liste.append(line)

	with open('mycsv.csv.txt', 'w', newline = '') as f:
		thewriter = csv.writer(f, quoting = csv.QUOTE_ALL)

		General_counter=0

		while(General_counter < len(kitap_liste)):
			try:

				rank = [0]
				sayac = [0]
				pass_point=0
				newObj = getLinks( kitap_liste[General_counter][0] , "/s/ref=lp_468226_pg_2?rh=n%3A283155%2Cn%3A%212349030011%2Cn%3A465600%2Cn%3A468226&page=2&ie=UTF8&qid=1545237856")
				first_newObj =newObj

				
				if(isinstance(newObj,str)):
				 	continue
				else:
				 	thewriter.writerow([kitap_liste[General_counter][0]])

				print(kitap_liste[General_counter][0])
				
				#ilkine bir yaz ikinciye ikiyi yaz yoksa ilk syfa gide



				temp_obj=newObj.findAll("div", {"class": "img_header hdr noborder"})

			
				last_num=int(temp_obj[0].findAll("span", {"class": "pagnDisabled"})[0].get_text())


				bsObj = None
				test=0
				
				count=0;

				while(count < last_num ):


					if(pass_point >= 45):
						thewriter.writerow(["Passing because of 35 unranking books is collected"])
						break

					if(newObj!=bsObj and count==0):
						bsObj=newObj
						booklist = bsObj.findAll("div", {"class": "a-fixed-left-grid-inner"})
						print("booklist lenght: ", len(booklist))
						index=0
						while(index <len(booklist)):
							temp = booklist[index].findAll("a", {"class" : "a-link-normal s-access-detail-page  s-color-twister-title-link a-text-normal"})
							link = temp[0].attrs["href"]

							if("ebook" in link):
								print("passing e-book")
								index =index +1
								continue


							inside_obj = links(link,bsObj)
							index = [index]
							gecici = [order(inside_obj,index,sayac,rank)]

							if(gecici!= ["9780385480017"]):
								if(rank[0] <= 300000):
									pass_point=0
									thewriter.writerow(gecici)
									collected_book = collected_book+1
								else:
									pass_point=pass_point +1


							index = index[0]
							rank= [0]
							print(link)


							index=index+1
							print("size of the array= ", collected_book)
							print("unranked books: ", pass_point)
							print(index)
							if(sayac[0] > 35):
								index = index+1
								sayac[0]=0

						count = count+1

					elif(newObj!=bsObj):
						bsObj=newObj
						all_part_of_book_list = bsObj.findAll("div", {"class": "s-result-list sg-row"})

						booklist = all_part_of_book_list[0].findAll("a", {"class": "a-link-normal a-text-normal"})
						print("BOOKLIST LENGHT: ", len(booklist))
						index=0
						while(index <len(booklist)):
							link = "https://www.amazon.com" + booklist[index].attrs["href"]

							if("ebook" in link):
								print("passing e-book")
								index = index +1
								continue

							inside_obj = links(link,bsObj)
							index = [index]
							gecici = [order(inside_obj,index,sayac,rank)]

							if(gecici!= ["9780385480017"]):
								if(rank[0] <= 300000):
									pass_point=0
									thewriter.writerow(gecici)
									collected_book = collected_book+1
								else:
									pass_point=pass_point +1


							index = index[0]
							rank= [0]
							print(link)
							index=index+1
							print("size of the array= ", collected_book)
							print("unranked books: ", pass_point)
							print(index)
							if(sayac[0] > 55):
								index = index+1
								sayac[0]=0

						count = count+1

					if(count <last_num-1 and count ==1):
						next_page = bsObj.findAll("a", { "class" : "pagnNext"})


						print("lenght:", len(next_page))
						print(next_page[0].attrs["href"])
						newObj = getLinks(next_page[0].attrs["href"],bsObj)

					elif(count <last_num-1):

						next_page = bsObj.findAll("li", { "class" : "a-last"})
						next_page = next_page[0].findAll("a")

						print("lenght:", len(next_page))
						print(next_page[0].attrs["href"])
						newObj = getLinks(next_page[0].attrs["href"],bsObj)

						
					else:
						count = count+1

				General_counter = General_counter +1

			except Exception as e:
				thewriter.writerow(["Passing because of str problem exception: "])
				print("str problem ---> ",e)
				exc_type, exc_obj, exc_tb = sys.exc_info()
				fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
				print(exc_type, fname, exc_tb.tb_lineno)
				General_counter = General_counter +1
				continue







		