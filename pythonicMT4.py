# -*- coding: utf-8 -*-
"""
Created on Mon Apr 30 20:15:31 2018
@author: Ars
"""
import zmq
import numpy as np
class zmq_python():
    
    def __init__(self):
        # Create ZMQ Context
        self.context = zmq.Context()

        # Create REQ Socket
        self.reqSocket = self.context.socket(zmq.REQ)
        self.reqSocket.connect("tcp://localhost:5555")

        # Create PULL Socket
        self.pullSocket = self.context.socket(zmq.PULL)
        self.pullSocket.connect("tcp://localhost:5556")
    
    def remote_send(self, socket, data):
    
        try:
            socket.send_string(data)
            msg_send = socket.recv_string()
            print (msg_send)

        except zmq.Again as e:
            print ("Waiting for PUSH from MetaTrader 4..")
            
    def remote_pull(self, socket):
    
        try:
            msg_pull = socket.recv(flags=zmq.NOBLOCK)
            return msg_pull

        except zmq.Again as e:
            print ("Waiting for PUSH from MetaTrader 4..")
            
    
    def get_data(self, symbol, timeframe, start_bar, end_bar):
        '''
        only start_bar and end_bar as int
        '''
        self.data = "DATA|"+ symbol+"|"+"PERIOD_"+timeframe+"|"+str(start_bar)+"|"+str(end_bar+1)
        self.remote_send(self.reqSocket, self.data)
        prices= self.remote_pull(self.pullSocket)
        prices_str= str(prices)
        price_lst= prices_str.split(sep='|')[1:-1]
        price_lst= [float(i) for i in price_lst]
        price_lst= price_lst[::-1]
        price_arr= np.array(price_lst)
        return price_arr
    
    def buy_order(self, symbol, stop_loss, take_profit):
        self.buy= "TRADE|OPEN|0|"+ str(symbol)+"|"+str(stop_loss)+"|"+str(take_profit)
        self.remote_send(self.reqSocket, self.buy)
        reply= self.remote_pull(self.pullSocket)
        return reply
    
    def sell_order(self, symbol, stop_loss, take_profit):
        self.buy= "TRADE|OPEN|1|"+ str(symbol)+"|"+str(stop_loss)+"|"+str(take_profit)
        self.remote_send(self.reqSocket, self.buy)
        reply= self.remote_pull(self.pullSocket)
        return reply
    
    def close_buy_order(self):
        self.close_buy= "TRADE|CLOSE|0"
        self.remote_send(self.reqSocket, self.close_buy)
        reply= self.remote_pull(self.pullSocket)
        return reply
    
    def close_sell_order(self):
        self.close_sell= "TRADE|CLOSE|1"
        self.remote_send(self.reqSocket, self.close_sell)
        reply= self.remote_pull(self.pullSocket)
        return reply