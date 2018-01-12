import sys
from threading import Thread
import gdax
import json
import time

class GdaxWebsocketClient(gdax.WebsocketClient):
	def on_open(self):
		#self.url = "wss://ws-feed.gdax.com/"
		#self.products = ["BTC-USD"]
		self.current_price = -1
		print("----- GDAX Websocket Client Connection Opened -----")

	def on_message(self, msg):
		data = json.dumps(msg, indent=4, sort_keys=True)
		if msg.get("type") == "match":
			price = float(msg.get("price", -1))
			if price > 0:
				self.current_price = price

	def on_close(self):
		print("----- GDAX Websocket Client Connection Closed -----")

	def get_current_price(self):
		return self.current_price

#Test for webclient
if __name__ == "__main__":
	wsClient = GdaxWebsocketClient(products=["BTC-USD"], channels=["matches"])
	wsClient.start()
	try:
		while True:
			print("The current price is: " + str(wsClient.get_current_price()))
			time.sleep(1)
	except KeyboardInterrupt:
		wsClient.close()

	if wsClient.error:
		sys.exit(1)
	else:
		sys.exit(0)