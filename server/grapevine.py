from flask import Flask, request, render_template, url_for, Markup
import HTMLParser
import json
import requests
import TorBE
import Translate
import urllib

TRANSLATE_URL = 'https://www.googleapis.com/language/translate/v2?key=%s&q=%s&source=en&target=%s'
API_KEY = 'AIzaSyD7KOKsTnSnOfQO5yO4dPdGTDmipxKvbh4'

app = Flask(__name__, static_url_path='/static')

country_codes = ['us', 'uk', 'ru', 'ar']

@app.route('/')
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
									["tt","RU"],
									["te","IN"],
									["th","TH"],
									["tr","TR"],
									["uk","UA"],
									["ur","PK"],
									["vi","VN"]]
	print (search_term)
	print (country_codes)

	news = {}
	if(country_codes):
		for country in country_codes:
				print ('search_term', search_term)
				print ('country', country.lower())

				lang_Code = []
				print (country_codes_to_lang_code)
				for lc in country_codes_to_lang_code:
					if country.lower() == lc[1].lower():
						lang_Code = lc[0]

				print (lang_Code)

				translation_result = Translate.translate_into_local_language(search_term, lang_Code)
				print (json.dumps(translation_result, indent = 4, separators=(',', ': ')))

				print (translation_result)

				translated_search_term  = translation_result['data']['translations'][0]['translatedText']
				url = 'https://ajax.googleapis.com/ajax/services/search/news?v=1.0&q=%s' % translated_search_term
				print(url)
				news_dict = TorBE.make_request_thru_tor(url, country)
				results = []
				translated_results = []
				for result in news_dict['responseData']['results']:
					results.append({'title': result['title'],'url':result['url'], 'content':result['content']})
					
					print (results)

					translated_title   = TRANSLATE_URL % (API_KEY, results[result['title']], country)
					translated_snippet = TRANSLATE_URL % (API_KEY, results[result['content']], country)

					translated_results.append({'title': result[translated_title], 'url': result['url'], 'content': result[translated_snippet]})

					print (translated_results)

				news[country] = translated_results
	return str(news)

def construct_carousel(name=None):
	title = []
	url = []
	content = []
	news = {'uk':[{'title': 'Elvis Presley&#39;s first record, &#39;My <b>Happiness</b>, auctions for $300K','url': 'http%3A%2F%2Fwww.tennessean.com%2Fstory%2Fentertainment%2Fmusic%2F2015%2F01%2F09%2Felvis-presleys-first-record-happiness-auctions%2F21497915%2F','content': 'Lorisa Hilburn, right, and relative Dianna Brookins, left, smile after an acetate recording of \u201cMy <b>Happiness</b>,\u201d the first song Elvis Presley ever recorded, was auctioned for a $300,000 on Thursday, Jan. 8, 2015, in Memphis. The record sat in a safe <b>...</b>'},{'title': '6 Toxic People Who May Be Sabotaging Your <b>Happiness</b>','url': 'http%3A%2F%2Fwww.huffingtonpost.com%2F2015%2F01%2F09%2Ftoxic-relationships-get-rid-of-them_n_6397200.html','content': 'I once read a quote by motivational speaker Jim Rohn that blatantly stated, &quot;You&#39;re the average of the five people you spend the most time with.&quot; It&#39;s an alarming thought -- shouldn&#39;t you be your own person, and not the sum of those around you? However&nbsp;...'}],'us':[{'title': 'Elvis Presley&#39;s first record, &#39;My <b>Happiness</b>, auctions for $300K','url': 'http%3A%2F%2Fwww.tennessean.com%2Fstory%2Fentertainment%2Fmusic%2F2015%2F01%2F09%2Felvis-presleys-first-record-happiness-auctions%2F21497915%2F','content': 'Lorisa Hilburn, right, and relative Dianna Brookins, left, smile after an acetate recording of \u201cMy <b>Happiness</b>,\u201d the first song Elvis Presley ever recorded, was auctioned for a$300,000 on Thursday, Jan. 8, 2015, in Memphis. The record sat in a safe <b>...</b>'},{'title': '6 Toxic People Who May Be Sabotaging Your <b>Happiness</b>','url': 'http%3A%2F%2Fwww.huffingtonpost.com%2F2015%2F01%2F09%2Ftoxic-relationships-get-rid-of-them_n_6397200.html','content': 'I once read a quote by motivational speaker Jim Rohn that blatantly stated, &quot;You&#39;re the average of the five people you spend the most time with.&quot; It&#39;s an alarming thought -- shouldn&#39;t you be your own person, and not the sum of those around you? However&nbsp;...'}], 'ru':[{'title': 'Elvis Presley&#39;s first record, &#39;My <b>Happiness</b>, auctions for $300K','url': 'http%3A%2F%2Fwww.tennessean.com%2Fstory%2Fentertainment%2Fmusic%2F2015%2F01%2F09%2Felvis-presleys-first-record-happiness-auctions%2F21497915%2F','content': 'Lorisa Hilburn, right, and relative Dianna Brookins, left, smile after an acetate recording of \u201cMy <b>Happiness</b>,\u201d the first song Elvis Presley ever recorded, was auctioned for a $300,000 on Thursday, Jan. 8, 2015, in Memphis. The record sat in a safe <b>...</b>'},{'title': '6 Toxic People Who May Be Sabotaging Your <b>Happiness</b>','url': 'http%3A%2F%2Fwww.huffingtonpost.com%2F2015%2F01%2F09%2Ftoxic-relationships-get-rid-of-them_n_6397200.html','content': 'I once read a quote by motivational speaker Jim Rohn that blatantly stated, &quot;You&#39;re the average of the five people you spend the most time with.&quot; It&#39;s an alarming thought -- shouldn&#39;t you be your own person, and not the sum of those around you? However&nbsp;...'}],'ar':[{'title': 'Elvis Presley&#39;s first record, &#39;My <b>Happiness</b>, auctions for $300K','url': 'http%3A%2F%2Fwww.tennessean.com%2Fstory%2Fentertainment%2Fmusic%2F2015%2F01%2F09%2Felvis-presleys-first-record-happiness-auctions%2F21497915%2F','content': 'Lorisa Hilburn, right, and relative Dianna Brookins, left, smile after an acetate recording of \u201cMy <b>Happiness</b>,\u201d the first song Elvis Presley ever recorded, was auctioned for a $300,000 on Thursday, Jan. 8, 2015, in Memphis. The record sat in a safe <b>...</b>'},{'title': '6 Toxic People Who May Be Sabotaging Your <b>Happiness</b>','url': 'http%3A%2F%2Fwww.huffingtonpost.com%2F2015%2F01%2F09%2Ftoxic-relationships-get-rid-of-them_n_6397200.html','content': 'I once read a quote by motivational speaker Jim Rohn that blatantly stated, &quot;You&#39;re the average of the five people you spend the most time with.&quot; It&#39;s an alarming thought -- shouldn&#39;t you be your own person, and not the sum of those around you? However&nbsp;...'}]}
	print (Markup((news['uk'][0]['title']).decode('unicode-escape')))
	for country in news.keys(): #for every news item...
		print (country)
		for story in news[country]:		
			title.append(Markup((story['title']).decode('unicode-escape')))
			url.append(Markup((story['url']).decode('unicode-escape')))
			content.append(Markup((story['content']).decode('unicode-escape')))

	print ("title"+str(title))
	print ("url"+str(url))
	print ("content:"+str(content))
	listlength=len(title)
	num_countries=len(news.keys()) 
	print (listlength)
	render = render_template('./carouseltemplate.html', country_codes=country_codes, name=name, news=news, listlength=listlength, num_countries=num_countries, url=url, title=title, content=content)

	return render

if __name__ == '__main__':
	app.debug = True
#	app.run()
	app.run('0.0.0.0')
