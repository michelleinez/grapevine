import json
import requests
import urllib
from flask import Markup

API_KEY = 'AIzaSyD7KOKsTnSnOfQO5yO4dPdGTDmipxKvbh4'

# a list of languages can be found here: https://cloud.google.com/translate/v2/using_rest
def translate_into_local_language(search_query, from_language, to_language):
	search_query = urllib.quote(search_query)

	print 'search_query', search_query

#	search_query = search_query.encode('utf-8')

#	print 'search_query.encode(utf-8)', search_query

#	search_query = Markup(search_query).decode('unicode-escape')

#	print 'search_query Markup', search_query

	translate = 'https://www.googleapis.com/language/translate/v2?key=%s&q=%s&source=%s&target=%s' % (API_KEY, search_query, from_language, to_language)
	print 'translate', translate
	response  = json.loads(requests.get(translate).text)


	tranlated_text = dict(response)

	return tranlated_text