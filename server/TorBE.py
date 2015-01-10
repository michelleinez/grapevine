import socks
import socket
import requests
import json
import stem.process
	
PORT = 7000
	
# DNS resolution
def getaddrinfo(*args):
	return [(socket.AF_INET, socks.SOCK_STREAM, 6, "", (args[0], args[1]))]

def query(url):
	response = json.loads(requests.get(url).text)
	print json.dumps(response, indent=4, separators=(',',': '))

# a list of country codes can be found here: https://b3rn3d.herokuapp.com/blog/2014/03/05/tor-country-codes
def make_request_thru_tor(countryCode, url):
	print "Connecting to tor..."
	socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", PORT)
	socket.socket = socks.socksocket

	socks.getaddrinfo = getaddrinfo

	print "Starting to configure tor..."
	# make sure that a secondary tor process is not running!
	tor_config = stem.process.launch_tor_with_config(
		config = {"SocksPort" : str(PORT), "ExitNodes" : "{" + countryCode + "}"})

	print "Querying",url
	query(url)

	tor_config.kill()

if __name__ == '__main__':
	make_request_thru_tor("ru", 'https://ajax.googleapis.com/ajax/services/search/web?v=1.0&q=paris')