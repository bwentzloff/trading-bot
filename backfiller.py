import gdax
import urllib, json
import pprint
from botcandlestick import BotCandlestick
import datetime

class Backfiller(object):
	def __init__(self, exchange, pair, period, num_days_to_backTest=5):
		self.pair = pair
		self.period = period

		self.data = []

		if (exchange == "gdax"):
			#create connection to client (key, secret, passphrase)
			auth_client = gdax.AuthenticatedClient('ec4af4d834af89078dfa8ce52e487421', 'wYxKIZ8oO8Ntaj8Mq42M7A1L8Z3WM+qeWGnh7V4NSr7cVnUZmoz2VIMhuFHHFvyDt2KyeXGdT0mAZvXzN1tfAA==', 'er2maud6tej')
			print("connected to client")
			#set the start and end times for backtesting in ISO 8601 format
			#get the current date and time in a datetime object
			current_date = datetime.datetime.now()
			#get the number of days from the parameter passed in
			delta = datetime.timedelta(num_days_to_backTest)
			#get the start date in a datetime object
			start_date = current_date - delta
			#convert start and end to iso format to comply with gdax API
			start = start_date.isoformat()
			end = current_date.isoformat()
			#get the historic data for the timeframe
			#granularity is in seconds
			#TODO: handle error if granularity isn't in the set of values accepted by GDAX (60, 300, 900, 3600, 21600, 86400)
			gdax_data = auth_client.get_product_historic_rates('BTC-USD', start=start, end=end, granularity=period)
			print(str(gdax_data))
			for data_point in gdax_data:
				#using price average = (high + low + close)/3
				#TODO: move these hardcoded integers into a constants file
				print(str(data_point))
				priceAverage = (float(data_point[2]) + float(data_point[1]) + float(data_point[4])) / float(3)
				candlestick = BotCandlestick(period, data_point[3], data_point[4], data_point[2], data_point[1], priceAverage, data_point[5])
				candlestick.setTime(data_point[0])
				self.data.append(candlestick)


	def getPoints(self):
		return self.data
