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
			#TODO: handle error if granularity isn't in the set of values accepted by GDAX (60, 300, 900, 3600, 21600, 86400)
			#create connection to client (key, secret, passphrase)
			auth_client = gdax.AuthenticatedClient('ec4af4d834af89078dfa8ce52e487421', 'wYxKIZ8oO8Ntaj8Mq42M7A1L8Z3WM+qeWGnh7V4NSr7cVnUZmoz2VIMhuFHHFvyDt2KyeXGdT0mAZvXzN1tfAA==', 'er2maud6tej')
			print("connected to client")
			#get the current date and time in a datetime object
			end_date = datetime.datetime.now()
			#86400 seconds in a day
			#compute the number of points required per day at this granularity
			numPointsPerDay = (86400/period)
			#GDAD API limits number of points returned per request to 350
			#compute the number of requests needed per day
			numRequestsPerDay = numPointsPerDay/350
			#And the amount of time to cover with each request
			delta = datetime.timedelta(1/numRequestsPerDay)
			#get the number of days from the parameter passed in
			backtestingTimeframe = datetime.timedelta(num_days_to_backTest)
			#get the start date in a datetime object
			previous_date = end_date - backtestingTimeframe
			current_date = previous_date + delta
			print("Collecting data from " + str(previous_date) + " to " + str(end_date))
			while current_date < end_date:
				#convert start and end to iso format to comply with gdax API
				start = previous_date.isoformat()
				end = current_date.isoformat()
				gdax_data = auth_client.get_product_historic_rates('BTC-USD', start=start, end=end, granularity=period)
				for data_point in reversed(gdax_data):
					#using price average = (high + low + close)/3
					#TODO: move these hardcoded integers into a constants file
					#print(str(data_point))
					priceAverage = (float(data_point[2]) + float(data_point[1]) + float(data_point[4])) / float(3)
					candlestick = BotCandlestick(period, data_point[3], data_point[4], data_point[2], data_point[1], priceAverage, data_point[5])
					candlestick.setTime(data_point[0])
					self.data.append(candlestick)
			
				previous_date = current_date + datetime.timedelta(period/86400)
				current_date = previous_date + delta
			
			
			start = previous_date.isoformat()
			end = end_date.isoformat()
			gdax_data = auth_client.get_product_historic_rates('BTC-USD', start=start, end=end, granularity=period)
			for data_point in reversed(gdax_data):
				#using price average = (high + low + close)/3
				#TODO: move these hardcoded integers into a constants file
				#print(str(data_point))
				priceAverage = (float(data_point[2]) + float(data_point[1]) + float(data_point[4])) / float(3)
				candlestick = BotCandlestick(period, data_point[3], data_point[4], data_point[2], data_point[1], priceAverage, data_point[5])
				candlestick.setTime(data_point[0])
				self.data.append(candlestick)

			


	def getPoints(self):
		return self.data
