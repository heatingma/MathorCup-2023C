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
    
    
if __name__ == "__main__":
    divide_data()