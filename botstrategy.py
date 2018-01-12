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
		candlestick.printInfo()
		self.currentPrice = float(candlestick.priceAverage)
		self.prices.append(self.currentPrice)
		
		self.output.log("Price: "+str(candlestick.priceAverage)+"\tMoving Average: "+str(self.indicators.movingAverage(self.prices,15)))

		self.evaluatePositions()
		self.updateOpenTrades()
		self.showAllTrades()

	def evaluatePositions(self):
		openTrades = []
		for trade in self.trades:
			if (trade.status == "OPEN"):
				openTrades.append(trade)

		if (len(openTrades) < self.numSimulTrades):
			if (self.currentPrice < self.indicators.movingAverage(self.prices,15)):
				#eventually expand this stop loss to be based on risk reward, volume, etc.
				#hardcoded for now
				trade = (BotTrade(self.currentPrice,stopLoss=.0001))
				self.trades.append(trade)

		for trade in openTrades:
			if (self.currentPrice > self.indicators.movingAverage(self.prices,15)):
				trade.close(self.currentPrice)

	def updateOpenTrades(self):
		for trade in self.trades:
			if (trade.status == "OPEN"):
				trade.tick(self.currentPrice)

	def getAllTrades(self):
		return self.trades

	def showAllTrades(self):
		for trade in self.trades:
			trade.showTrade()

		
