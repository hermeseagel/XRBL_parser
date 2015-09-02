#import numpy
#URL=	http://mops.twse.com.tw/mops/web/t164sb02
#EXAMPLE POST BODY :encodeURIComponent=1&step=1&firstin=true&MAR_KIND=sii&CODE=24&SYEAR=2014&SSEASON=04&REPORT_ID=C
#
import os
import re
import pycurl
from multiprocessing import Process, Queue
import zipfile
from urllib.parse import urlencode
#try:
from io import BytesIO
#except ImportError:
#from StringIO import StringIO as BytesIO
#import cStringIO
#this Taiwan_company_url_gen to Genernation Static url to Quenue 
def Taiwan_company_postdata_gen(year_q):
	#/* 上市、上櫃、興櫃、公開發行 */
	market_type=['sii','otc','rotc','pub']
	industry_origin=list(range(1,32))
	industry_origin.append(80)
	industry_origin.append(91)
	industry_origin.append(97)
	industry_origin.append(98)
	industry_origin.append(99)
	#個別財報A、個體財報B、合併報表C
	statment_type=['A','B','C']
	#old using get version 
	#static_url="http://mops.twse.com.tw/server-java/FileDownLoad?firstin=true&step=9&fileName="
	#below is new for postdata

	static_url="http://mops.twse.com.tw/server-java/FileDownLoad"
	static_dir="&filePath=/home/html/nas/xbrl/"
	postdata_list = []
	for market in market_type:
		for industry_no in industry_origin:
			industry=str(industry_no)
			for statment in statment_type:
				filename=year_q+"-"+market+"-"+industry+'-'+statment+'.zip'
				pathfile='/Users/Hermes/Python_script/'+filename
				post_data='firstin=true&step=9&fileName='+filename+'&filePath=%2Fhome%2Fhtml%2Fnas%2Fifrs%2F'+year_q[:4]+'%2F'
				#print(post_data)
				postdata_list.append(post_data)
	return postdata_list
'''
				with open(pathfile,"wb") as file:
					connection=pycurl.Curl()
					connection.setopt(connection.URL,static_url)
					connection.setopt(connection.WRITEDATA,file)
					connection.perform()
					connection.close()

'''
			

def get_xbrl_zipfile(postbody):
	static_url="http://mops.twse.com.tw/server-java/FileDownLoad"
	static_dir="&filePath=/home/html/nas/xbrl/"
	filetemp=postbody.split('=')[3]
	filename=filetemp.split('&')[0]
	pathfile='/home/xrbl/TW/'+filename
	return pathfile
		#with open(pathfile,"wb") as file:
			#connection=pycurl.Curl()
			#connection.setopt(connection.URL,static_url)
			#connection.setopt(connection.WRITEDATA,file)
			#connection.perform()
			#connection.close()
def work(postbody):
	info=get_xbrl_zipfile(postbody)
	#print (str(os.getpid()) + '(get):' + info)
	
	
			
#if __name__ == '__main__':
#	for postbody in Taiwan_company_postdata_gen('2014-02'):
		#print(postbody)
		#proc1=Process(target=work,args=(postbody,))
		#proc1.start()
	
			

#print(Taiwan_company_url_gen('2014-02'))
#print(q1.qsize)
#filetemp='firstin=true&step=9&fileName=2014-02-pub-99-B.zip&filePath=%2Fhome%2Fhtml%2Fnas%2Fifrs%2F2014%2F'.split('=')[3]
#filename=filetemp.split('&')[0]
#print(filename)
#zzfile=zipfile.is_zipfile('/Users/Hermes/Python_script/xbrl_zip/2014-04-sii-24-C.zip')
#print(zzfile)
#if __name__ == '__main__':
#	p = Process(target=workq, args=(q1,))
#	p.start()
#	print(q1.get)
#	p.join()
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


filename='2014-04-sii-24-C.zip'
static_url="http://mops.twse.com.tw/server-java/FileDownLoad"
#post_data='firstin=true&step=9&fileName='+filename+'&filePath=%2Fhome%2Fhtml%2Fnas%2Fifrs%2F2014%2F'
post_data='firstin=true&step=9&fileName=2014-02-sii-06-C.zip&filePath=%2Fhome%2Fhtml%2Fnas%2Fifrs%2F2014%2F'
#post_data='firstin=true&step=9&fileName=2014-03-sii-02-C.zip&filePath=%2Fhome%2Fhtml%2Fnas%2Fifrs%2F2014%2F'
#post_data='firstin=true&step=9&fileName=2014-02-pub-20-A.zip&filePath=%2Fhome%2Fhtml%2Fnas%2Fifrs%2F2014%2F'
#post_data='firstin=true&step=9&fileName=2014-02-pub-23-A.zip&filePath=%2Fhome%2Fhtml%2Fnas%2Fifrs%2F2014%2F'
#post_data="firstin=true&step=9&fileName=2014-02-rotc-17-B.zip&filePath=%2Fhome%2Fhtml%2Fnas%2Fifrs%2F2014%2F"
connection=pycurl.Curl()
connection.setopt(connection.URL,static_url)
pathfile='/Users/Hermes/Python_script/'+filename
#f=open(pathfile,"wb")
buffer = BytesIO()
#with open('/Users/Hermes/twxbrl/2014-03-sii-02-C2.zip',"wb") as file:
connection.setopt(connection.USERAGENT,u'Mozilla/5.0')
#postdata look like this 'firstin=true&step=9&fileName=2014-04-sii-24-C.zip&filePath=%2Fhome%2Fhtml%2Fnas%2Fifrs%2F2014%2F'

connection.setopt(connection.POSTFIELDS,post_data)
	# Set our header function.
connection.setopt(connection.HEADERFUNCTION, header_function)
connection.setopt(connection.WRITEDATA,buffer)
connection.setopt(connection.VERBOSE, True)
	#if 
	#re.search('< Content-type: text/html',s)
	#if bool(a)==True:
	#	print(OK)
	#else:
	#	pass
#	connection.setopt(connection.WRITEDATA,file)
connection.perform()
connection.close()
print(headers)
if  'content-type' in headers:
	content_type = headers['content-type'].lower()
	match=re.search('application/x-zip-compressed',content_type) 
	if match:
		print(headers['content-disposition'])
		with open('/Users/Hermes/twxbrl/2014-02-pub-98-C.zip',"wb") as file:
			file.write(buffer.getvalue())
