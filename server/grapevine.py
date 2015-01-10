from flask import Flask, request
import json
import requests

app = Flask(__name__,static_url_path='')


@app.route('/grapevine')
def respond_to_request():
	search_term = request.args.get('search_term')
	country_codes = request.args.get('country_code')
	news = []
	if(country_codes):
		for country in country_codes:
			translated_search_term = translate_into_local_language(search_term, country)
			news.append(make_request_thru_tor(translated_search_term, country))
	return "hello world"
#	return construct_carousel(news)

def translate_into_local_language(search_term, country_code):
	pass

def make_request_thru_tor(search_term, country_code):
	pass

def construct_carousel(news_list):
	pass

	
if __name__ == '__main__':
	app.debug = True
#	app.run()
	app.run('0.0.0.0')