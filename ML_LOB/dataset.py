import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os

class One_Order_Book:
    def __init__(self, date='12-03-25', name='stock_27.jsonl'):
        url = "/home/qinry/ubiquant_trading_competition/dataset/collected_data/2023-" + date + '/' + name
        self.df = pd.read_json(url, lines=True)
        # print(df)
    def __len__(self):
        return len(self.df)
    def begin(self):
        self.current_idx = 0
    def get_next_data(self, N):
        time = self.df.iloc[self.current_idx]['lob']['localtime']
        price = self.df.iloc[self.current_idx]['lob']['last_price']
        bid_price = self.df.iloc[self.current_idx]['lob']['bidprice'][0:3]
        bid_volume = self.df.iloc[self.current_idx]['lob']['bidvolume'][0:3]
        ask_price = self.df.iloc[self.current_idx]['lob']['askprice'][0:3]
        ask_volume = self.df.iloc[self.current_idx]['lob']['askvolume'][0:3]
        trade_volume = self.df.iloc[self.current_idx]['lob']['trade_volume']
        # print(price)
        # next_price = self.df.iloc[self.current_idx+1]['lob']['last_price'] if self.current_idx < self.__len__()-1 else price
        self.current_idx += 1
        # return {'price':price, 'next_price':next_price, 'bid_volume':bid_volume, 'ask_price':ask_price, \
        #     'ask_volume':ask_volume, 'bid_price':bid_price}, self.current_idx == self.__len__()
        return {'time':time, 'price':price, 'bid_volume':bid_volume, 'ask_price':ask_price, 'ask_volume':ask_volume, \
                'bid_price':bid_price, 'trade_volume':trade_volume}, self.current_idx == N
    def show(self):
        print(self.df.iloc[self.current_idx]['lob'])
        print(self.df.iloc[self.current_idx]['lob']['localtime'])
        print(self.df.iloc[self.current_idx]['lob']['askprice'][0:3])

def get_data1(order_book, N):
    price = []
    bid1_price = []
    ask1_price = []
    bid1_volume = []
    ask1_volume = []
    timeline = []

    end_flag = 0
    order_book.begin()
    while not end_flag:
        return_dict, end_flag = order_book.get_next_data(N)
        price.append(return_dict['price'])
        bid1_price.append(return_dict['bid_price'][0])
        ask1_price.append(return_dict['ask_price'][0])
        bid1_volume.append(return_dict['bid_volume'][0])
        ask1_volume.append(return_dict['ask_volume'][0])
        timeline.append(return_dict['time'])
        # state_volume = return_dict['trade_volume']
        
    return np.array(timeline), np.array(price), np.array(bid1_price), np.array(ask1_price), \
        np.array(bid1_volume), np.array(ask1_volume)

def get_data_m(order_book, N):
    bid2_price = []
    ask2_price = []
    bid2_volume = []
    ask2_volume = []
    bid3_price = []
    ask3_price = []
    bid3_volume = []
    ask3_volume = []

    end_flag = 0
    order_book.begin()
    while not end_flag:
        return_dict, end_flag = order_book.get_next_data(N)
        bid2_price.append(return_dict['bid_price'][1])
        ask2_price.append(return_dict['ask_price'][1])
        bid2_volume.append(return_dict['bid_volume'][1])
        ask2_volume.append(return_dict['ask_volume'][1])
        bid3_price.append(return_dict['bid_price'][2])
        ask3_price.append(return_dict['ask_price'][2])
        bid3_volume.append(return_dict['bid_volume'][2])
        ask3_volume.append(return_dict['ask_volume'][2])
        # state_volume = return_dict['trade_volume']
    return np.array(bid2_volume), np.array(bid3_volume), np.array(ask2_volume), np.array(ask3_volume), \
        np.array(bid2_price), np.array(bid3_price), np.array(ask2_price), np.array(ask3_price)