import sys, getopt
import time

from botchart import BotChart
from botstrategy import BotStrategy
from botlog import BotLog
from botcandlestick import BotCandlestick
from gdaxwebsocketclient import GdaxWebsocketClient

def main(argv):
	strategy = BotStrategy(mode="LIVE")

	wsClient = GdaxWebsocketClient(products=["BTC-USD"], channels=["matches"])
	wsClient.start()
	
	#wait 10 seconds to let the web client connect
	time.sleep(int(10))

	candlesticks = []
	developingCandlestick = BotCandlestick()

	while True:
		try:
			currentPrice = wsClient.get_current_price()
			print("The current price is: " + str(currentPrice))
			developingCandlestick.tick(currentPrice)
		except:
			print("Error reading current price from websocket client: " + sys.exec_info()[0])

		#if (developingCandlestick.isClosed()):
		#more efficient, checking a class variable rather than calling a function each time
		if (developingCandlestick.closed == True):
			candlesticks.append(developingCandlestick)
			strategy.tick(developingCandlestick)
			developingCandlestick = BotCandlestick()
		
		time.sleep(int(5))

if __name__ == "__main__":
	main(sys.argv[1:])