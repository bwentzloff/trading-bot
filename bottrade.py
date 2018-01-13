from botlog import BotLog
import datetime
import dateutil.parser

class BotTrade(object):
	def __init__(self,currentPrice,openTime,stopLoss=0):
		self.output = BotLog()
		#this is the time the candlestick the triggered the trade order was closed, there will be some delay before trade is actually opened
		self.openTime = openTime
		#open = datetime.datetime(openTime)
		#timeString = str(dateutil.parser.parse(self.openTime.isoformat()))
		#self.output.log("Trade opened at " + timeString)
		self.status = "OPEN"
		self.entryPrice = currentPrice
		self.exitPrice = ""
		self.closeTime = None
		self.stopLoss = None
		if (stopLoss):
			self.stopLoss = currentPrice - stopLoss*currentPrice
	
	def close(self,currentPrice, closeTime):
		self.status = "CLOSED"
		self.exitPrice = currentPrice
		self.closeTime = closeTime
		#timeString = str(dateutil.parser.parse(self.closeTime.isoformat))
		#self.output.log("Trade closed at " + timeString)

	def tick(self, currentPrice):
		if (self.stopLoss):
			if (currentPrice < self.stopLoss):
				self.output.log("Stop loss triggered")
				self.close(currentPrice)

	def getStopLossPrice(self):
		if (self.stopLoss):
			return self.stopLoss
		else:
			return None

	def showTrade(self):
		tradeStatus = "Entry Price: "+str(self.entryPrice)+" Status: "+str(self.status)+" Exit Price: "+str(self.exitPrice)

		if (self.status == "CLOSED"):
			tradeStatus = tradeStatus + " Percent Change: "
			if (self.exitPrice > self.entryPrice):
				tradeStatus = tradeStatus + "\033[92m"
			else:
				tradeStatus = tradeStatus + "\033[91m"
			#calculate the percentage of change of this trade
			percentage = ((float(self.exitPrice) - float(self.entryPrice))/float(self.entryPrice))*float(100)

			tradeStatus = tradeStatus+str(percentage)+"\033[0m"

		self.output.log(tradeStatus)
		self.output.log("Open Time: " + str(self.openTime) + " Close Time: " + str(self.closeTime))
	