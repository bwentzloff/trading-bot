from poloniex import poloniex
import urllib, json
import pprint

class BotChart(object):
	def __init__(self, exchange, pair, period, backtest=True):
		self.pair = pair
		self.period = period

		self.startTime = 1491048000
		self.endTime = 1491591200

		self.data = []
		
		if (exchange == "poloniex"):
			self.conn = poloniex('key goes here','Secret goes here')

			if backtest:
				self.data = self.conn.api_query("returnChartData",{"currencyPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period})

		if (exchange == "bittrex"):
			if backtest:
				url = "https://bittrex.com/Api/v2.0/pub/market/GetTicks?marketName="+self.pair+"&tickInterval="+self.period+"&_="+str(self.startTime)
				response = urllib.urlopen(url)
				rawdata = json.loads(response.read())

				self.data = rawdata["result"]


	def getPoints(self):
		return self.data

	def getCurrentPrice(self):
		currentValues = self.conn.api_query("returnTicker")
		lastPairPrice = {}
		lastPairPrice = currentValues[self.pair]["last"]
		return lastPairPrice
