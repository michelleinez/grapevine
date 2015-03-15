from flask import Flask, request, render_template, url_for, Markup
from multiprocessing import Process, Queue
import HTMLParser
import json
import requests
import tor
import Translate
import urllib

TRANSLATE_URL = 'http://www.googleapis.com/language/translate/v2?key=%s&q=%s&source=en&target=%s'
API_KEY = 'AIzaSyD7KOKsTnSnOfQO5yO4dPdGTDmipxKvbh4'

app = Flask(__name__, static_url_path='/static')

@app.route('/search')
def respond_to_request():
	#return construct_carousel()


	search_term     = request.args.get('search_term')
	country_codes   = request.args.getlist('country_code')

	country_codes_to_lang_code = [
									["af","ZA"],
									["sq","AL"],
									["ar","DZ"],
									["ar","BH"],
									["ar","EG"],
									["ar","IQ"],
									["ar","JO"],
									["ar","KW"],
									["ar","LB"],
									["ar","LY"],
									["ar","MA"],
									["ar","OM"],
									["ar","QA"],
									["ar","SA"],
									["ar","SY"],
									["ar","TN"],
									["ar","AE"],
									["ar","YE"],
									["hy","AM"]	,
									["eu","ES"],
									["be","BY"],
									["bg","BG"],
									["ca","ES"],
									["zh","CN"],
									["zh","HK"],
									["zh","MO"],
									["zh","SG"],
									["zh","TW"],
									["zh","CHS"],
									["zh","CHT"],
									["hr","HR"],
									["cs","CZ"],
									["da","DK"],
									["div","MV"],
									["nl","BE"],
									["nl","NL"],
									["en","AU"],
									["en","BZ"],
									["en","CA"],
									["en","CB"],
									["en","IE"],
									["en","JM"],
									["en","NZ"],
									["en","PH"],
									["en","ZA"],
									["en","TT"],
									["en","GB"],
									["en","US"],
									["en","ZW"],
									["et","EE"],
									["fo","FO"],
									["fa","IR"],
									["fi","FI"],
									["fr","BE"],
									["fr","CA"],
									["fr","FR"],
									["fr","LU"],
									["fr","MC"],
									["fr","CH"],
									["gl","ES"],
									["ka","GE"],
									["de","AT"],
									["de","DE"],
									["de","LI"],
									["de","LU"],
									["de","CH"],
									["el","GR"],
									["gu","IN"],
									["he","IL"],
									["hi","IN"],
									["hu","HU"],
									["is","IS"],
									["id","ID"],
									["it","IT"],
									["it","CH"],
									["ja","JP"],
									["kn","IN"],
									["kk","KZ"],
									["kok","IN"],
									["ko","KR"],
									["ky","KZ"],
									["lv","LV"],
									["lt","LT"],
									["mk","MK"],
									["ms","BN"],
									["ms","MY"],
									["mr","IN"],
									["mn","MN"],
									["nb","NO"],
									["nn","NO"],
									["pl","PL"],
									["pt","BR"],
									["pt","PT"],
									["pa","IN"],
									["ro","RO"],
									["ru","RU"],
									["sa","IN"],
									["sk","SK"],
									["sl","SI"],
									["es","AR"],
									["es","BO"],
									["es","CL"],
									["es","CO"],
									["es","CR"],
									["es","DO"],
									["es","EC"],
									["es","SV"],
									["es","GT"],
									["es","HN"],
									["es","MX"],
									["es","NI"],
									["es","PA"],
									["es","PY"],
									["es","PE"],
									["es","PR"],
									["es","ES"],
									["es","UY"],
									["es","VE"],
									["sw","KE"],
									["sv","FI"],
									["sv","SE"],
									["syr","SY"],
									["ta","IN"],
									["ru","RU"],
									["te","IN"],
									["th","TH"],
									["tr","TR"],
									["uk","UA"],
									["ur","PK"],
									["vi","VN"]]
	print ('search_term', search_term)
	print ('country_codes', country_codes)

	news = {}
	if(country_codes):
		for country in country_codes:
			print ('search_term', search_term)
			print ('country', country.lower())

			lang_Code = []
			for lc in country_codes_to_lang_code:
				if country.lower() == lc[1].lower():
					lang_Code = lc[0]

			print 'lang_Code', lang_Code

			translation_result = Translate.translate_into_local_language(search_term, 'en', lang_Code)
			#print json.dumps(translation_result, indent = 4, separators=(',', ': '))

			#print (translation_result)

			translated_search_term  = translation_result['data']['translations'][0]['translatedText']
			url = 'https://ajax.googleapis.com/ajax/services/search/news?v=1.0&q=%s' % translated_search_term
			print url


			q = Queue()
			p = Process(target=tor.make_request_thru_tor, args=(country,url, q))
			p.start()
			news_dict = q.get()
			p.join()
			#print ('news_dict', news_dict)


			#news_dict = TorBE.make_request_thru_tor(country, url)
			results = []
			translated_results = []
			for result in news_dict['responseData']['results']:
				results.append({'title': result['titleNoFormatting'],'url':result['url'], 'content':result['content']})
				
#				print 'result', result

#				translated_title   = Translate.translate_into_local_language(result['titleNoFormatting'], lang_Code, 'en')
#				translated_snippet = Translate.translate_into_local_language(result['content'], lang_Code, 'en')
#				translated_results.append({'title': translated_title, 'url': result['url'], 'content': translated_snippet})

#				print translated_results
#			news[country] = translated_results
			print 'results for %s : %s' % (country, str(results))
			news[country] = results

		return construct_carousel(news)

def construct_carousel(news):
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


	parser = HTMLParser.HTMLParser()

	title = []
	url = []
	content = []
	countries = []
	countryname = []
	#news = {'YE':[{'title': 'Elvis Presley&#39;s first record, &#39;My <b>Happiness</b>, auctions for $300K','url': 'http%3A%2F%2Fwww.tennessean.com%2Fstory%2Fentertainment%2Fmusic%2F2015%2F01%2F09%2Felvis-presleys-first-record-happiness-auctions%2F21497915%2F','content': 'Lorisa Hilburn, right, and relative Dianna Brookins, left, smile after an acetate recording of \u201cMy <b>Happiness</b>,\u201d the first song Elvis Presley ever recorded, was auctioned for a $300,000 on Thursday, Jan. 8, 2015, in Memphis. The record sat in a safe <b>...</b>'},{'title': '6 Toxic People Who May Be Sabotaging Your <b>Happiness</b>','url': 'http%3A%2F%2Fwww.huffingtonpost.com%2F2015%2F01%2F09%2Ftoxic-relationships-get-rid-of-them_n_6397200.html','content': 'I once read a quote by motivational speaker Jim Rohn that blatantly stated, &quot;You&#39;re the average of the five people you spend the most time with.&quot; It&#39;s an alarming thought -- shouldn&#39;t you be your own person, and not the sum of those around you? However&nbsp;...'}],'US':[{'title': 'Elvis Presley&#39;s first record, &#39;My <b>Happiness</b>, auctions for $300K','url': 'http%3A%2F%2Fwww.tennessean.com%2Fstory%2Fentertainment%2Fmusic%2F2015%2F01%2F09%2Felvis-presleys-first-record-happiness-auctions%2F21497915%2F','content': 'Lorisa Hilburn, right, and relative Dianna Brookins, left, smile after an acetate recording of \u201cMy <b>Happiness</b>,\u201d the first song Elvis Presley ever recorded, was auctioned for a$300,000 on Thursday, Jan. 8, 2015, in Memphis. The record sat in a safe <b>...</b>'},{'title': '6 Toxic People Who May Be Sabotaging Your <b>Happiness</b>','url': 'http%3A%2F%2Fwww.huffingtonpost.com%2F2015%2F01%2F09%2Ftoxic-relationships-get-rid-of-them_n_6397200.html','content': 'I once read a quote by motivational speaker Jim Rohn that blatantly stated, &quot;You&#39;re the average of the five people you spend the most time with.&quot; It&#39;s an alarming thought -- shouldn&#39;t you be your own person, and not the sum of those around you? However&nbsp;...'}], 'RU':[{'title': 'Elvis Presley&#39;s first record, &#39;My <b>Happiness</b>, auctions for $300K','url': 'http%3A%2F%2Fwww.tennessean.com%2Fstory%2Fentertainment%2Fmusic%2F2015%2F01%2F09%2Felvis-presleys-first-record-happiness-auctions%2F21497915%2F','content': 'Lorisa Hilburn, right, and relative Dianna Brookins, left, smile after an acetate recording of \u201cMy <b>Happiness</b>,\u201d the first song Elvis Presley ever recorded, was auctioned for a $300,000 on Thursday, Jan. 8, 2015, in Memphis. The record sat in a safe <b>...</b>'},{'title': '6 Toxic People Who May Be Sabotaging Your <b>Happiness</b>','url': 'http%3A%2F%2Fwww.huffingtonpost.com%2F2015%2F01%2F09%2Ftoxic-relationships-get-rid-of-them_n_6397200.html','content': 'I once read a quote by motivational speaker Jim Rohn that blatantly stated, &quot;You&#39;re the average of the five people you spend the most time with.&quot; It&#39;s an alarming thought -- shouldn&#39;t you be your own person, and not the sum of those around you? However&nbsp;...'}],'AR':[{'title': 'Elvis Presley&#39;s first record, &#39;My <b>Happiness</b>, auctions for $300K','url': 'http%3A%2F%2Fwww.tennessean.com%2Fstory%2Fentertainment%2Fmusic%2F2015%2F01%2F09%2Felvis-presleys-first-record-happiness-auctions%2F21497915%2F','content': 'Lorisa Hilburn, right, and relative Dianna Brookins, left, smile after an acetate recording of \u201cMy <b>Happiness</b>,\u201d the first song Elvis Presley ever recorded, was auctioned for a $300,000 on Thursday, Jan. 8, 2015, in Memphis. The record sat in a safe <b>...</b>'},{'title': '6 Toxic People Who May Be Sabotaging Your <b>Happiness</b>','url': 'http%3A%2F%2Fwww.huffingtonpost.com%2F2015%2F01%2F09%2Ftoxic-relationships-get-rid-of-them_n_6397200.html','content': 'I once read a quote by motivational speaker Jim Rohn that blatantly stated, &quot;You&#39;re the average of the five people you spend the most time with.&quot; It&#39;s an alarming thought -- shouldn&#39;t you be your own person, and not the sum of those around you? However&nbsp;...'}]}
	#print Markup((news['YE'][0]['title']).decode('unicode-escape'))

	for country in news.keys(): #for every news item...
		countries.append(country)
		countryname.append(countrycode_to_name[country])


	for i in range(4):
		for country in news.keys(): #for every news item...
			title.append(parser.unescape(news[country][i]['title']))
			url.append(urllib.unquote(news[country][i]['url']))
			content.append(parser.unescape(news[country][i]['content']))
	print "countryname"+str(countryname)
	print "title"+str(title)
	print "url"+str(url)
	print "content:"+str(content)
	listlength=len(title)
	num_countries=len(news.keys()) 
	print listlength
	render = render_template('./carouseltemplate.html', countryname=countryname, news=news, listlength=listlength, num_countries=num_countries, url=url, title=title, content=content)

	return render

@app.route('/')
def render(name=None):
    render = render_template('./form.html', name=name)
    print render
    return render


if __name__ == '__main__':
	app.debug = True
	app.threaded = False
#	app.run()
	app.run('0.0.0.0')
