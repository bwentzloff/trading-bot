import sys, getopt
import time
import datetime

from botlog import BotLog

class BotCandlestick(object):
	def __init__(self, period=300,open=None,close=None,high=None,low=None,priceAverage=None,volume=None):
		self.current = None
		self.open = open
		self.close = close
		self.high = high
		self.low = low
		self.startTime = time.time()
		self.period = period
		self.output = BotLog()
		self.priceAverage = priceAverage
		self.closed = False
		self.volume = volume
		self.endTime = None

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
			self.closed = True
			self.priceAverage = ( self.high + self.low + self.close ) / float(3)
			self.endTime = time.time()
			self.output.log("candlestick closed")

		self.output.log("Open: "+str(self.open)+" Close: "+str(self.close)+" High: "+str(self.high)+" Low: "+str(self.low)+" Current: "+str(self.current))

	#update the time of the candestick to fill in accurate information in 
	#candesticks generated from backfilled data
	def setTime(self, time):
		self.endTime = time

	#print out the information contained in this candlestick to its output log
	def printInfo(self):
		time = datetime.datetime.utcfromtimestamp(self.startTime)
		self.output.log("Start time: " + str(time) + " Open: "+str(self.open)+" Close: "+str(self.close)+" High: "+str(self.high)+" Low: "+str(self.low) + " Price Average: " + str(self.priceAverage))
