import sys, getopt
import time

from botlog import BotLog

class BotCandlestick(object):
	def __init__(self, period=300):
		self.current = None
		self.open = None
		self.close = None
		self.high = None
		self.low = None
		self.startTime = time.time()
		self.period = period
		self.output = BotLog()
		self.weightedAverage = None

	def tick(self,price):
		self.current = float(price)
		if (self.open is None):
			self.open = self.current

		if ( (self.high is None) or (self.current > self.high) ):
			self.high = self.current

		if ( (self.low is None) or (self.current < self.low) ):
			self.low = self.current

		if ( time.time() >= ( self.startTime + self.period) ):
			self.close = self.current
			self.weightedAverage = ( self.high + self.low + self.close ) / float(3)

		self.output.log("Open: "+str(self.open)+" Close: "+str(self.close)+" High: "+str(self.high)+" Low: "+str(self.low)+" Current: "+str(self.current))

	def isClosed(self):
		if (self.close is not None):
			return True
		else:
			return False

