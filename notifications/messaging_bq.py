# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 13:02:28 2023

@author: Niraj
"""

import zmq 
import random 
import json 
import time
import notifier
import threading

class zmqConn():
    def __init__(self):
        self.pubsocket = self.__zmq_config(5556)
        self.functions = {
                            "addto_Feed" : self.addto_Feed,
                            "terminate" : self.terminate
                          }
        self.tokens = ["NSE:26009", "NSE:26000", "NSE:212", "NSE:230"]
        self.load = True
        self.runserver = True
        threading.Thread(target = self.load_data).start()
        self.server_setup("5558")
        
    def __zmq_config(self, port):
        context = zmq.Context()
        socket = context.socket(zmq.PUB)
        socket.bind("tcp://*:%s" % port)
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
            self.get_ltp()
            time.sleep(0.1)
            
    def get_ltp(self):
        for i in self.tokens:
            ltp = random.randint(500, 520)
            self.pubsocket.send_string("{topic} & {marketdata}".format(topic = i, marketdata = json.dumps({"token" : i, "ltp" : ltp, "bestbidprice" : ltp - 0.5,
                                                                                                           "bestaskprice" : ltp + 0.5})))
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
