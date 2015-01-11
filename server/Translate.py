import json
import requests

API_KEY = 'AIzaSyD7KOKsTnSnOfQO5yO4dPdGTDmipxKvbh4'

# a list of languages can be found here: https://cloud.google.com/translate/v2/using_rest
def translate_into_local_language(search_query, country_code):
	search_term  = search_query.replace(" ", "%20")
	translate    = 'https://www.googleapis.com/language/translate/v2?key=%s&q=%s&source=en&target=%s' % (API_KEY, search_term, country_code)
	response     = json.loads(requests.get(translate).text)

	tranlated_text = dict(response)

	return tranlated_text