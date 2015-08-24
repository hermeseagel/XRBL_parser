#import numpy
#URL=	http://mops.twse.com.tw/mops/web/t164sb02
#EXAMPLE POST BODY :encodeURIComponent=1&step=1&firstin=true&MAR_KIND=sii&CODE=24&SYEAR=2014&SSEASON=04&REPORT_ID=C
#
import pycurl
from urllib.parse import urlencode
#try:
from io import BytesIO
#except ImportError:
#from StringIO import StringIO as BytesIO
#import cStringIO
def Taiwan_company_url_gen(year_q):
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
	url = ''
	for market in market_type:
		for industry_no in industry_origin:
			industry=str(industry_no)
			for statment in statment_type:
				filename=year_q+"-"+market+"-"+industry+'-'+statment+'.zip'
				url=static_url+filename+static_dir+year_q[:4]+'/'
				
				return url
filename='2014-04-sii-24-C.zip'
static_url="http://mops.twse.com.tw/server-java/FileDownLoad"
post_data='firstin=true&step=9&fileName='+filename+'&filePath=%2Fhome%2Fhtml%2Fnas%2Fifrs%2F2014%2F'
connection=pycurl.Curl()
connection.setopt(connection.URL,static_url)
pathfile='/Users/Hermes/Python_script/'+filename
f=open(pathfile,"wb")
#postdata look like this 'firstin=true&step=9&fileName=2014-04-sii-24-C.zip&filePath=%2Fhome%2Fhtml%2Fnas%2Fifrs%2F2014%2F'
connection.setopt(connection.POSTFIELDS,post_data)
#connection.setopt(connection.WRITEDATA,buffer)
#connection.setopt(connection.VERBOSE, True)
connection.setopt(connection.WRITEDATA,f)
connection.perform()
connection.close()
f.close()