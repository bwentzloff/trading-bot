import sys, getopt
import time

from botchart import BotChart
from botstrategy import BotStrategy

def main(argv):
	chart = BotChart("poloniex","BTC_XMR",300,False)

	strategy = BotStrategy()

	while True:
		candlestick = chart.getCurrentPrice()
		strategy.tick(candlestick)
		time.sleep(int(10))

if __name__ == "__main__":
	main(sys.argv[1:])
