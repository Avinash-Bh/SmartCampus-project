from firebase import firebase
import socket 
import pickle
import os

class quote:                           #Used to temporarily store the newly received quote from user
	def __init__(self,quote,speaker):
		self.qoute = qoute
		self.speaker = speaker

host = '127.0.0.1'
port = 55432
serv_conn = (host,port)
parent_count

with open("parent_count.txt",'r',encoding = 'utf-8') as p:  #Retrieve the current parent index for the database 
	pdata = p.read()                                        # WARNING: Current encoding applicable for Linux ONLY. Change 'encoding' to 'cp1252' for Windows 
	global parent_count
	parent_count = pdata

with firebase.FirebaseApplication('website address') as firebase: #Insert the database address where 'website address' is written
	with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  #Create a socket object to communicate with the front-end
		s.bind(serv_conn)
		print('Listening on', serv_conn)
		s.listen()
		conn, addr = s.accept()
		with conn:
			print('Connected by', addr)
			while True:
				request = conn.recv(1024).decode()
				if not request:
					continue
				if 'update' in request:          #Inform front-end that the request to update has been received and server is ready to accept the new entry
					conn.sendall(b'ready')
					data = conn.recv(1024)       #Temporarily store the recived data in binary form
					nquote = pickle.loads(data)  #Store the data in object after extracting
					quote = nquote.quote         #Create new separate variables to hold
					speaker = nquote,speaker     #quote and speaker individually
					global firebase
					global parent_count
					upd_result = firebase.put('quotes',parent_count,{quote:speaker})
					print('Updated in database', upd_result)  #Notify on server terminal when update is done
					p_temp = int(parent_count)
					p_temp = p_temp + 1
					parent_count = str(p_temp)
					#Code to send notification
					#to the admin view
				if 'retrieve' in request:
					#code block to
					#retrieve the data from firebase
				if 'close' in request:
					break

os.remove('parent_count.txt') #May not be necessary as code further down will overwrite any pre-existing file

with open("parent_count.txt",'w',encoding = 'utf-8') as p:
	global parent_count
	p.write(parent_count)