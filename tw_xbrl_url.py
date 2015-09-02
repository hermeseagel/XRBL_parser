#import numpy
#URL=	http://mops.twse.com.tw/mops/web/t164sb02
#EXAMPLE POST BODY :encodeURIComponent=1&step=1&firstin=true&MAR_KIND=sii&CODE=24&SYEAR=2014&SSEASON=04&REPORT_ID=C
#
import os,sys,re
import configparser
import pycurl
import logging
from io import BytesIO
from multiprocessing import Process, Queue, Pool,cpu_count,current_process
import zipfile
from urllib.parse import urlencode
import time 
#try:
from io import BytesIO
#except ImportError:
#from StringIO import StringIO as BytesIO
#import cStringIO
#this Taiwan_company_url_gen to Genernation Static url to Quenue 
#v2 using Quenue to make sure no duplicate 
queue1=Queue()
def Taiwan_company_postdata_gen(year_q):
	#/* 上市(sii)、上櫃(otc)、興櫃(rotc)、公開發行(pub) *
	#But just sii and otc have xbrl file
	#/
	market_type=['sii','otc']
	industry_origin=list()
	for num in range(1,32):
		num_str=str(num).zfill(2)
		industry_origin.append(num_str)
	industry_origin.append(80)
	industry_origin.append(91)
	industry_origin.append(97)
	industry_origin.append(98)
	industry_origin.append(99)
	#個別財報A、個體財報B、(前二種報表不存在）,合併報表C
	statment_type=['C']
	#old using get version 
	#static_url="http://mops.twse.com.tw/server-java/FileDownLoad?firstin=true&step=9&fileName="
	#below is new for postdata

	static_url="http://mops.twse.com.tw/server-java/FileDownLoad"
	static_dir="&filePath=/home/html/nas/xbrl/"
	static_dir2="&filePath=/home/html/nas/ifrs/"
	postdata_list = []
	for market in market_type:
		for industry_no in industry_origin:
			industry=str(industry_no)
			for statment in statment_type:
				filename=year_q+"-"+market+"-"+industry+'-'+statment+'.zip'
				pathfile='/Users/Hermes/Python_script/'+filename
				post_data='firstin=true&step=9&fileName='+filename+'&filePath=%2Fhome%2Fhtml%2Fnas%2Fifrs%2F'+year_q[:4]+'%2F'
				#print(post_data)
				#v1 using list but will generation 100 Processes
				#postdata_list.append(post_data)
				queue1.put(post_data)
	return queue1
headers = {}
def header_function(header_line):
# HTTP standard specifies that headers are encoded in iso-8859-1.
# On Python 2, decoding step can be skipped.
# On Python 3, decoding step is required.
	header_line = header_line.decode('iso-8859-1')

# Header lines include the first status line (HTTP/1.x ...).
# We are going to ignore all lines that don't have a colon in them.
# This will botch headers that are split on multiple lines...
	if ':' not in header_line:
		return

# Break the header line into header name and value.
	name, value = header_line.split(':', 1)

# Remove whitespace that may be present.
# Header lines include the trailing newline, and there may be whitespace
# around the colon.
	name = name.strip()
	value = value.strip()
# Header names are case insensitive.
# Lowercase name here.
	name = name.lower()
# Now we can actually record the header name and value.
	headers[name] = value

			

def get_xbrl_zipfile(postbody):
	static_url="http://mops.twse.com.tw/server-java/FileDownLoad"
	static_dir="&filePath=/home/html/nas/xbrl/"
	filetemp=postbody.split('=')[3]
	filename=filetemp.split('&')[0]
	config=configparser.ConfigParser()
	config.read('xbrl.conf')
	savepath=config['twxbrl']['savepath']
	pathfile=savepath+'/'+filename
	print(current_process().name)
	print(postbody)
	buffer = BytesIO()
	connection=pycurl.Curl()
	connection.setopt(connection.URL,static_url)
	connection.setopt(connection.POSTFIELDS,postbody)
	connection.setopt(connection.HEADERFUNCTION, header_function)
	connection.setopt(connection.WRITEDATA,buffer)
	connection.perform()
	connection.close()
	logfile=logging.basicConfig(filename='xrbl-error.log')
	if  'content-type' in headers:
		content_type = headers['content-type'].lower()
		match=re.search('application/x-zip-compressed',content_type) 
		if match:
		#	print(headers['content-disposition'])
			with open(pathfile,"wb") as file:
				file.write(buffer.getvalue())
		else:
			logging.warning('Warn_postdata',postbody)
	#check download file is zip files 
	#if zipfile.is_zipfile(pathfile) != True:
	#	print(pathfile,' broken ')
	#else:
	#	print('OK')
def tw_xbrl_download(postbody):
	get_xbrl_zipfile(postbody)
	
def start_process():
	#print('Starting',current_process().name)
	pass
			
if __name__ == '__main__':
	#v1 using list to pass 
	#for postbody in Taiwan_company_postdata_gen('2014-02'):
		#print(postbody)
	#	proc1=Process(target=work,args=(postbody,))
	#	proc1.start()
	#how to use this script by http  or  command line 
	#1.http must to do a interface to recvice 
	config=configparser.ConfigParser()
	config.read('xbrl.conf')
	savepath=config['twxbrl']['savepath']
	#print(savepath)
	#year_q=sys.argv[1]
	year_q='2014-03'
	match=re.match("^\d\d\d\d(\-)\d\d$",year_q)
	if match:
		Taiwan_company_postdata_gen(year_q)
	else:
		print('wrong')
	
	default_dir=savepath+year_q[:4]
	#if os.path.isdir(default_dir)== False :
	#	os.mkdir(default_dir)
	#using process Pool
	#procpool=Pool(processes=cpu_count()*2,initializer=start_process)
	#tw xbrl can't use Multiprocess but I will keep it for example 
	#each download must wait for sometime  to download next 
	while queue1.empty() ==  False :
		a=queue1.get()
		#proc=Process(target=tw_xbrl_download,args=(queue1.get(),))
		#proc.start()
		#procpool.apply_async(tw_xbrl_download,args=(queue1.get(),))
		tw_xbrl_download(a)
		time.sleep('20')
