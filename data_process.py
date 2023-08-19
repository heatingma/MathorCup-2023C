import pandas as pd
import numpy as np
import pdb

def divide_data():
    """
    divide data to 12 lines
    """
    df = pd.read_excel("data/1 - 生产订单.xlsx", usecols=np.r_[0:5])
    data = np.array(df)
    lines = dict()
    for i in range(12):
        lines[i] = list()        
    for order in data:
        lines[int(order[4][-2:]) - 1].append(order)
    for i in range(12):
        np.save("processed_data/problem_1/line_{}".format(i+1), lines[i])
        lines[i] = pd.DataFrame(data=lines[i], columns=df.columns)
        lines[i].to_excel("processed_data/problem_1/line_{}.xlsx".format(i+1))


def get_result_from_problem_1():
    data = pd.read_excel("result/problem_1/results.xlsx")
    data = np.array(data)[0][2:-1].astype(int)
    np.save("processed_data/problem_2/overtimes.npy", data)
    

def get_workers():
    data = pd.read_excel("data/2 - 生产员工技能表.xlsx", usecols=np.r_[1:13])
    data = np.array(data)[1:]
    swap = {'E': 1.0, 'O': 0.8, 'N': 0.0}
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            data[i][j] = swap[data[i][j]]
    data = data.astype(float)
    np.save("processed_data/problem_2/workers.npy", data)


if __name__ == "__main__":
    divide_data()
    get_result_from_problem_1()
    get_workers()