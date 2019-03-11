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
s.settimeout(2)

#used for lab6 go back N
windowSize = 4
isDone = False
ackFlag = True
sendList = ["Hi", "my", "name", "is", "Alex", "and", "I", "am", "in", "CS164"]
base = 0
i = 0
tmpList = sendList[base:windowSize]

csList = []

# print "Base - ", base
# print "Window Size - ", windowSize
# print tmpList

asd = True
x = 0

while not isDone:

	serverACK = []
	zero = 0
	one = 0
	messUp = -1
	prev = -1

	for packets in tmpList:

		d = ip_checksum(packets)

		if i % 2 == 0:
			ackNum = 0
			if ackFlag:
				tmp = str(ackNum) + "," + packets + "," + str(d)
			else:
				tmp = str(ackNum) + "," + packets + "," + "-1"
		elif i % 2 == 1:
			ackNum = 1
			if ackFlag:
				tmp = str(ackNum) + "," + packets + "," + str(d)
				if asd:
					tmp = str(ackNum) + "," + packets + "," + "-1"
					asd = False
			else:
				tmp = str(ackNum) + "," + packets + "," + "-1"

		# print i , "-" , tmp
		i += 1
		sendMessage(tmp, host, port, s)
		d = s.recvfrom(1024)
		reply = d[0]
		addr = d[1]
		serverACK.append(reply)

	for j in range(len(serverACK)):
		if serverACK[j] == "0":
			zero += 1
			if prev == 0:
				messUp = j 
				break
			prev = 0
		else:
			one += 1
			if prev == 1:
				messUp = j
				break
			prev = 1

	if messUp == -1:
		for z in serverACK:
			print "Server replies with ACK", z
		base += 4
		windowSize += 4
		tmpList = sendList[base:windowSize]

	else:
		print "Packet loss, resending", sendList[messUp] 
		base += messUp
		windowSize += messUp
		tmpList = sendList[base:windowSize]

	# print tmpList

	if sendList[-1] in tmpList and zero == one:
		isDone = True



# while not isDone:
# 	for z in range(windowSize):
# 		# print "Z - ", z
# 		try:
# 			print tmpList
# 			print "Sending Message - ", tmpList[z]
# 			if tmpList[z] == sendList[-1]:
# 				isDone = True
# 				break

# 			d = ip_checksum(tmpList[z])

# 			if i % 2 == 0:
# 				ackNum = 0
# 				if ackFlag:
# 					tmp = str(ackNum) + "," + tmpList[z] + "," + str(d)
# 					if phone:
# 						ackFlag = False
# 						phone = False
# 				else:
# 					tmp = str(ackNum) + "," + tmpList[z] + "," + "-1"
# 			elif i % 2 == 1:
# 				ackNum = 1
# 				if ackFlag:
# 					tmp = str(ackNum) + "," + tmpList[z] + "," + str(d)
# 				else:
# 					tmp = str(ackNum) + "," + tmpList[z] + "," + "-1"


# 			i += 1
# 			sendMessage(tmp, host, port, s)
# 			# d = s.recvfrom(1024)
# 			isAckList.append(0)
# 			# reply = d[0]
# 			# addr = d[1]
# 			# print "From server - ", reply, "\n"

# 		except timeout:
# 			isAckList.append(1)
# 			print isAckList
# 			ackFlag = True
# 			print "Timeout occured\n"
# 			continue

# 	if 1 in isAckList:
# 		isDone = False
# 		print "ASDASDASDA"
# 		for i in isAckList:
# 			if i == 0:
# 				# printAtEnd.append(tmpList[i])
# 				base += 1
# 				windowSize += 1
# 			if i == 1:
# 				break
# 		print "Base - ", base
# 		print "windowSize - ", windowSize
# 		tmpList = sendList[base:windowSize]
# 		del isAckList[:]
# 		d = s.recvfrom(1024)
# 		isAckList.append(0)
# 		reply = d[0]
# 		addr = d[1]
# 		print "From server - ", reply, "\n"
# 	else:
# 		print "SADWDASDA!@#!@#"
# 		if sendList[-1] not in tmpList:
# 			base += 1
# 			windowSize += 1
# 			tmpList = sendList[base:windowSize]
# 			isDone = False

# 			d = s.recvfrom(1024)
# 			isAckList.append(0)
# 			reply = d[0]
# 			addr = d[1]
# 			print "From server - ", reply, "\n"
# 		else:
# 			isDone = True
