import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Rise Ratio
def rise_ask(time, ask, before_time):
    rise_ratio = []
    index = np.where(time >= before_time)[0][0]
    for i in range(index):
        ratio = round((ask[i] - ask[0])/ask[0] * 100, 5)
        rise_ratio.append(ratio)
    for i in range(index, len(ask), 1):
        index_moving = np.where(time[:i] >= time[i] - before_time)[0][0]
        ratio = round((ask[i] - ask[index_moving])/ask[index_moving] * 100, 5)
        rise_ratio.append(ratio)
    return rise_ratio

# Weighted OBI & Depth Ratio
def weighted_OBI(time, start, end, bid1, bid2, bid3, ask1, ask2, ask3, weight = [0.5, 0.3, 0.2]):
    index_start = np.where(time >= start)[0][0]
    index_end = np.where(time <= end)[0][-1]
    weighted_ask = weight[0] * ask1[index_start: index_end + 1] + weight[1] * ask2[index_start: index_end + 1] + \
        weight[2] * ask3[index_start: index_end + 1]
    weighted_bid = weight[0] * bid1[index_start: index_end + 1] + weight[1] * bid2[index_start: index_end + 1] + \
        weight[2] * bid3[index_start: index_end + 1]
    weighted_depth_ratio = weighted_ask/weighted_bid
    OBI = (weighted_ask - weighted_bid)/(weighted_ask + weighted_bid)
    return OBI, weighted_depth_ratio

# TODO: Generate data
# 完善Label标注，同时生成训练数据
# 注意所有可调参数：预期最长fill时间-traded_time, rise_ratio的before time, Depth权重
def generate_factor(time, start, end, ask1_price, before_time, ask1_v, ask2_v, ask3_v, bid1_v, bid2_v, bid3_v):
    # 生成rise_ratio, 采用多种超参
    rise_ratio = []
    for i in range(5):
        index_start = np.where(time >= start)[0][0]
        index_end = np.where(time <= end)[0][-1]
        rise = rise_ask(time, ask1_price, before_time[i])
        rise_ratio.append(rise[index_start: index_end+1])
    
    # 自定权重选择
    weights = [[1, 0, 0], [0.9, 0.1, 0], [0.8, 0.2, 0], [0.7, 0.2, 0.1], [0.5, 0.3, 0.2], [0, 1, 0], [0, 0, 1]]
    w_OBI = []
    w_depth = []
    for i in range(7):
        OBI, depth = weighted_OBI(time, start, end, bid1_v, bid2_v, bid3_v, ask1_v, ask2_v, ask3_v, weights[i])
        w_OBI.append(OBI)
        w_depth.append(depth)

    return np.array(rise_ratio), np.array(w_OBI), np.array(w_depth)

# TODO: Generate label
def get_trade_label(time, bid, ask, start, end, period, fee = 0.01):
    label = []
    index_start = np.where(time >= start)[0][0]
    index_end = np.where(time <= end)[0][-1]
    for i in range(index_start, index_end + 1, 1):
        index = np.where(time <= time[i] + 7 * period)[0][-1]
        if bid[i] > (min(ask[i: index + 1]) + fee): label.append(1)
        else: label.append(0)
    return label