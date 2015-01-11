from flask import Flask, request, render_template, url_for, Markup
import HTMLParser
import json
import requests
import TorBE
import Translate
import urllib

API_KEY = 'AIzaSyD7KOKsTnSnOfQO5yO4dPdGTDmipxKvbh4'

app = Flask(__name__, static_url_path='/static')

translated_results = {}

country_codes = ['US', 'UK', 'RU', 'AR']

@app.route('/')
def respond_to_request():
	return construct_carousel()


	search_term     = request.args.get('search_term')
	country_codes   = request.args.get('country_code')

	news = {}
	if(country_codes):
		for country in country_codes:
				translation_result = Translate.translate_into_local_language(search_term, country)
				print json.dumps(translation_result, indent = 4, separators=(',', ': '))

				translated_search_term  = translation_result['data']['translations'][0]['translatedText']
				url = 'https://ajax.googleapis.com/ajax/services/search/news?v=1.0&q=%s' % translated_search_term
				news_dict = TorBE.make_request_thru_tor(url, country)
				results = []
				for result in news_dict['responseData']['results']:
					results.append({'title': result['title'],'url':result['url'], 'content':result['content']})
					
					translated_title   = 'https://www.googleapis.com/language/translate/v2?key=%s&q=%s&source=en&target=%s' % (API_KEY, results[result['title']], country)
					translated_url     = 'https://www.googleapis.com/language/translate/v2?key=%s&q=%s&source=en&target=%s' % (API_KEY, results[result['url']], country)
					translated_snippet = 'https://www.googleapis.com/language/translate/v2?key=%s&q=%s&source=en&target=%s' % (API_KEY, results[result['content']], country)

					translated_results.append({'title': result[translated_title], 'url': result[translated_url], 'content': result[translated_snippet]})

				news[country] = translated_results

def construct_carousel(name=None):
	countrycode_to_name = {
	"AL":"ALBANIA",
	"DZ":"ALGERIA",
	"AR":"ARGENTINA",
	"AU":"AUSTRALIA",
	"AT":"AUSTRIA",
	"BH":"BAHRAIN",
	"BY":"BELARUS",
	"BE":"BELGIUM",
	"BZ":"BELIZE",
	"BO":"PLURINATIONAL STATE OF BOLIVIA",
	"BR":"BRAZIL",
	"BN":"BRUNEI DARUSSALAM",
	"BG":"BULGARIA",
	"CA":"CANADA",
	"CL":"CHILE",
	"CN":"CHINA",
	"CO":"COLOMBIA",
	"CR":"COSTA RICA",
	"HR":"CROATIA",
	"CZ":"CZECH REPUBLIC",
	"DK":"DENMARK",
	"DO":"DOMINICAN REPUBLIC",
	"EC":"ECUADOR",
	"EG":"EGYPT",
	"SV":"EL SALVADOR",
	"EE":"ESTONIA",
	"FI":"FINLAND",
	"FR":"FRANCE",
	"GE":"GEORGIA",
	"DE":"GERMANY",
	"GR":"GREECE",
	"GT":"GUATEMALA",
	"HN":"HONDURAS",
	"HK":"HONG KONG",
	"HU":"HUNGARY",
	"IS":"ICELAND",
	"IN":"INDIA",
	"ID":"INDONESIA",
	"IR":"ISLAMIC REPUBLIC OF IRAN",
	"IQ":"IRAQ",
	"IE":"IRELAND",
	"IT":"ITALY",
	"JM":"JAMAICA",
	"JP":"JAPAN",
	"JO":"JORDAN",
	"KE":"KENYA",
	"KR":"KOREA REPUBLIC OF",
	"KW":"KUWAIT",
	"LV":"LATVIA",
	"LB":"LEBANON",
	"LY":"LIBYA",
	"LI":"LIECHTENSTEIN",
	"LT":"LITHUANIA",
	"LU":"LUXEMBOURG",
	"MO":"MACAO",
	"MK":"THE FORMER YUGOSLAV REPUBLIC OF MACEDONIA",
	"MY":"MALAYSIA",
	"MX":"MEXICO",
	"MC":"MONACO",
	"MA":"MOROCCO",
	"NL":"NETHERLANDS",
	"NZ":"NEW ZEALAND",
	"NI":"NICARAGUA",
	"OM":"OMAN",
	"PK":"PAKISTAN",
	"PA":"PANAMA",
	"PY":"PARAGUAY",
	"PE":"PERU",
	"PH":"PHILIPPINES",
	"PL":"POLAND",
	"PT":"PORTUGAL",
	"PR":"PUERTO RICO",
	"QA":"QATAR",
	"RO":"ROMANIA",
	"RU":"RUSSIAN FEDERATION",
	"SA":"SAUDI ARABIA",
	"SG":"SINGAPORE",
	"SK":"SLOVAKIA",
	"SI":"SLOVENIA",
	"ZA":"SOUTH AFRICA",
	"ES":"SPAIN",
	"SE":"SWEDEN",
	"CH":"SWITZERLAND",
	"SY":"SYRIAN ARAB REPUBLIC",
	"TW":"TAIWAN PROVINCE OF CHINA",
	"TH":"THAILAND",
	"TT":"TRINIDAD AND TOBAGO",
	"TN":"TUNISIA",
	"TR":"TURKEY",
	"UA":"UKRAINE",
	"AE":"UNITED ARAB EMIRATES",
	"GB":"UNITED KINGDOM",
	"US":"UNITED STATES",
	"UY":"URUGUAY",
	"VE":"VENEZUELA BOLIVARIAN REPUBLIC OF",
	"YE":"YEMEN"
	}

	print countrycode_to_name["YE"]
	title = []
	url = []
	content = []
	countries = []
	countryname = []
	news = {'YE':[{'title': 'Elvis Presley&#39;s first record, &#39;My <b>Happiness</b>, auctions for $300K','url': 'http%3A%2F%2Fwww.tennessean.com%2Fstory%2Fentertainment%2Fmusic%2F2015%2F01%2F09%2Felvis-presleys-first-record-happiness-auctions%2F21497915%2F','content': 'Lorisa Hilburn, right, and relative Dianna Brookins, left, smile after an acetate recording of \u201cMy <b>Happiness</b>,\u201d the first song Elvis Presley ever recorded, was auctioned for a $300,000 on Thursday, Jan. 8, 2015, in Memphis. The record sat in a safe <b>...</b>'},{'title': '6 Toxic People Who May Be Sabotaging Your <b>Happiness</b>','url': 'http%3A%2F%2Fwww.huffingtonpost.com%2F2015%2F01%2F09%2Ftoxic-relationships-get-rid-of-them_n_6397200.html','content': 'I once read a quote by motivational speaker Jim Rohn that blatantly stated, &quot;You&#39;re the average of the five people you spend the most time with.&quot; It&#39;s an alarming thought -- shouldn&#39;t you be your own person, and not the sum of those around you? However&nbsp;...'}],'US':[{'title': 'Elvis Presley&#39;s first record, &#39;My <b>Happiness</b>, auctions for $300K','url': 'http%3A%2F%2Fwww.tennessean.com%2Fstory%2Fentertainment%2Fmusic%2F2015%2F01%2F09%2Felvis-presleys-first-record-happiness-auctions%2F21497915%2F','content': 'Lorisa Hilburn, right, and relative Dianna Brookins, left, smile after an acetate recording of \u201cMy <b>Happiness</b>,\u201d the first song Elvis Presley ever recorded, was auctioned for a$300,000 on Thursday, Jan. 8, 2015, in Memphis. The record sat in a safe <b>...</b>'},{'title': '6 Toxic People Who May Be Sabotaging Your <b>Happiness</b>','url': 'http%3A%2F%2Fwww.huffingtonpost.com%2F2015%2F01%2F09%2Ftoxic-relationships-get-rid-of-them_n_6397200.html','content': 'I once read a quote by motivational speaker Jim Rohn that blatantly stated, &quot;You&#39;re the average of the five people you spend the most time with.&quot; It&#39;s an alarming thought -- shouldn&#39;t you be your own person, and not the sum of those around you? However&nbsp;...'}], 'RU':[{'title': 'Elvis Presley&#39;s first record, &#39;My <b>Happiness</b>, auctions for $300K','url': 'http%3A%2F%2Fwww.tennessean.com%2Fstory%2Fentertainment%2Fmusic%2F2015%2F01%2F09%2Felvis-presleys-first-record-happiness-auctions%2F21497915%2F','content': 'Lorisa Hilburn, right, and relative Dianna Brookins, left, smile after an acetate recording of \u201cMy <b>Happiness</b>,\u201d the first song Elvis Presley ever recorded, was auctioned for a $300,000 on Thursday, Jan. 8, 2015, in Memphis. The record sat in a safe <b>...</b>'},{'title': '6 Toxic People Who May Be Sabotaging Your <b>Happiness</b>','url': 'http%3A%2F%2Fwww.huffingtonpost.com%2F2015%2F01%2F09%2Ftoxic-relationships-get-rid-of-them_n_6397200.html','content': 'I once read a quote by motivational speaker Jim Rohn that blatantly stated, &quot;You&#39;re the average of the five people you spend the most time with.&quot; It&#39;s an alarming thought -- shouldn&#39;t you be your own person, and not the sum of those around you? However&nbsp;...'}],'AR':[{'title': 'Elvis Presley&#39;s first record, &#39;My <b>Happiness</b>, auctions for $300K','url': 'http%3A%2F%2Fwww.tennessean.com%2Fstory%2Fentertainment%2Fmusic%2F2015%2F01%2F09%2Felvis-presleys-first-record-happiness-auctions%2F21497915%2F','content': 'Lorisa Hilburn, right, and relative Dianna Brookins, left, smile after an acetate recording of \u201cMy <b>Happiness</b>,\u201d the first song Elvis Presley ever recorded, was auctioned for a $300,000 on Thursday, Jan. 8, 2015, in Memphis. The record sat in a safe <b>...</b>'},{'title': '6 Toxic People Who May Be Sabotaging Your <b>Happiness</b>','url': 'http%3A%2F%2Fwww.huffingtonpost.com%2F2015%2F01%2F09%2Ftoxic-relationships-get-rid-of-them_n_6397200.html','content': 'I once read a quote by motivational speaker Jim Rohn that blatantly stated, &quot;You&#39;re the average of the five people you spend the most time with.&quot; It&#39;s an alarming thought -- shouldn&#39;t you be your own person, and not the sum of those around you? However&nbsp;...'}]}
	print Markup((news['YE'][0]['title']).decode('unicode-escape'))
	for country in news.keys(): #for every news item...
		countries.append(country)
		countryname.append(countrycode_to_name[country])
		for story in news[country]:
			title.append(Markup((story['title']).decode('unicode-escape')))
			url.append(Markup((story['url']).decode('unicode-escape')))
			content.append(Markup((story['content']).decode('unicode-escape')))
	print "countryname"+str(countryname)
	print "title"+str(title)
	print "url"+str(url)
	print "content:"+str(content)
	listlength=len(title)
	num_countries=len(news.keys()) 
	print listlength
	render = render_template('./carouseltemplate.html', countryname=countryname, country_codes=country_codes, name=name, news=news, listlength=listlength, num_countries=num_countries, url=url, title=title, content=content)

	return render

if __name__ == '__main__':
	app.debug = True
#	app.run()
	app.run('0.0.0.0')
