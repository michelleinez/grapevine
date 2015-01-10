from flask import Flask, request
import json
import requests
import TorBE
import Translate

API_KEY = 'AIzaSyD7KOKsTnSnOfQO5yO4dPdGTDmipxKvbh4'

app = Flask(__name__,static_url_path='')

translated_results = {}

@app.route('/grapevine')
def respond_to_request():
	search_term   = request.args.get('search_term')
	country_codes = request.args.get('country_code')
	news = {}
	if(country_codes):
		for country in country_codes:
				translated_search_term = Translate.translate_into_local_language(search_term, country)
				url = 'https://ajax.googleapis.com/ajax/services/search/news?v=1.0&q=%s' % translated_search_term
				news_dict = TorBE.make_request_thru_tor(url, country)
				results = []
				for result in news_dict['responseData']['results']:
					results.append({result['title'], result['url'], result['comment']})
					
					translated_title   = 'https://www.googleapis.com/language/translate/v2?key=%s&q=%s&source=en&target=%s' % (API_KEY, results[result['title']], country)
					translated_url     = 'https://www.googleapis.com/language/translate/v2?key=%s&q=%s&source=en&target=%s' % (API_KEY, results[result['url']], country)
					translated_snippet = 'https://www.googleapis.com/language/translate/v2?key=%s&q=%s&source=en&target=%s' % (API_KEY, results[result['snippet']], country)

					translated_results.append({result[translated_title], result[translated_url], result[translated_snippet]})

				news[country] = results


	return "hello world"
#	return construct_carousel(news)

def construct_carousel(news_list):
	pass

if __name__ == '__main__':
	app.debug = True
#	app.run()
	app.run('0.0.0.0')


















