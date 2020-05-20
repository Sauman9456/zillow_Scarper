import requests
import time
from bs4 import BeautifulSoup as B
import time
import json
import pandas as pd


def link(name,filename):
	neighbour_names=[]
	hrff=[]
	dictf=[]
	jsonfile="data/"+filename+".json"
	csvfile="data/"+filename+".csv"
	url="https://www.zillow.com/"+name+"/home-values/"
	crawler(url,neighbour_names,hrff,name,dictf)
	neighbourhood(neighbour_names,hrff,dictf)
	with open(jsonfile,'a') as fp:
		json.dump(dictf, fp,indent=3)
	df = pd.DataFrame(dictf)
	df=df[['Location','zillow-value','one-year-change','one-year-forcast','market-temperature','price-sqft','median-listing-price','median-sale-price','avg-days-on-market','negative-equity','delinquincy','rent-list-price','rent-sqft']]
	df.to_csv(csvfile, index=False)


def neighbourhood(neighbour_names,hrff,dictf):
	for j,i in enumerate(hrff):
		url="https://www.zillow.com"+i
		name=neighbour_names[j]+' neighbour'
		crawler(url,neighbour_names,hrff,name,dictf)

def crawler(url,neighbour_names,hrff,name,dictf):
	header={
	    "dnt":"1",
	    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36"
	}
	re=requests.get(url,headers=header)
	base=B(re.content,'html.parser')
	data_dictionary={	
	    "Location":name,
	    "zillow-value":"Nodata",
	    "one-year-change":"Nodata",
	    "one-year-forcast":"Nodata",
	    "market-temperature":"Nodata",
	    "price-sqft":"Nodata",
	    "median-listing-price":"Nodata",
	    "median-sale-price":"Nodata",
	    "avg-days-on-market":"Nodata",
	    "negative-equity":"Nodata",
	    "delinquincy":"Nodata",
	    "rent-list-price":"Nodata",
	    "rent-sqft":"Nodata",
	}
	
	try:
	  market_temp=base.find('div',{'class':'market-temperature'})
	  temperature=market_temp.find('div',{'class':'zsg-h2'}).text
	  data_dictionary['market-temperature']=temperature
	except:
	  pass


	try:
	  outer=base.find('section',{'class':'zm-forecast-chart'})
	  content_box=outer.find('ul',{'class':'zsg-g'})
	  all_li=content_box.find('li',{'class':'zsg-lg-1-2'})
	  sp=all_li.find('span',{'class':'zsg-fineprint'})
	  sp.decompose()
	  all_li=content_box.find('li',{'class':'zsg-lg-1-2'}).text
	  temp=all_li.replace(" ","")
	  temp=temp.replace("\n","")
	  temp=temp.replace("%","")
	  data_dictionary['one-year-change']=temp
	except:
	  pass



	try:
	  outer=base.find('section',{'class':'zsg-content-section market-overview'})
	  content_box=outer.find('ul',{'class':'value-info-list'})
	  all_li=content_box.find_all('li')
	  ab=[]
	  for i in all_li:
	    temp=i.find('span',{'class':'value'}).text
	    temp=temp.replace(" ","")
	    temp=temp.replace("\n","")
	    temp=temp.replace("%","")
	    temp=temp.replace("$","")
	    ab.append(temp)
	  data_dictionary['zillow-value']=ab[0]
	  data_dictionary['one-year-forcast']=ab[1]
	  data_dictionary['median-listing-price']=ab[2]
	  data_dictionary['median-sale-price']=ab[3]
	except:
	  pass


	try:
	  outer=base.find('section',{'class':'zsg-content-section market-health'})
	  content_box=outer.find('ul',{'class':'value-info-list'})
	  all_li=content_box.find_all('li')
	  ab=[]
	  for i in all_li:
	    temp=i.find('span',{'class':'value'}).text
	    temp=temp.replace(" ","")
	    temp=temp.replace("\n","")
	    temp=temp.replace("%","")
	    ab.append(temp)
	  if len(ab)>=3:
	  	data_dictionary['avg-days-on-market']=ab[0]
	  	data_dictionary['negative-equity']=ab[1]
	  	data_dictionary['delinquincy']=ab[2]
	  else:
	  	data_dictionary['negative-equity']=ab[0]
	  	data_dictionary['delinquincy']=ab[1]
	except:
	  pass
	if data_dictionary['negative-equity']!= 'Nodata':
		data_dictionary['negative-equity']=round(float(data_dictionary['negative-equity'])/100,3)
	if data_dictionary['delinquincy'] != 'Nodata':
		data_dictionary['delinquincy']=round(float(data_dictionary['delinquincy'])/100,3)

	    
	try:
	  outer=base.find('section',{'class':'zsg-content-section listing-to-sales'})
	  content_box=outer.find('ul',{'class':'value-info-list'})
	  all_li=content_box.find_all('li')
	  ab=[]
	  for i in all_li:
	    temp=i.find('span',{'class':'value'}).text
	    temp=temp.replace(" ","")
	    temp=temp.replace("\n","")
	    temp=temp.replace("$","")
	    ab.append(temp)
	  data_dictionary['price-sqft']=ab[0]
	except:
	  pass

	try:
	  outer=base.find_all('section',{'class':'zsg-content-section region-info'})
	  content_box=outer[1].find('ul',{'class':'value-info-list'})
	  spans=content_box.find_all('span',{'class':'value'})
	  ab=[]
	  for i in spans:
	    temp=i.text
	    temp=temp.replace(" ","")
	    temp=temp.replace("\n","")
	    temp=temp.replace("$","")
	    ab.append(temp)
	  data_dictionary['rent-list-price']=ab[1]
	  data_dictionary['rent-sqft']=ab[2]
	except:
	  pass 
	print(data_dictionary)
	

	dictf.append(data_dictionary)
	try:
	  nearby=base.find('section',{'class':'zsg-content-section nearby-regions'})
	  neighbourhoods=nearby.find('div',{'class':'zsg-content-section'}).text.split()
	  if 'Neighborhoods' in neighbourhoods:
		  tables=nearby.find_all('table')
		  for k in tables:
		    at=k.find_all('a')
		    for p in at:
		      n_n=p.text
		      n_l=p['href']
		      if n_n not in neighbour_names and n_l not in hrff:
		      	neighbour_names.append(n_n)
		      	hrff.append(n_l)
	except:
	  pass

	
print("Write the location names, separated by comma(,):")
Locations = list(map(str, input().split(',')))
for i in range(len(Locations)):
	filename="zillowInsight-"+Locations[i]
	link(Locations[i],filename)