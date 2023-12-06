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
        ask_price = self.df.iloc[self.current_idx]['lob']['askprice'][0:3]
        ask_volume = self.df.iloc[self.current_idx]['lob']['askvolume'][0:3]
        bid_price = self.df.iloc[self.current_idx]['lob']['bidprice'][0:3]
        bid_volume = self.df.iloc[self.current_idx]['lob']['bidvolume'][0:3]
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

    
    def _get_data(self):
        path = os.sep.join(['第三期股票模拟交易所', 'dataset', str(self.day), self.name])
        data = pd.read_csv(path)
        
        self.price_list = data['LastPrice'].tolist()
        # idx = sum(np.array(self.price_list)==0)
        self.time_list = data['LocalTime'].tolist()
        self.trade_volume = data['TradeVolume'].tolist()
        self.trade_value = data['TradeValue'].tolist()
        bid_query = data.columns[4:14]
        ask_query = data.columns[14:24]
        self.bid_price = data[bid_query]
        self.ask_price = data[ask_query]
        self.bid_volume = data[data.columns[24:34]]
        self.ask_volume = data[data.columns[34:44]]

        # print(self.ask_volume.loc[1].tolist())
        return 



class One_stock_true:
    def __init__(self, name='stock_27.jsonl'):
        self.df = pd.read_json(name, lines=True)
        # print(df)
    def __len__(self):
        return len(self.df)
    def begin(self):
        self.current_idx = 0
    def get_next_data(self):
        price = self.df.iloc[self.current_idx]['lob']['last_price']
        ask_price = self.df.iloc[self.current_idx]['lob']['askprice']
        ask_volume = self.df.iloc[self.current_idx]['lob']['askvolume']
        bid_price = self.df.iloc[self.current_idx]['lob']['bidprice']
        bid_volume = self.df.iloc[self.current_idx]['lob']['bidvolume']
        # print(price)
        next_price = self.df.iloc[self.current_idx+1]['lob']['last_price'] if self.current_idx < self.__len__()-1 else price
        self.current_idx += 1
        return {'price':price, 'next_price':next_price, 'bid_volume':bid_volume, 'ask_price':ask_price, \
            'ask_volume':ask_volume, 'bid_price':bid_price}, self.current_idx == self.__len__()




if __name__ == '__main__':
    dataset = One_stock_true()
    price_list = []
    end_flag = 0
    dataset.begin()
    while not end_flag:
        return_dict, end_flag = dataset.get_next_data()
        # print
        price = return_dict['price']
        # print(price)
        price_list.append(price)
    
    plt.plot(price_list)
    plt.show()