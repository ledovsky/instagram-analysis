import requests
import urllib2 
import html5lib
from bs4 import BeautifulSoup
import time
# import psycopg2
import json
import sys
import csv



def getId (name):

	id = "000"
	header = ['Cache-Control', 'Accept', 'User-Agent', 'Referrer', 'Accept-Encoding', 'Accept-Language']
	value = ['no-cache','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 39.0.2171.95 Safari/537.36', 'https://www.google.com/', 'gzip, deflate, sdch', 'ru-RU,en-US,en;q=0.8']
	custom_headers={}
	for i in range(1,len(header)):
		custom_headers[header[i]] = value[i]
	
	r = requests.get("https://api.instagram.com/v1/users/search?q="+name+"&client_id=e467b070519f452abe8e687393081b96", headers=custom_headers)
	data = json.loads(r.text)
	
	for i in range(0,len(data['data'])):
		if data['data'][i]['username'] == name:
			id = data['data'][0]['id']
			break
			
	if id == "000":
		print "Account is not found"
		sys.exit()
		
	return id

def getSubscribers(name, cursor="", key = "1688942629.b59fbe4.550682dbcb9347438e411e5188f08337"):

	t0 = time.time()
	id = getId (name)
	counter = 0
	
	header = ['Cache-Control', 'Accept', 'User-Agent', 'Referrer', 'Accept-Encoding', 'Accept-Language']
	value = ['no-cache','text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/ 39.0.2171.95 Safari/537.36', 'https://www.google.com/', 'gzip, deflate, sdch', 'ru-RU,en-US,en;q=0.8']
	custom_headers={}
	for i in range(1,len(header)):
		custom_headers[header[i]] = value[i]
		
	cursor = ""
	q = 0
	
	add = [['username','id','full_name']]
	
	for c in range(0,9999999):
		r = requests.get("https://api.instagram.com/v1/users/"+id+"/followed-by?access_token="+key+"&cursor="+cursor, headers=custom_headers)
		data = json.loads(r.text)
		
		for i in range (0,len(data['data'])):
			add.append([(data['data'][i]['username']).encode('utf-8'),data['data'][i]['id'],(data['data'][i]['full_name']).encode('utf-8')])
			q = q + 1
		print "------------- \n" + str(q)
		t1 = time.time()
		print cursor
		print "Code execution time is:" , time.strftime("%H:%M:%S", time.gmtime(t1-t0))
				
		if len(data['pagination']) <> 0:
			cursor = data['pagination']['next_cursor']
		else:
			c = csv.writer(open(name+"_followers.csv", "wb"), delimiter=',')
			c.writerows (add)
			break

	print "Total followers scanned:" + str(q)
