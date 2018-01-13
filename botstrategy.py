from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade

class BotStrategy(object):
	def __init__(self, mode="SIM", trade_type="taker", starting_balance_currency=1000, starting_balance_asset=0, buy_percentage=0.99, sell_percentage=0.99):
		self.output = BotLog()
		self.prices = []
		self.closes = [] # Needed for Momentum Indicator
		self.trades = []
		self.startingPrice = None
		self.currentPrice = ""
		self.currentClose = ""
		self.buy_percentage=buy_percentage
		self.sell_percentage=sell_percentage
		self.numSimulTrades = 1
		self.indicators = BotIndicators()
		#taker orders have no (or minimal) delay, but a 0.25% transaction fee
		#maker orders have no fee but won't be filled instantly
		self.trade_type=trade_type
		self.balance_currency=starting_balance_currency
		self.balance_asset=starting_balance_asset
		self.mode = mode
		if (mode == "LIVE"):
			self.authClient = auth_client = gdax.AuthenticatedClient('ec4af4d834af89078dfa8ce52e487421', 'wYxKIZ8oO8Ntaj8Mq42M7A1L8Z3WM+qeWGnh7V4NSr7cVnUZmoz2VIMhuFHHFvyDt2KyeXGdT0mAZvXzN1tfAA==', 'er2maud6tej')

	def tick(self,candlestick):
		#candlestick.printInfo()
		self.currentPrice = float(candlestick.priceAverage)
		self.prices.append(self.currentPrice)
		if self.startingPrice is None:
			self.startingPrice = self.currentPrice
		
		#self.output.log("Price: "+str(candlestick.priceAverage)+"\tMoving Average: "+str(self.indicators.movingAverage(self.prices,15)))
		candleCloseTime = candlestick.endTime
		self.evaluatePositions(candleCloseTime)
		#self.updateOpenTrades()
		#self.showAllTrades()

	def evaluatePositions(self, candleCloseTime):
		openTrades = []
		for trade in self.trades:
			if (trade.status == "OPEN"):
				openTrades.append(trade)

		if (len(openTrades) < self.numSimulTrades):
			if (self.currentPrice < self.indicators.movingAverage(self.prices,15)):
				#eventually expand this stop loss to be based on risk reward, volume, etc.
				#hardcoded for now
				trade = (BotTrade(self.currentPrice,candleCloseTime,stopLoss=.03))
				self.trades.append(trade)
				#if this strategy is running in live mode, trigger the actual buy
				#if (self.mode == "LIVE"):
				#otherwise simulate the purchase by changing the balances manually
				#else:
				#remove 99% of the currency balance
				balance_to_spend = 0.99 * self.balance_currency
				self.balance_currency -= balance_to_spend
				#amount to buy is the balance to spend * the value of one dollar * 0.9975 to account for transaction fee
				asset_value = balance_to_spend * (1/self.currentPrice) * 0.9975
				self.balance_asset += asset_value

		for trade in openTrades:
			if (trade.stopLoss and self.currentPrice < trade.stopLoss):
				self.output.log("Stop loss triggered")
				trade.close(self.currentPrice, candleCloseTime)
			if (self.currentPrice > self.indicators.movingAverage(self.prices,15)):
				trade.close(self.currentPrice, candleCloseTime)
				#if this strategy is running in live mode, trigger the actual sell
				#if (self.mode == "LIVE"):
				#otherwise simulate the purchase by changing the balances manually
				#else:
				asset_to_spend = 0.99 * self.balance_asset
				self.balance_asset -= asset_to_spend
				currency_value = asset_to_spend * self.currentPrice * 0.9975
				self.balance_currency += currency_value

	def updateOpenTrades(self):
		for trade in self.trades:
			if (trade.status == "OPEN"):
				trade.tick(self.currentPrice)

	def getAllTrades(self):
		return self.trades

	def showAllTrades(self):
		for trade in self.trades:
			trade.showTrade()

		
