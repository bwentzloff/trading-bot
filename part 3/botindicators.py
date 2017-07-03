class BotIndicators(object):
	def __init__(self):
		 pass

	def movingAverage(self, dataPoints, period):
		if (len(dataPoints) > 1):
			return sum(dataPoints[-period:]) / float(len(dataPoints[-period:]))
		
	def momentum (self, dataPoints, period=14):
		if (len(dataPoints) > period -1):
			return dataPoints[-1] * 100 / dataPoints[-period]

	def EMA(self, dataPoints, period, position=None, previous_ema=None):
		"""https://www.oanda.com/forex-trading/learn/forex-indicators/exponential-moving-average"""
		if len(dataPoints) < period + 2:
			return None
		c = 2 / float(period + 1)
		if not previous_ema:
			return EMA(dataPoints, period, period, movingAverage(dataPoints[-period*2 + 1:-period + 1], period))
		else:
			current_ema = (c * dataPoints[-position]) + ((1 - c) * previous_ema)
			if position > 0:
				return EMA(dataPoints, period, position - 1, current_ema)
		return previous_ema
