from resources.api_request import client_request
from bingx.monitor import bingx_monitor

if __name__ == "__main__":
    price = bingx_monitor.get_market_price()
