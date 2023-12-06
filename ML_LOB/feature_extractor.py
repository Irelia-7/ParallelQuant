import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from dataset import One_Order_Book

def get_data(order_book, N):
    price = []
    bid1_price = []
    ask1_price = []
    timeline = []

    end_flag = 0
    order_book.begin()
    while not end_flag:
        return_dict, end_flag = order_book.get_next_data(N)
        price.append(return_dict['price'])
        bid1_price.append(return_dict['bid_price'][0])
        ask1_price.append(return_dict['ask_price'][0])
        timeline.append(return_dict['time'])
        # state_volume = return_dict['trade_volume']
        
    return price, bid1_price, ask1_price, timeline

# 自定义训练标签，0代表空仓，1代表多仓
# 信息获取间隔为1，trade操作的时间单位为7: 若当前bid_price高于未来expect_period时间内ask price的最小值，则认为此时买入可以在较短时间fill
def get_trade_label(time, bid, ask, start, end, period, fee = 0.01):
    label = []
    
    time_np = np.array(time)
    index_start = np.where(time_np >= start)[0][0]
    index_end = np.where(time_np <= end)[0][-1]
    for i in range(index_start, index_end + 1, 1):
        index = np.where(time_np <= time_np[i] + 7 * period)[0][-1]
        if bid[i] > min(ask[i: index + 1] + fee): label.append(1)
        else: label.append(0) 
    return label

def rise_ask(Ask1,timestamp, before_time):
    rise_ratio = []
    index = np.where(timestamp >= before_time)[0][0]
    #open first before_time mins
    for i in range(0,index,1):
        rise_ratio_ = round((Ask1[i] - Ask1[0])*(1.0)/Ask1[0]*100,5)
        rise_ratio.append(rise_ratio_)
    # for i in range(index,len(Ask1),1):
    #     #print np.where(timestamp_time_second[:i] >= timestamp_time_second[i] - before_time)
    #     #print timestamp_time_second[i],timestamp_time_second[i] - before_time
    #     index_start = np.where(timestamp_time_second[:i] >= timestamp_time_second[i] - before_time)[0][0]
    #     rise_ratio_ = round((Ask1[i] - Ask1[index_start])*(1.0)/Ask1[index_start]*100,5)
    #     rise_ratio.append(rise_ratio_)
    return np.array(rise_ratio)

if __name__ == "__main__":
    order_book = One_Order_Book(name = 'stock_23.jsonl')
    price, bid1_price, ask1_price, timeline = get_data(order_book, len(order_book))
    trade_label = get_trade_label(timeline, bid1_price, ask1_price, 0, timeline[-1], 10)

    plt.figure(figsize=(20,16))
    plt.subplot(211)
    plt.plot(timeline, price, color = 'g', label = 'Price')
    plt.plot(timeline, ask1_price, color = 'b', label = 'Ask1')
    plt.plot(timeline, bid1_price, color = 'r', label = 'Bid1')
    plt.ylabel("Price")
    plt.legend(loc = 1)

    plt.subplot(212)
    plt.grid()
    plt.ylim(-0.5, 1.5)
    plt.plot(timeline, trade_label, color = 'b')
    plt.ylabel("Traded Label")
    plt.savefig("./test.jpg")
    plt.show()
