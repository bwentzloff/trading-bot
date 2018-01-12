import sys, getopt

from backfiller import Backfiller
from botstrategy import BotStrategy

def main(argv):
	chart = Backfiller("gdax","BTC_USD",3600)

	strategy = BotStrategy()

	for candlestick in chart.getPoints():
		strategy.tick(candlestick)

if __name__ == "__main__":
	main(sys.argv[1:])