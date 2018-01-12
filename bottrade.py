from botlog import BotLog
import datetime

class BotTrade(object):
	def __init__(self,currentPrice,stopLoss=0):
		self.output = BotLog()
		self.openTime = str(datetime.datetime.now())
		self.output.log("Trade opened at " + self.openTime)
		self.status = "OPEN"
		self.entryPrice = currentPrice
		self.exitPrice = ""
		self.closeTime = ""
		if (stopLoss):
			self.stopLoss = currentPrice - stopLoss
	
	def close(self,currentPrice):
		self.status = "CLOSED"
		self.exitPrice = currentPrice
		self.output.log("Trade closed")

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
	