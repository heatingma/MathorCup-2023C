import numpy as np
import pandas as pd
from utils import get_orders, get_lines, get_workers, constant
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
    workers_data = np.load("processed_data/problem_2/workers.npy", allow_pickle=True)
    workers = get_workers(workers_data)
    lines = get_lines(workers)
    time = 0
    assign = pd.read_excel("result/problem_2/assign_results.xlsx", usecols=[3, 5, 7])
    assign = np.array(assign).astype(int)
    while lines.finished == False:  
        if time == 0:
            lines.update_state(time)
            lines.time_zero(assign)
            time += 1
        else:          
            lines.update_state(time)
            lines.next_orders(time)
            time += 1 

    rdf = pd.DataFrame(lines.get_msg(), columns=['产线', '订单ID', '开始时间', '结束时间', '截止时间', \
        '超时时间', '总耗时', '工人'])
    rdf.to_excel("result/problem_3/results_orders.xlsx")
    
    worker_update = np.array(lines.workers.get_msg())    
    data = worker_update[:, 0:13]
    rdf = pd.DataFrame(data, columns=['工人ID', 'Line01', 'Line02', \
        'Line03', 'Line04', 'Line05', 'Line06', 'Line07', 'Line08', \
        'Line09', 'Line10', 'Line11', 'Line12'])
    rdf.to_excel("result/problem_3/初始技能水平.xlsx")

    data = np.concatenate([np.expand_dims(worker_update[:, 0], axis=1), worker_update[:, 13:25]], axis=1)
    rdf = pd.DataFrame(data, columns=['工人ID', 'Line01', 'Line02', \
        'Line03', 'Line04', 'Line05', 'Line06', 'Line07', 'Line08', \
        'Line09', 'Line10', 'Line11', 'Line12'])
    rdf.to_excel("result/problem_3/结束时技能水平.xlsx")
    
    data = np.concatenate([np.expand_dims(worker_update[:, 0], axis=1), 
                           worker_update[:, 13:25].astype(float) - worker_update[:, 1:13].astype(float)], axis=1)
    rdf = pd.DataFrame(data, columns=['工人ID', 'Line01', 'Line02', \
        'Line03', 'Line04', 'Line05', 'Line06', 'Line07', 'Line08', \
        'Line09', 'Line10', 'Line11', 'Line12'])
    rdf.to_excel("result/problem_3/技能升级情况.xlsx")
    
    worker_update = np.array(lines.workers.get_msg_2())
    
    data = worker_update[:, 0:13]
    rdf = pd.DataFrame(data, columns=['工人ID', 'Line01', 'Line02', \
        'Line03', 'Line04', 'Line05', 'Line06', 'Line07', 'Line08', \
        'Line09', 'Line10', 'Line11', 'Line12'])
    rdf.to_excel("result/problem_3/理论培训时长.xlsx")
    
    data = np.concatenate([np.expand_dims(worker_update[:, 0], axis=1), worker_update[:, 13:25]], axis=1)
    rdf = pd.DataFrame(data, columns=['工人ID', 'Line01', 'Line02', \
        'Line03', 'Line04', 'Line05', 'Line06', 'Line07', 'Line08', \
        'Line09', 'Line10', 'Line11', 'Line12'])
    rdf.to_excel("result/problem_3/产线培训时长.xlsx")


def problem_4():
    workers_data = np.load("processed_data/problem_2/workers.npy", allow_pickle=True)
    workers = get_workers(workers_data)
    lines = get_lines(workers)
    time = 0
    assign = pd.read_excel("result/problem_2/assign_results.xlsx", usecols=[3, 5, 7])
    assign = np.array(assign).astype(int)
    while lines.finished == False:  
        if time == 0:
            lines.update_state(time)
            lines.time_zero(assign)
            time += 1
            continue
        if time == 2250:
            constant.important_score()
        elif time == 4500:
            constant.lower_score()
        elif time == 6750:
            lines.workers.del_worker([i+1 for i in range(10)])
            lines.workers.get_new_worker(10)
            constant.important_score()
        elif time == 13500:
            constant.lower_score()
        lines.update_state(time)
        lines.next_orders(time)
        time += 1 

    rdf = pd.DataFrame(lines.get_msg(), columns=['产线', '订单ID', '开始时间', '结束时间', '截止时间', \
        '超时时间', '总耗时', '工人'])
    rdf.to_excel("result/problem_4/results_orders.xlsx")
    
    worker_update = np.array(lines.workers.get_msg())
    
    data = worker_update[:, 0:13]
    rdf = pd.DataFrame(data, columns=['工人ID', 'Line01', 'Line02', \
        'Line03', 'Line04', 'Line05', 'Line06', 'Line07', 'Line08', \
        'Line09', 'Line10', 'Line11', 'Line12'])
    rdf.to_excel("result/problem_4/初始技能水平.xlsx")

    data = np.concatenate([np.expand_dims(worker_update[:, 0], axis=1), worker_update[:, 13:25]], axis=1)
    rdf = pd.DataFrame(data, columns=['工人ID', 'Line01', 'Line02', \
        'Line03', 'Line04', 'Line05', 'Line06', 'Line07', 'Line08', \
        'Line09', 'Line10', 'Line11', 'Line12'])
    rdf.to_excel("result/problem_4/结束时技能水平.xlsx")
    
    data = np.concatenate([np.expand_dims(worker_update[:, 0], axis=1), 
                           worker_update[:, 13:25].astype(float) - worker_update[:, 1:13].astype(float)], axis=1)
    rdf = pd.DataFrame(data, columns=['工人ID', 'Line01', 'Line02', \
        'Line03', 'Line04', 'Line05', 'Line06', 'Line07', 'Line08', \
        'Line09', 'Line10', 'Line11', 'Line12'])
    rdf.to_excel("result/problem_4/技能升级情况.xlsx")
    
    worker_update = np.array(lines.workers.get_msg_2())
    
    data = worker_update[:, 0:13]
    rdf = pd.DataFrame(data, columns=['工人ID', 'Line01', 'Line02', \
        'Line03', 'Line04', 'Line05', 'Line06', 'Line07', 'Line08', \
        'Line09', 'Line10', 'Line11', 'Line12'])
    rdf.to_excel("result/problem_3/理论培训时长.xlsx")
    
    data = np.concatenate([np.expand_dims(worker_update[:, 0], axis=1), worker_update[:, 13:25]], axis=1)
    rdf = pd.DataFrame(data, columns=['工人ID', 'Line01', 'Line02', \
        'Line03', 'Line04', 'Line05', 'Line06', 'Line07', 'Line08', \
        'Line09', 'Line10', 'Line11', 'Line12'])
    rdf.to_excel("result/problem_3/产线培训时长.xlsx")

if __name__ == "__main__":
    # problem_1()
    # problem_2()
    problem_3()
    problem_4()

