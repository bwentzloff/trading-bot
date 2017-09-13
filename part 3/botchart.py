from poloniex import poloniex

class BotChart(object):
	def __init__(self, exchange, pair, period):
		self.conn = poloniex('ID8SVZR495A6A44RPKXPWVSGR1ANXPH6','518b0335e8931b8a4d37286728ed582b8ba4eb96a099a20677167ddc9ded911ab5c8217c0c1dfe6665a833128193576ea3ae1e8ab96f9f623ce271663f9c7148')

		self.pair = pair
		self.period = period

		self.startTime = 1491048000
		self.endTime = 1491591200

		self.data = self.conn.api_query("returnChartData",{"currencyPair":self.pair,"start":self.startTime,"end":self.endTime,"period":self.period})

	def getPoints(self):
		return self.data
