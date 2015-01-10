import json
import requests

def translate_into_local_language(search_query, country_code):
	api_key      = 'AIzaSyD7KOKsTnSnOfQO5yO4dPdGTDmipxKvbh4'

	# TODO: if not already done, replace spaces in search_query with '%20'
	#search_query = 'hello%20world'
	translate    = 'https://www.googleapis.com/language/translate/v2?key=%s&q=%s&source=en&target=%s' % (api_key, search_query, country_code)
	response     = json.loads(requests.get(translate).text)

	tranlated_text = dict(response)

	return tranlated_text

#if __name__ == '__main__':
#	translate_into_local_language("ru")