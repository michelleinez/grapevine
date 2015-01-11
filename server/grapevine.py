from flask import Flask, request, render_template, url_for
import json
import requests
import TorBE
import Translate

API_KEY = 'AIzaSyD7KOKsTnSnOfQO5yO4dPdGTDmipxKvbh4'

app = Flask(__name__,static_url_path='')

translated_results = {}

@app.route('/')
def respond_to_request():
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

	return construct_carousel()

def construct_carousel(name=None):
	render = render_template('./childtemplate.html', name=name)
	print render
	return render

if __name__ == '__main__':
	app.debug = True
#	app.run()
	app.run('0.0.0.0')