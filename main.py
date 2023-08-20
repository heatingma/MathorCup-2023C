import numpy as np
import pandas as pd
from utils import get_orders, get_workers
from models import dmsf, msf, derf, erf, meonf, lip


work_num = [1, 2, 1, 3, 1, 1, 2, 1, 1, 3, 1, 1]

def problem_1():
    models = {'meonf': meonf, 'dmsf': dmsf,'derf': derf, 'msf': msf, 'erf': erf}
    # solve 
    for name, model in models.items():
        for i in range(12):
            data = np.load("processed_data/problem_1/line_{}.npy".format(i+1), allow_pickle=True)
            orders = get_orders(data)
            orders = model(orders)
            result = orders.print()
            df = pd.DataFrame(result, columns=['生产订单', '开始时间', '完工时间', '截止时间', '超时', '总耗时'])
            df.to_excel("result/problem_1/{}/result_{}.xlsx".format(name, i+1))
    
    # statistic
    results = list()
    results_2 = list()
    results_3 = list()
    for name in models.keys():
        part_result = [name]
        part_result_2 = [name]
        part_result_3 = [name]
        for i in range(12):
            data = np.array(pd.read_excel("result/problem_1/{}/result_{}.xlsx".format(name, i+1)))
            part_result.append(np.sum(data[:, 5]))
            part_result_2.append(np.sum(data[:, 6]))
            part_result_3.append(np.sum(data[:, 5]) + np.sum(data[:, 6]))
        part_result.append(np.sum(part_result[1:]))
        results.append(part_result)
        results_2.append(part_result_2)
        results_3.append(part_result_3)
        
    rdf = pd.DataFrame(results, columns=['策略', 'Line01', 'Line02', \
        'Line03', 'Line04', 'Line05', 'Line06', 'Line07', 'Line08', \
        'Line09', 'Line10', 'Line11', 'Line12', 'SUM'])
    rdf.to_excel("result/problem_1/results-overtime.xlsx")

    rdf = pd.DataFrame(results_2, columns=['策略', 'Line01', 'Line02', \
        'Line03', 'Line04', 'Line05', 'Line06', 'Line07', 'Line08', \
        'Line09', 'Line10', 'Line11', 'Line12'])
    rdf.to_excel("result/problem_1/results-sumtime.xlsx")
       
    rdf = pd.DataFrame(results_3, columns=['策略', 'Line01', 'Line02', \
        'Line03', 'Line04', 'Line05', 'Line06', 'Line07', 'Line08', \
        'Line09', 'Line10', 'Line11', 'Line12'])
    rdf.to_excel("result/problem_1/results-overtime-sumtime.xlsx")


def problem_2():
    workers = np.load("processed_data/problem_2/workers.npy", allow_pickle=True)
    times_list = ['sumtime', 'overtime-sumtime']
    
    lines = list() 
    for time in times_list:
        times =  np.load("processed_data/problem_2/{}.npy".format(time), allow_pickle=True)
        result = lip(work_num, workers, times)
        swap = {1.: 'E', 0.8: 'O', 0.: 'N'}   
        for j in range(12):
            cur_line = [time, 'line{}'.format(j+1)]
            for i in range(20):
                if result[i][j]:
                    cur_line.append(i+1)
                    cur_line.append(swap[workers[i][j]])
            lines.append(cur_line)
            
    rdf = pd.DataFrame(lines, columns=['采用的时间', '产线', '工人1', '技能1', \
        '工人2', '技能2', '工人3', '技能3'])
    rdf.to_excel("result/problem_2/assign_results.xlsx")


def problem_3():
    workers = np.load("processed_data/problem_2/workers.npy", allow_pickle=True)
    workers = get_workers(workers)

if __name__ == "__main__":
    problem_1()
    # problem_2()
    # import pdb
    # arr = [10, 20, 30]
    # pdb.set_trace()
    # problem_3()

