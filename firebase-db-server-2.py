from firebase import firebase
import socket
import pickle

class quote:
	def __init__(self,quote,speaker):
		self.quote = quote
		self.speaker = speaker

host = '127.0.0.1'
port = 55433
serv_conn = (host,port)
parent_count = 0

with open("parent_count.txt",'r',encoding = 'utf-8') as p: #To retrieve current parent index feom database
	global parent_count                                    # WARNING: 'utf-8' encoding is only applicable for linux systems
	parent_count = p.read()  

with firebase.FirebaseApplication('website address') as firebase:
	while True:
		res = input("Do you want to keep the server online?[Y/N]")
		if 'N' in res:
			break
		with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
			s.bind(serv_conn)
			print('Listening on', serv_conn)
			s.listen()
			(conn, addr) = s.accept()
			with conn:
				print('Connected by', addr)
				while True:
					global s
					request = conn.recv(1024).decode()
					if not request:
						continue
					if 'update' in request:
						conn.sendall(b'ready')
						data = conn.recv(1024)
						nquote = pickle.loads(data)
						quote = nquote.quote
						speaker = nquote.speaker
						global firebase
						global parent_count
						upd_result = firebase.put('/quotes',parent_count,{quote:speaker})
						print('Updated in database', upd_result)
						p_temp = int(parent_count)
						p_temp = p_temp + 1
						parent_count = str(p_temp)
						#code to send notification 
						#to the admin view
					if 'retrieve' in request:
						conn.sendall(b'ready')
						data = conn.recv(1024).decode()
						qnum = str(data)
						req_data = firebase.get('/quotes',qnum)
						t1 = list(req_data)
						t2 = list(req_data.values())
						quote = t1[0]
						speaker = t2[0]
						ret_data = quote(quote,speaker)
						data2 = pickle.dumps(ret_data)
						conn.sendall(data2)
					if 'close' in request:
						break

with open("parent_count.txt",'w',encoding = 'utf-8') as f:
	global parent_count
	f.write(parent_count)