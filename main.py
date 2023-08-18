import numpy as np
import pandas as pd
from utils import get_orders
from models import edf
import pdb

work_num = [1, 2, 1, 3, 1, 1, 2, 1, 1, 3, 1, 1]

for i in range(12):
    data = np.load("processed_data/problem_1/line_{}.npy".format(i+1), allow_pickle=True)
    orders = get_orders(data)
    orders = edf(orders, work_num[i])
    result = orders.print()
    df = pd.DataFrame(result, columns=['生产订单', '开始时间', '完工时间', '截止时间', '超时'])
    df.to_excel("result/problem_1/result_{}.xlsx".format(i+1))

