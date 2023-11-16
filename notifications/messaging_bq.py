import zmq 
import random 
import json 
import time
import notifier
import threading
import requests
from cachetools import TTLCache

class zmqConn():
    def __init__(self):
        self.pubsocket = self.__zmq_config(5556)
        self.functions = {
            "addto_Feed": self.addto_Feed,
            "terminate": self.terminate
        }
        self.tokens = []
        self.load = True
        self.runserver = True
        self.cache = TTLCache(maxsize=100, ttl=30)  # 30 seconds TTL
        threading.Thread(target=self.load_data, daemon=True).start()
        self.server_setup("5558")

    def __zmq_config(self, port):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind(f"tcp://*:{port}")
        return socket
    
    def addto_Feed(self, values):
        payload = values.get('payload')
        if payload == None: 
            raise Exception("payload missing")
        else: 
            tokens = payload['tokens']
            for t in tokens: 
                if t not in self.tokens:
                    self.tokens.append(t)
                
    def load_data(self):
        while self.load:
            try:
                if 'coingecko_data' not in self.cache:
                    print("Refreshing cache...")
                    self.refresh_cache()
                if 'coingecko_data' in self.cache:
                    self.publish_market_data()
                else:
                    print("Cache does not contain 'coingecko_data', waiting for next refresh...")
            except Exception as e:
                print(f"Error in load_data: {e}")
            time.sleep(0.1)

            
    def refresh_cache(self):
        try:
            response = requests.get("https://api.coingecko.com/api/v3/coins/markets",
                params={"vs_currency": "usd", "order": "market_cap_desc",
                        "per_page": 100, "page": 1, "sparkline": False},
                timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data:
                    self.cache['coingecko_data'] = data
                    self.tokens = [coin['symbol'].upper() for coin in data]
                    # print(f"Received the following {self.cache['coingecko_data']} and Tokens: {self.tokens}")
                else:
                    print("Received empty data from CoinGecko.")
            else:
                print(f"Error fetching data: HTTP Status Code {response.status_code}")
                print(f"Response Content: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

    def publish_market_data(self):
        if 'coingecko_data' in self.cache:
            for token in self.tokens:
                token_data = next((item for item in self.cache['coingecko_data'] if item['symbol'].upper() == token), None)
                if token_data:
                    self.pubsocket.send_string(f"{token} & {json.dumps({'token': token, 'name': token_data['name'], 'current_price': token_data['current_price'], 'bestbidprice': token_data['high_24h'],'market_cap': token_data['market_cap'], 'bestaskprice': token_data['low_24h']})}")
                time.sleep(0.2)
    
    def exit_app(self, timer = 2):
        time.sleep(timer)
        self.runserver = False
        self.load = False
        try: 
            self.context.destroy()
        except:pass

    def terminate(self, values):
        t1 = threading.Thread(target = self.exit_app).start()
        values.update({"exit" : "True"})
        return values
    
    def server_setup(self, serverport): 
        self.context = zmq.Context()
        socket = self.context.socket(zmq.REP)
        socket.bind("tcp://*:%s" % serverport)
        while self.runserver : 
            message = socket.recv().decode()
            try : 
                print(message)
                notifier.notification.delay(message)
                message = json.loads(message)
                message.update({"port" : serverport})
                try :  
                    resprecv = self.functions[message['function']](message)
                    resp = {"status" : True, "error" : False, "data" : [resprecv], "message" : "Data Received."}
                except Exception as e :
                    resp = {"status" : False, "error" : True,"message" : str(e)}
                socket.send(json.dumps(resp).encode())
            except Exception as e : 
                socket.send(json.dumps({"status" : False, "error" : True, "message" : str(e)}).encode())
            time.sleep(0.1)

zq = zmqConn()
# zq.refresh_cache()


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