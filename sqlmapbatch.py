#coding: utf-8
import os
import requests
import json
import threading
from time import ctime, sleep, time

def sql(url): 
	try: 
		r = requests.get("http://127.0.0.1:8775/task/new")
		taskid = r.json()['taskid']
		print taskid
		r = requests.post('http://127.0.0.1:8775/scan/' + taskid + '/start', data = json.dumps({'url': url}), headers = {'content-type': 'application/json'})
		start = time()
		while  True:
			sleep(3)
			r = requests.get('http://127.0.0.1:8775/scan/' + taskid + '/status')
			if r.json()['status'] == 'terminated': break
			end = time()
			if end-start > 4 : print end-start ;break
		r = requests.get('http://127.0.0.1:8775/scan/' + taskid + '/data')
		requests.get('http://127.0.0.1:8775/scan/' + taskid + '/stop')
		requests.get('http://127.0.0.1:8775/scan/' + taskid + '/delete')
		if r.json()['data']:
			# print r.json()['data'] 
			print u" [√]: " + url + " " + ctime()
		else :
			# print r.json()
			print u" [x]: " + url + " " + ctime()
	except requests.ConnectionError:
		print '无法连接到SQLMAPAPI服务,请在SQLMAP根目录下运行python sqlmapapi.py -s 来启动'

print "start"

file = open("url.txt")
threads = []
for line in file:
	url = line.strip()
	threads.append(threading.Thread(target = sql, args = (url, )))
for t in threads:
	t.setDaemon(True)
	t.start()
	t.join()

