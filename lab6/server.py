import socket
import sys
from check import ip_checksum
HOST = ''
PORT = 8888

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	print "Socket created"
except socket.error:
		print "Failed to create client socket"
		sys.exit()


try:
	s.bind((HOST, PORT))
	print "Bind socket Created"
except socket.error, msg:
	print "Failed to bind"
	sys.exit()

#temp variable to save the last ack sent
tmpAck = -1
while 1:
	d = s.recvfrom(1024)
	data = d[0]
	addr = d[1]
	x = data.split(",")
	
	if x[2] != ip_checksum(x[1]):
		print "Packet was lost"
		reply = str(tmpAck)
	else:
		if x[0] == "0" or x[0] == "1":
			reply = str(x[0])
			tmpAck = x[0]

	s.sendto(reply, addr)
		