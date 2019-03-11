from socket import timeout
import socket
import sys
from check import ip_checksum

def sendMessage(data, host, port, s):
	s.sendto(data, (host, port))

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
		print "Failed to create client socket"
		sys.exit()

host = 'localhost'
port = 8888
i = 0
s.settimeout(2)

while(1):
	flag2 = True
	flag = True
	msg = raw_input('Enter message to send: ')
	ackNum = 999
	while flag2:
		try :
			d = ip_checksum(msg)

			if i % 2 == 0:
				ackNum = 0
				if flag:
					tmp = str(ackNum) + "," + str(msg) + "," + "-1"
				else:
					tmp = str(ackNum) + "," + str(msg) + "," + d
			elif i % 2 == 1:
				ackNum = 1
				if flag:
					tmp = str(ackNum) + "," + str(msg) + "," + "-1"
				else:
					tmp = str(ackNum) + "," + str(msg) + "," + d

			sendMessage(tmp, host, port, s)
			d = s.recvfrom(1024)
			reply = d[0]
			addr = d[1]
			i += 1
			flag2 = False
			x = reply.split(",")

			if x[2] == "ACK0":
				reply = x[0]
				print "Server got ACK0"
			elif x[2] == "ACK1":
				reply = x[0]
				print "Server got ACK1"
			elif x[2] == "NAK":
				print "Server reply: " + reply

		except timeout:
			flag = False
			print "Timeout . . ."
			print "Error in receiving message from server"
			continue

