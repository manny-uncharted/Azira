import aiozmq
import zmq
import asyncio
import json
import time
import threading
import logging
from cachetools import TTLCache
import requests
import aiohttp

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s ')
logger = logging.getLogger(__name__)


class zmqConn:
    def __init__(self):
        self.pubsocket = None  # Will be initialized asynchronously
        self.runserver = asyncio.Event()
        self.runserver.set()
        self.cache = TTLCache(maxsize=100, ttl=30)  # 30 seconds TTL
        self.tokens = []

    async def _zmq_config(self, port):
        self.pubsocket = await aiozmq.create_zmq_stream(zmq.PUB, bind=f"tcp://*:{port}")
        logger.info(f"pubsocket initialized on port {port}")

    async def refresh_cache(self):
        params = {
            "vs_currency": "usd", 
            "order": "market_cap_desc", 
            "per_page": 100, 
            "page": 1, 
            "sparkline": str(False).lower()
        }
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.coingecko.com/api/v3/coins/markets", 
                params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    # logger.info(f"Refresh cache | Data returned {data}")
                    if data:
                        self.cache['coingecko_data'] = data
                        self.tokens = [coin['symbol'].upper() for coin in data]
                    else:
                        print("Received empty data from CoinGecko.")
                else:
                    print(f"Error fetching data: HTTP Status Code {response.status}")
                    print(f"Response Content: {await response.text()}")

    async def publish_market_data(self):
        if 'coingecko_data' in self.cache and self.pubsocket is not None:
            for token in self.tokens:
                token_data = next((item for item in self.cache['coingecko_data'] if item['symbol'].upper() == token), None)
                if token_data:
                    try:
                        message = f"{token} & {json.dumps({'token': token, 'name': token_data['name'], 'current_price': token_data['current_price'], 'bestbidprice': token_data['high_24h'],'market_cap': token_data['market_cap'], 'bestaskprice': token_data['low_24h']})}"
                        # logger.info(f"Message to be encoded: {message} and TYPE: {type(message)}")
                        self.pubsocket.write([message.encode()])
                    except Exception as e:
                        pass
                        # logger.error(f"Error in publish_market_data for token {token}: {e}", exc_info=True)
                await asyncio.sleep(0.2)
        else:
            logger.warning("pubsocket is not initialized or coingecko_data not in cache")

    async def load_data(self):
        while self.runserver.is_set():
            if self.pubsocket is not None:
                try:
                    if 'coingecko_data' not in self.cache:
                        logger.info("Refreshing cache...")
                        await self.refresh_cache()
                    if 'coingecko_data' in self.cache:
                        await self.publish_market_data()
                    else:
                        logger.info("Cache does not contain 'coingecko_data', waiting for next refresh...")
                except Exception as e:
                    pass
                    # logger.error(f"Error in load_data: {e}", exc_info=True)
                await asyncio.sleep(0.1)
            else:
                logger.info(f"pubsocket is not initialized and the value is == {self.pubsocket}")
    


    async def stop(self):
        self.runserver.clear()
        if self.pubsocket:
            self.pubsocket.close()

    async def server_setup(self, serverport):
        socket = await aiozmq.create_zmq_stream(zmq.REP, bind=f"tcp://*:{serverport}")
        while self.runserver.is_set():
            try:
                message_bytes = await socket.read()
                print(f"Message bytes: {message_bytes}")
                message_str = message_bytes.decode()
                message_json = json.loads(message_str)
                print(f"JSON Decoded message format: {message_json}")

                message_json.update({"port": serverport})
                try:
                    resprecv = self.functions[message_json['function']](message_json)
                    resp = {"status": True, "error": False, "data": [resprecv], "message": "Data Received."}
                except Exception as e:
                    resp = {"status": False, "error": True, "message": str(e)}

                await socket.write(json.dumps(resp).encode())
            except json.JSONDecodeError as e:
                await socket.write(json.dumps({"status": False, "error": True, "message": f"JSON decode error: {e}"}).encode())
            except Exception as e:
                await socket.write(json.dumps({"status": False, "error": True, "message": str(e)}).encode())

            await asyncio.sleep(0.1)


# """
# NOTE: I have noticed an error in this implementation above, as the goal here would be to convert this application to a library.
# One that allows people to build distributed communications systems from simple messaging servers that act standalone to highly complex ones, using kafka, amqp, zeromq.

# A better way to optimize things is to allow people choose what communication protocol they want:
# - req/rep
# - pub/sub


# This project would evolve into two phases: 
# 1. Azira & AziraClient: A library that allows you to receive near real-time stream of tokens on the exchange market.
# 2. #TODO: Need a name: A library that allows you to build distributed communication systems with ease, from simple messaging servers, to complex ones, using various messaging brokers, kafka, amqp, zeromq.
# """