import requests


def request(url):
	try:
		return requests.get(url,timeout=3)
	except requests.exceptions.ConnectionError:
		pass


target_url = "192.168.1.113/mutillidae/"
with open("wordlist.txt","r") as wordlist:
	for line in wordlist:
		word = line.strip()
		url = "http://" + target_url + "/" + word
		#print(url)
		response = request(url)
		if response:
			print("[+] Discovered Url -> " + url)
