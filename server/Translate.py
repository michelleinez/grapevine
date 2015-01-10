import json
import requests

def translate_into_local_language(search_query, country_code):
	api_key      = 'AIzaSyD7KOKsTnSnOfQO5yO4dPdGTDmipxKvbh4'
#	search_query = 'hello world'
	search_term  = search_query.replace(" ", "%20")
	translate    = 'https://www.googleapis.com/language/translate/v2?key=%s&q=%s&source=en&target=%s' % (api_key, search_term, country_code)
	response     = json.loads(requests.get(translate).text)

	tranlated_text = dict(response)

	return tranlated_text