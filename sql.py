# coding:utf-8
import os
import requests
import json
import threading
from time import sleep

file = open("url.txt")
def sql(url) :
	try:
		r = requests.get("http://127.0.0.1:8775/task/new")
		taskid= r.json()['taskid']
		r = requests.post('http://127.0.0.1:8775/scan/'+taskid+'/start', data=json.dumps({'url': url}), headers={'content-type': 'application/json'})
		sleep(5)
		r = requests.get('http://127.0.0.1:8775/scan/'+taskid+'/status')
		running_status = r.json()['status']
		while running_status == "running":
			if running_status == "running":
				sleep(5)
				r = requests.get('http://127.0.0.1:8775/scan/'+taskid+'/status')
				running_status = r.json()['status']
			elif running_status == "terminated":
				break
		r = requests.get('http://127.0.0.1:8775/scan/'+taskid+'/data')
		requests.get('http://127.0.0.1:8775/scan/' + taskid + '/stop')
		requests.get('http://127.0.0.1:8775/scan/'+taskid+'/delete')
		if r.json()['data']:
			print " [√]: " + url
		else:
			print " [x]: " + url
	except requests.ConnectionError:
		print '无法连接到SQLMAPAPI服务,请在SQLMAP根目录下运行python sqlmapapi.py -s 来启动'
for line in file:
	threads = []
	url = line.strip()
	threads.append(threading.Thread(target=sql,args=(url,)))
	for t in threads:
		t.setDaemon(True)
		t.start()
		t.join()