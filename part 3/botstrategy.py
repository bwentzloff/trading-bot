from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade

class BotStrategy(object):
	def __init__(self):
		self.output = BotLog()
		self.prices = []
		self.closes = [] # Needed for Momentum Indicator
		self.trades = []
		self.currentPrice = ""
		self.currentClose = ""
		self.numSimulTrades = 1
		self.indicators = BotIndicators()


	def tick(self,candlestick):
		self.currentPrice = float(candlestick['weightedAverage'])
		self.prices.append(self.currentPrice)

		self.currentClose = float(candlestick['close'])
		self.closes.append(self.currentClose)

=======
		
		#self.currentClose = float(candlestick['close'])
		#self.closes.append(self.currentClose)
		
		self.output.log("Price: "+str(candlestick['weightedAverage'])+"\tMoving Average: "+str(self.indicators.movingAverage(self.prices,15)))

		self.evaluatePositions()
		self.updateOpenTrades()
		self.showPositions()

	def evaluatePositions(self):
		openTrades = []
		for trade in self.trades:
			if (trade.status == "OPEN"):
				openTrades.append(trade)

		if (len(openTrades) < self.numSimulTrades):
			if (self.currentPrice < self.indicators.movingAverage(self.prices,15)):
				self.trades.append(BotTrade(self.currentPrice,stopLoss=.0001))

		for trade in openTrades:
			if (self.currentPrice > self.indicators.movingAverage(self.prices,15)):
				trade.close(self.currentPrice)

	def updateOpenTrades(self):
		for trade in self.trades:
			if (trade.status == "OPEN"):
				trade.tick(self.currentPrice)

	def showPositions(self):
		for trade in self.trades:
			trade.showTrade()
		
