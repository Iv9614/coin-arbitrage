import time
import hmac
from hashlib import sha256

from resources.api_request import client_request
import config


class BingxMarketMonitor:
    def __init__(self) -> None:
        self.get_market_price_api = "/openApi/swap/v1/ticker/price"

    # @staticmethod
    def __get_sign(self, api_secret, payload):
        signature = hmac.new(
            api_secret.encode("utf-8"), payload.encode("utf-8"), digestmod=sha256
        ).hexdigest()

        return signature

    def get_market_price(self):
        paramsMap = {}
        paramsStr = self.parseParam(paramsMap)

        url = "{}?{}&signature={}".format(
            self.get_market_price_api,
            paramsStr,
            self.__get_sign(config.get("API_SECRET"), paramsStr),
        )
        api_response = client_request.get(url)

        return api_response

    def parseParam(self, paramsMap):
        sortedKeys = sorted(paramsMap)
        paramsStr = "&".join(["%s=%s" % (x, paramsMap[x]) for x in sortedKeys])
        if paramsStr != "":
            return paramsStr + "&timestamp=" + str(int(time.time() * 1000))
        else:
            return paramsStr + "timestamp=" + str(int(time.time() * 1000))


bingx_monitor = BingxMarketMonitor()

# if __name__ == "__main__":
#     market_monitor = BingxMarketMonitor()
#     market_monitor.get_market_price()
