from bs4 import BeautifulSoup
import requests
import urllib.request
import re
from urllib.parse import urlparse
import tldextract

def get_count_url(url):
	r = requests.get(url)
	soup = BeautifulSoup(r.text, "html.parser")
	count = 0
	urls={}
	# input_domain=url.split('//')[1].split('/')[0]
	input_domain=tldextract.extract(url).domain+"."+tldextract.extract(url).suffix
	for link in soup.find_all('a'):
		# print(link.get('href'))
		word =link.get('href')
		# print(word)
		if word is not None:
			# Same website or domain calls
			if "#" in word or word[0]=="/":
				if not input_domain in urls:
					# print(input_domain)
					urls[input_domain]=1
				else:
					urls[input_domain]+=1
			elif "javascript:;" in word:
				if not "JavascriptRenderingFunctionCall" in urls:
					urls["JavascriptRenderingFunctionCall"]=1
				else:
					urls["JavascriptRenderingFunctionCall"]+=1
			else:
				# main_domain=word.split('//')[1].split('/')[0]
				main_domain=tldextract.extract(word).domain+"."+tldextract.extract(word).suffix
				# print(main_domain)
				if main_domain.split('.')[0]=='www':
					main_domain = main_domain.replace("www.","")
					# print(domain)
				if not main_domain in urls:
					urls[main_domain]=1
				else:
					urls[main_domain]+=1
			# main_domain=tldextract.extract(word).domain
			# print(word)
			# print(domain)
			count += 1
	
	for key, value in urls.items():
	 	print(key,value)
	return count	


def get_url_info(url):
    d = urllib.request.urlopen(url)
    return len(d.read())

url = input('Enter URL\n') 
print("Size of Web Page: ",get_url_info(url)," Bytes")
print("Total Number of links:",get_count_url(url))