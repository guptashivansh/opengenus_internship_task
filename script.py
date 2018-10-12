from bs4 import BeautifulSoup
import requests
import urllib.request
import re
from urllib.parse import urlparse
import tldextract
#various imports during the assignment

def get_count_url(url): # get the umber of links having the same domain and suffix
	r = requests.get(url)
	soup = BeautifulSoup(r.text, "html.parser")
	count = 0
	urls={} #dictionary for the domains
	# input_domain=url.split('//')[1].split('/')[0]
	#library to extract the exact domain( ex.- blog.bbc.com and bbc.com have the same domains )
	input_domain=tldextract.extract(url).domain+"."+tldextract.extract(url).suffix 
	for link in soup.find_all('a'):
		word =link.get('href')
		# print(word)
		if word:
			# Same website or domain calls
			if "#" in word or word[0]=="/": #div call or same domain call
				if not input_domain in urls:
					# print(input_domain)
					urls[input_domain]=1 #if first encounter with the domain
				else:
					urls[input_domain]+=1 #multiple encounters
			elif "javascript" in word:
				# javascript function calls (for domains that use modern JS frameworks to display information)
				if not "JavascriptRenderingFunctionCall" in urls:
					urls["JavascriptRenderingFunctionCall"]=1
				else:
					urls["JavascriptRenderingFunctionCall"]+=1
			else:
				# main_domain=word.split('//')[1].split('/')[0]
				main_domain=tldextract.extract(word).domain+"." +tldextract.extract(word).suffix
				# print(main_domain)
				if main_domain.split('.')[0]=='www':
					main_domain = main_domain.replace("www.","") # removing the www
				if not main_domain in urls: # maintaining the dictionary
					urls[main_domain]=1
				else:
					urls[main_domain]+=1
			count += 1
	
	for key, value in urls.items(): # printing the dictionary in a paragraph format for better readability
	 	print(key,value)
	return count	


def get_url_info(url): # function to get size of web page in bytes
    d = urllib.request.urlopen(url)
    return len(d.read())

url = input('Enter URL\n') 
print("Size of Web Page: ",get_url_info(url)," Bytes")
print("Total Number of links:",get_count_url(url))