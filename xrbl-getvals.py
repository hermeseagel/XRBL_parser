import io,re,collections,pymongo,datetime
import lxml.etree as etree
#fs='/Users/Hermes/Downloads/tifrs-fr0-m1-ci-cr-2330-2013Q3.xml'
fs='/Users/Hermes/Downloads/CN_SZ_000001_GB0710_20131023.xml'
root=etree.parse(fs).getroot()
def match(source,pattern):
	matchobj=re.compile(pattern)
	result=matchobj.findall(source)
	if len(result) > 0:
		return True
	else:
		return False
def xmlparser(filename):
	global dicts
	dicts={}
	count=collections.Counter()
	for i in root:
		item=i.tag.split('}')[1] 
		if item not in dicts.keys() and i.text != None and item != 'schemaRef':
			if item=='context' or  item=='object':
				attribs=i.attrib.values()
				texta=attribs[0]
				dicts[item]=texta
			else:
				print(item,count[item])
				dicts[item]=i.text
				count[item] +=1
		elif item in dicts.keys() and i.text != None and item != 'schemaRef':
			if item=='context' or  item=='object' :
				attribs=i.attrib.values()
				count[item] +=1 
				texta=attribs[0]
				anum=count[item]
				astr=item+str(anum)
				dicts[astr]=texta
			else:
	#			print(item,count[item])
				count[item] +=1 
				anum=count[item]
				astr=item+str(anum)
				dicts[astr]=i.text 
		#else: 
		#	print(item,'ll')
		#	dicts[i.tag]=i.text
	return dicts
def mongoconnect(dbdest,db_name,collection_name,post):
		conn=pymongo.Connection(dbdest)
		db=conn[db_name]
		#collec=db.create_collection(collection_name)
		db.collection_name.insert(post)
		

list=xmlparser(fs)
#print(list)

mongoconnect('10.37.129.4','hermes','haha',list)

		
		