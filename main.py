import numpy as np
import pandas as pd
from utils import get_orders
from models import dmlf, mlf, derf, erf, meonf


work_num = [1, 2, 1, 3, 1, 1, 2, 1, 1, 3, 1, 1]

def problem_1():
    models = {'meonf': meonf, 'dmlf': dmlf,'derf': derf, 'mlf': mlf, 'erf': erf}
    # solve 
    for name, model in models.items():
        for i in range(12):
            data = np.load("processed_data/problem_1/line_{}.npy".format(i+1), allow_pickle=True)
            orders = get_orders(data)
            orders = model(orders, work_num[i])
            result = orders.print()
            df = pd.DataFrame(result, columns=['生产订单', '开始时间', '完工时间', '截止时间', '超时', '总耗时'])
            df.to_excel("result/problem_1/{}/result_{}.xlsx".format(name, i+1))
    
    # statistic
    results = list()
    for name in models.keys():
        part_result = [name]
        for i in range(12):
            data = np.array(pd.read_excel("result/problem_1/{}/result_{}.xlsx".format(name, i+1)))
            part_result.append(np.sum(data[:, 5]))
        part_result.append(np.sum(part_result[1:]))
        results.append(part_result)
    results = pd.DataFrame(results, columns=['策略', 'Line01', 'Line02', 'Line03', 'Line04', 'Line05', 'Line06',
                                            'Line07', 'Line08', 'Line09', 'Line10', 'Line11', 'Line12', 'SUM'])
    results.to_excel("result/problem_1/results.xlsx")

if __name__ == "__main__":
    problem_1()

