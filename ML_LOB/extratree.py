import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import recall_score, precision_score

import dataset
import factor

if __name__ == "__main__":
    order_book = dataset.One_Order_Book('12-08-12', 'stock_17.jsonl')
    timeline, price, bid1_price, ask1_price, bid1_volume, ask1_volume = dataset.get_data1(order_book, len(order_book))
    bid2_volume, bid3_volume, ask2_volume, ask3_volume, _, _, _, _ = dataset.get_data_m(order_book, len(order_book))
    
    before_time = [100, 200, 300, 400, 500]
    period = 40
    rise_ratio, w_OBI, w_depth = factor.generate_factor(timeline, 0, 14400, ask1_price, before_time, ask1_volume, \
                                                        ask2_volume, ask3_volume, bid1_volume, bid2_volume, bid3_volume)
    true_label = factor.get_trade_label(timeline, bid1_price, ask1_price, 0, 14400, period)
    train_stop = 10000

    model = ExtraTreesClassifier(n_estimators = 10, max_depth =10, min_samples_split = 2, criterion = 'entropy', \
                                 min_samples_leaf = 3)
    index = np.where(timeline <= train_stop)[0][-1]
    train_X = np.concatenate((rise_ratio[:, 0:index+1], w_OBI[:, 0:index+1], w_depth[:, 0:index+1]), axis = 0)
    train_label = true_label[0:index + 1]

    test_X = np.concatenate((rise_ratio[:, index+1:], w_OBI[:, index+1:], w_depth[:, index+1:]), axis = 0)
    model.fit(np.transpose(train_X), train_label)
    label_pred = model.predict(np.transpose(test_X))
    print("Accuracy: " + str(model.score(np.transpose(test_X), true_label[index+1:])))
    L = len(true_label[index+1:])
    print("Recall: " + str(recall_score(label_pred, true_label[index+1:])))
    print("Precision: " + str(precision_score(label_pred, true_label[index+1:])))

    plt.grid()
    plt.ylim(-0.5, 1.5)
    plt.plot(timeline[index+1:], true_label[index+1:], color = 'b')
    plt.ylabel("Traded Label")
    plt.savefig("./test_label.jpg")