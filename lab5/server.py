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


while 1:
	d = s.recvfrom(1024)
	data = d[0]
	addr = d[1]

	if not data:
		break

	x = data.split(",")

	if x[2] != ip_checksum(x[1]):
		print "ip_checksum not recgonized"
	else:
		if x[0] == "0":
			reply = "OK . . . " + "," + x[1] + "," + "ACK0" + "," + x[2]
			print "ACK0"
		elif x[0] == "1":
			reply = "OK . . . " + "," + x[1] + "," + "ACK1" + "," + x[2]
			print "ACK1"
		else:
			print "Did not read of not valid"
			break

		print "Sending: ", reply
		s.sendto(reply, addr)
		print "Message[" + addr[0] + ":" + str(addr[1]) + "] - " + data.strip()