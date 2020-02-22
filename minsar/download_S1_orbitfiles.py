#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#~~
#the url as change so update
#Edit by wangjing on August 2 2018
##############################################

import os
import os.path
import datetime
import glob
import requests

from bs4 import BeautifulSoup
import re
import time
def downOrbitFile(workdir,year,month,yesmonth,yesday,sensor):

	#https://qc.sentinel1.eo.esa.int/aux_poeorb/?validity_start=2018&validity_start=2018-02&validity_start=2018-02-16..2018-02-16&sentinel1__mission=S1A
	if sensor=='S1A':
		base_url='https://qc.sentinel1.eo.esa.int/aux_poeorb/?validity_start={year}&validity_start={yesmonth}&validity_start={yesday}..{yesday}&sentinel1__mission=S1A'.\
				format(year = year,yesmonth=yesmonth,yesday=yesday)
		print(('the base down url is %s' %base_url))
		
		soup=BeautifulSoup(urlopen(base_url).text,'lxml')
		page=soup.find_all('a',href=re.compile('.EOF'))
		
		#down aux_poeorb orbits EOF file from the url
		#http://aux.sentinel1.eo.esa.int/POEORB/2018/02/25/{name}
		url_down_template=str(page).split('\"')[1]
		print(('now the orbit url is \n %s' %url_down_template))
		
		#orbit file name
		orbitname=url_down_template.split('/')[-1]
		print(('now download the orbit file,please wait a few time <0.0> %s' %orbitname))
	else:
		base_url='https://qc.sentinel1.eo.esa.int/aux_poeorb/?validity_start={year}&validity_start={yesmonth}&validity_start={yesday}..{yesday}&sentinel1__mission=S1B'.\
				format(year = year,yesmonth=yesmonth,yesday=yesday)
		print(('the base down url is %s' %base_url))
		
		soup=BeautifulSoup(urlopen(base_url).text,'lxml')
		page=soup.find_all('a',href=re.compile('.EOF'))
		
		#down aux_poeorb orbits EOF file from the url
		#http://aux.sentinel1.eo.esa.int/POEORB/2018/02/25/{name}
		url_down_template=str(page).split('\"')[1]
		print(('now the orbit url is \n %s' %url_down_template))
		
		#orbit file name
		orbitname=url_down_template.split('/')[-1]
		print(('now download the orbit file,please wait a few time <0.0> %s' %orbitname))

		#判断200 响应码
	orbitpage=urlopen(url_down_template)
	if orbitpage.status_code==200:
		#down directory
		print(("download path is:%s" %workdir))
		down_EOF_path=os.path.join(workdir,orbitname)
		with open(down_EOF_path,'wb') as f:
			f.write(orbitpage.content)
	else:
		print(('orbit file can not be download correctly. please debug'))
		print((orbitpage.status_code))

def urlopen(url):
	from requests.packages.urllib3.exceptions import InsecureRequestWarning
	# 禁用安全请求警告
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
	# SSL: CERTIFICATE_VERIFY_FAILED
	r = requests.get(url, verify=False)
	urlcode=r.status_code
	if urlcode==200:
		return r
	else:
		print((urlcode))

def py_S1_orbit(scene_id,workdir,sensor):
	"""
	download the orbit file
	"""
	# step 1: download OPOD
	year = int(scene_id[0:4])
	month = int(scene_id[4:6])
	day = int(scene_id[6:8])

	# get the yesday orbit date
	d0 = datetime.datetime(int(year), int(month), int(day))
	print(('the orbit file day is'))
	print((d0))
	delta = datetime.timedelta(days=1)
	d1 = d0 - delta
	print(('the orbit yesday is '))
	print((d1))
	
	month=datetime.datetime.strftime(d1,'%m')
	year=datetime.datetime.strftime(d1,'%Y')
	yesmonth=datetime.datetime.strftime(d1,'%Y-%m')
	yesday=datetime.datetime.strftime(d1, '%Y-%m-%d')
	print((month,year,yesmonth,yesday))
	print(('the  orbit data get yesday :',yesday))
	downOrbitFile(workdir,year,month,yesmonth,yesday,sensor)

#main method
def autoDown_S1_Orbitfile(datadir,downdir):
	os.chdir(datadir)
	ziplist=glob.glob(r'*.zip')

	os.chdir(downdir)	
	workdir=os.path.join(downdir,'orbits')
	
	start=time.time()
	datelist=[]
	for zipfile in ziplist:
		date=zipfile[17:25]
		sensor=zipfile[0:3]
		orbitdir=os.path.join(downdir,date)
		orbit_files = glob.glob(os.path.join(orbitdir,  sensor + '*.EOF'))
		if len(orbit_files) == 0:
			print('we down the orbitfile to the dir %s' %orbitdir)
			if not os.path.isdir(orbitdir) :
				os.makedirs(orbitdir)
			py_S1_orbit(date,orbitdir,sensor)
		datelist.append(date)
	print(('the datelist is :'))
	print((datelist))
	end=time.time()
	print(('***********************************************'))
	print(("Run autoDown_S1_Orbitfile.py process use time:%f s" % (end-start)))
	print(('*****END!! finish down the all orbit files*****'))	

if __name__ == '__main__':
	import sys 
	if (len(sys.argv) < 2 or len(sys.argv) > 4):
		print(('*****************************************************************'))
		print(('*                 auto down the S1 orbitfile                    *'))
		print(('*   the base url is https://qc.sentinel1.eo.esa.int/aux_resorb  *'))
		print(('*****************************************************************'))
		print(('      autoDown_S1_Orbitfile.py <datadir> <downdir>               '))
		print(('  <datadir>                    the directory of the SLC files    '))
		print(('  <downdir>                    the directory of the orbitfile    '))
		sys.exit()
	
	datadir=sys.argv[1]
	downdir=sys.argv[2]
	if not(os.path.exists(downdir)):
		raise Exception('%s does not exist:' %downdir)
		
	autoDown_S1_Orbitfile(datadir,downdir)