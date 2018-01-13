import sys, getopt
import datetime
from backfiller import Backfiller
from botstrategy import BotStrategy

import matplotlib.pyplot as plt

def main(argv):
	chart = Backfiller("gdax","BTC_USD",300, 5)

	starting_balance=1000

	strategy = BotStrategy(starting_balance_currency=1000)

	candlesticks = chart.getPoints()

	x = []
	y = []

	for candlestick in candlesticks:
		time = (datetime.datetime.utcfromtimestamp(candlestick.endTime) - datetime.timedelta(hours=5))
		x.append(time)
		y.append(candlestick.priceAverage)
		print(time)
		strategy.tick(candlestick)

	strategy.showAllTrades()

	buy_times = []
	buy_prices = []
	sell_times = []
	sell_prices = []

	for trade in strategy.trades:
		b_time = (datetime.datetime.utcfromtimestamp(trade.openTime) - datetime.timedelta(hours=5))
		buy_times.append(b_time)
		buy_prices.append(trade.entryPrice)
		if trade.closeTime is not None:
			s_time = (datetime.datetime.utcfromtimestamp(trade.closeTime) - datetime.timedelta(hours=5))
			sell_times.append(s_time)
			sell_prices.append(trade.exitPrice)
		

	print("Final currency amount: " + str(strategy.balance_currency) + " Final asset amount: " + str(strategy.balance_asset))
	value = strategy.balance_currency + strategy.currentPrice*strategy.balance_asset
	print("Final value in currency: " + str(value))
	print("Percent change: " + str((value - starting_balance)/starting_balance))

	start_price = candlesticks[0].priceAverage
	end_price = candlesticks[len(candlesticks)-1].priceAverage
	percent_change_market = (strategy.currentPrice - strategy.startingPrice)/strategy.startingPrice
	print("Market performance over same period: " + str(percent_change_market))

	plt.plot(x,y, label="BTC Price in USD")
	plt.scatter(buy_times, buy_prices, label="BUYS", marker="^", color='tab:green')
	plt.scatter(sell_times, sell_prices, label="SELLS", marker="v", color='tab:red')
	plt.xlabel("Time")
	plt.ylabel("Price")
	plt.gcf().autofmt_xdate()
	plt.legend()
	plt.show()

if __name__ == "__main__":
	main(sys.argv[1:])