import sys
import fcntl
import termios
import threading
import time
import struct

# Progess bar code retrieved from somewhere on the net that I can't remember... sorry

COLS = struct.unpack('hh',  fcntl.ioctl(sys.stdout, termios.TIOCGWINSZ, '1234'))[1]

class Message(object):
	def __init__(self, messageType, calledInformation, message):
		self.messageType = messageType
		self.calledInformation = calledInformation
		self.message = message

	def print(self):
		print str(self.messageType) + " at " + str(self.time)
		print "From " + str(self.calledInformation["file"]) + " at " + str(self.calledInformation["line"])
		print "Trace:"
		print  
		

class MessageLog(object):
	def __init__(self):
		self.messages = {}

	def addMessage(self, message):
		self.messages[datetime.datetime.now()] = message

	def writeToDatabase(self):
		pass

class MessageHandler:
	def __init__(self):
		self.log = MessageLog()

	def bold(self, messsge):
		return u'\033[1m%s\033[0m' % message

	def progress(self, current, total, instanceTtype):
		prefix = '%d / %d %s' % (current, total, instanceType)
		barStart = ' ['
		barEnd = '] '
		barSize = COLS - len(prefix + barStart + barEnd)
		amount = int(current / (total / float(barSize)))
		remaining = barSize - amount
		bar = '.' * amount + ' ' * remaining
		return self.bold(prefix) + barStart + bar + barEnd

	def progressBar(self, number, total, interval, type):	
		number += 1	
		if (not (number % interval)):
			sys.stdout.write(self.progress(number, total, type) + '\r')
			sys.stdout.flush()	
		
	def end(self):
		print ""

	def message(self, objectType, location, message):
		if (self.level >= 0):
			print objectType + "Message: " + message
	
	def debug(self, objectType, location, message):
		if (self.level >= 1):
			print objectType + " at line " + location + " in " + fileName
			print "Message: " + message

	def error(self):
		pass

	def fatal(self):
		pass

#mh = MessageHandler()
#for i in range(100):
#	mh.progressBar(i, 100, "Histogram")
#print ""
