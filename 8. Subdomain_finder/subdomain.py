import requests


def request(url):
	try:
		return requests.get(url,timeout=3)
	except requests.exceptions.ConnectionError:
		pass

target_url = "your Target url goes here"
with open("wordlist.txt","r") as wordlist:
	for line in wordlist:
		word = line.strip()
		url = "http://" + word + "." + target_url
		#print(url)
		response = request(url)
		if response:
			print("[+] url found -> " + url)
