import subprocess,re


networks = subprocess.getoutput("netsh wlan show profile")
networks_list = re.findall("(?:Profile\s*:\s*)(.*)",networks)

result = ""
for network in networks_list:
	networkInfo = subprocess.getoutput('netsh wlan show profile "'+ network + '" key=clear')
	key = re.findall("(?:Content\s*:\s*)(.*)",networkInfo)
	if len(key) > 0:
		#print(str(network)+":"+key[0])
		result = result + str(network)+":"+key[0] + "\n"
	else:
		result = result + str(network)+":"+" Password Not Found\n" 


print(result)








