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

country_codes = ['us', 'uk', 'ru', 'ar']

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
	title = []
	url = []
	content = []
	news = {'uk':[{'title': 'Elvis Presley&#39;s first record, &#39;My <b>Happiness</b>, auctions for $300K','url': 'http%3A%2F%2Fwww.tennessean.com%2Fstory%2Fentertainment%2Fmusic%2F2015%2F01%2F09%2Felvis-presleys-first-record-happiness-auctions%2F21497915%2F','content': 'Lorisa Hilburn, right, and relative Dianna Brookins, left, smile after an acetate recording of \u201cMy <b>Happiness</b>,\u201d the first song Elvis Presley ever recorded, was auctioned for a $300,000 on Thursday, Jan. 8, 2015, in Memphis. The record sat in a safe <b>...</b>'},{'title': '6 Toxic People Who May Be Sabotaging Your <b>Happiness</b>','url': 'http%3A%2F%2Fwww.huffingtonpost.com%2F2015%2F01%2F09%2Ftoxic-relationships-get-rid-of-them_n_6397200.html','content': 'I once read a quote by motivational speaker Jim Rohn that blatantly stated, &quot;You&#39;re the average of the five people you spend the most time with.&quot; It&#39;s an alarming thought -- shouldn&#39;t you be your own person, and not the sum of those around you? However&nbsp;...'}],'us':[{'title': 'Elvis Presley&#39;s first record, &#39;My <b>Happiness</b>, auctions for $300K','url': 'http%3A%2F%2Fwww.tennessean.com%2Fstory%2Fentertainment%2Fmusic%2F2015%2F01%2F09%2Felvis-presleys-first-record-happiness-auctions%2F21497915%2F','content': 'Lorisa Hilburn, right, and relative Dianna Brookins, left, smile after an acetate recording of \u201cMy <b>Happiness</b>,\u201d the first song Elvis Presley ever recorded, was auctioned for a$300,000 on Thursday, Jan. 8, 2015, in Memphis. The record sat in a safe <b>...</b>'},{'title': '6 Toxic People Who May Be Sabotaging Your <b>Happiness</b>','url': 'http%3A%2F%2Fwww.huffingtonpost.com%2F2015%2F01%2F09%2Ftoxic-relationships-get-rid-of-them_n_6397200.html','content': 'I once read a quote by motivational speaker Jim Rohn that blatantly stated, &quot;You&#39;re the average of the five people you spend the most time with.&quot; It&#39;s an alarming thought -- shouldn&#39;t you be your own person, and not the sum of those around you? However&nbsp;...'}], 'ru':[{'title': 'Elvis Presley&#39;s first record, &#39;My <b>Happiness</b>, auctions for $300K','url': 'http%3A%2F%2Fwww.tennessean.com%2Fstory%2Fentertainment%2Fmusic%2F2015%2F01%2F09%2Felvis-presleys-first-record-happiness-auctions%2F21497915%2F','content': 'Lorisa Hilburn, right, and relative Dianna Brookins, left, smile after an acetate recording of \u201cMy <b>Happiness</b>,\u201d the first song Elvis Presley ever recorded, was auctioned for a $300,000 on Thursday, Jan. 8, 2015, in Memphis. The record sat in a safe <b>...</b>'},{'title': '6 Toxic People Who May Be Sabotaging Your <b>Happiness</b>','url': 'http%3A%2F%2Fwww.huffingtonpost.com%2F2015%2F01%2F09%2Ftoxic-relationships-get-rid-of-them_n_6397200.html','content': 'I once read a quote by motivational speaker Jim Rohn that blatantly stated, &quot;You&#39;re the average of the five people you spend the most time with.&quot; It&#39;s an alarming thought -- shouldn&#39;t you be your own person, and not the sum of those around you? However&nbsp;...'}],'ar':[{'title': 'Elvis Presley&#39;s first record, &#39;My <b>Happiness</b>, auctions for $300K','url': 'http%3A%2F%2Fwww.tennessean.com%2Fstory%2Fentertainment%2Fmusic%2F2015%2F01%2F09%2Felvis-presleys-first-record-happiness-auctions%2F21497915%2F','content': 'Lorisa Hilburn, right, and relative Dianna Brookins, left, smile after an acetate recording of \u201cMy <b>Happiness</b>,\u201d the first song Elvis Presley ever recorded, was auctioned for a $300,000 on Thursday, Jan. 8, 2015, in Memphis. The record sat in a safe <b>...</b>'},{'title': '6 Toxic People Who May Be Sabotaging Your <b>Happiness</b>','url': 'http%3A%2F%2Fwww.huffingtonpost.com%2F2015%2F01%2F09%2Ftoxic-relationships-get-rid-of-them_n_6397200.html','content': 'I once read a quote by motivational speaker Jim Rohn that blatantly stated, &quot;You&#39;re the average of the five people you spend the most time with.&quot; It&#39;s an alarming thought -- shouldn&#39;t you be your own person, and not the sum of those around you? However&nbsp;...'}]}
	print Markup((news['uk'][0]['title']).decode('unicode-escape'))
	for country in news.keys(): #for every news item...
		print country
		for story in news[country]:		
			title.append(Markup((story['title']).decode('unicode-escape')))
			url.append(Markup((story['url']).decode('unicode-escape')))
			content.append(Markup((story['content']).decode('unicode-escape')))

	print "title"+str(title)
	print "url"+str(url)
	print "content:"+str(content)
	listlength=len(title)
	num_countries=len(news.keys()) 
	print listlength
	render = render_template('./carouseltemplate.html', country_codes=country_codes, name=name, news=news, listlength=listlength, num_countries=num_countries, url=url, title=title, content=content)

	return render

if __name__ == '__main__':
	app.debug = True
#	app.run()
	app.run('0.0.0.0')
