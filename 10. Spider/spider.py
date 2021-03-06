import requests,re
from urllib.parse import urljoin


def extract_link_from(url):
	response = requests.get(url)
	try:
		return re.findall('(?:href=")(.*?)"',response.content.decode())
	except UnicodeDecodeError:
		return []


target_url = "your targer url"
target_links = []

def crawl(url):
	href_links = extract_link_from(url)
	for link in href_links:
		link = urljoin(url,link)

		if '#' in link:
			link = link.split('#')[0]

		if target_url in link and link not in target_links:
			target_links.append(link)
			print(link)
			crawl(link)

crawl(target_url)