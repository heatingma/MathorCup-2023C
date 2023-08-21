from utils import ORDERS, ORDER, PRODUCT, LINES, WORKER, WORKERS
import numpy as np
import pulp

###############################################
#             Models for Problem 1            #
###############################################

def meonf(orders:ORDERS):
    """
    Min Excpeted Overtime Numbers First
    """
    num_orders = len(orders.orders_dict)
    finished = 0
    time = 0
    
    deadline_orders = dict()
    added = dict()
    for order in orders.orders_dict.values():
        if order.deadline not in deadline_orders.keys():
            added[order.deadline] = False
            deadline_orders[order.deadline] = list()
        deadline_orders[order.deadline].append(order)
        
    deadlines = sorted(deadline_orders)    
    nums_ddl = len(deadlines)
    cur_deadline = deadlines[0]
    if nums_ddl > 1:
        next_ddl_id = 1
        next_deadline = deadlines[next_ddl_id]
    orders_cache = deadline_orders[cur_deadline]
    
    orders_cache: list()
    while(finished != num_orders):
        # action for next deadline coming
        flag = True
        for order in orders_cache:
            if order.finished == False:
                flag = False 
        if time > cur_deadline or flag:
            if next_deadline != -1 and added[next_deadline] == False:
                added[next_deadline] = True
                cur_deadline = next_deadline
                next_ddl_id += 1
                next_deadline = deadlines[next_ddl_id] if next_ddl_id < nums_ddl else -1
                for order in deadline_orders[cur_deadline]:
                    orders_cache.append(order)

        # find the order to achieve the minimal expected overtime numbers
        order_id = None
        min_overtime_nums = None
        min_sum_time = None
        
        for order in orders_cache:
            order: ORDER
            if order.finished:
                continue
            vir_time = time + order.sum_time
            nums = cal_overtime_nums(orders_cache, vir_time)
            
            if min_overtime_nums is None or nums < min_overtime_nums:
                min_overtime_nums = nums
                order_id = order.id
                min_sum_time = order.sum_time
            elif nums == min_overtime_nums and min_sum_time > order.sum_time:
                order_id = order.id
                min_sum_time = order.sum_time                
                 
        order = orders.orders_dict[order_id]
        order: ORDER
        
        # begin work
        time = order.begin_order(time)
        finished += 1
        
    return orders    


def cal_overtime_nums(orders_cache, vir_time):
    nums = 0
    for order in orders_cache:
        order: ORDER
        if order.finished:
            continue
        if order.deadline < vir_time:
            nums += 1
    return nums


def dmsf(orders: ORDERS):
    """
    Dealine & Min Sum Time First
    """
    num_orders = len(orders.orders_dict)
    finished = 0
    time = 0
    
    while(finished != num_orders):
        min_deadline = None
        min_sum_time = None
        order_id = None
        for id, order in orders.orders_dict.items():
            order: ORDER
            if order.finished:
                continue
            if min_deadline is None or min_deadline > order.deadline:
                min_deadline = order.deadline
                min_sum_time = order.sum_time
                order_id = id
            elif min_deadline == order.deadline and min_sum_time > order.sum_time:
                min_sum_time = order.sum_time
                order_id = id
                    
        order = orders.orders_dict[order_id]
        order: ORDER
        # begin work
        time = order.begin_order(time)
        finished += 1
    return orders


def msf(orders: ORDERS):
    """
    Min Sum Time First
    """
    num_orders = len(orders.orders_dict)
    finished = 0
    time = 0
    
    while(finished != num_orders):
        # find the minimal remaining time's order
        min_sum_time = None
        order_id = None
        for id, order in orders.orders_dict.items():
            order: ORDER
            if order.finished:
                continue
            if min_sum_time is None or min_sum_time > order.sum_time:
                min_sum_time = order.sum_time
                order_id = id
        order = orders.orders_dict[order_id]
        order: ORDER
        # begin work
        time = order.begin_order(time)
        finished += 1
    return orders


def derf(orders: ORDERS):
    """
    Dealine & Earliest Remaining Time First
    """
    num_orders = len(orders.orders_dict)
    finished = 0
    time = 0
    
    while(finished != num_orders):
        # find the minimal remaining time's order
        min_deadline = None
        min_rm_time = None
        order_id = None
        for id, order in orders.orders_dict.items():
            order: ORDER
            if order.finished:
                continue
            if min_deadline is None or min_deadline > order.deadline:
                min_deadline = order.deadline
                min_rm_time = order.sum_time
                order_id = id
            elif min_deadline == order.deadline and min_rm_time > order.rm_time:
                min_rm_time = order.sum_time
                order_id = id
                    
        order = orders.orders_dict[order_id]
        order: ORDER
        # begin work
        time = order.begin_order(time)
        finished += 1
    return orders


def erf(orders: ORDERS):
    """
    Earliest Remaining Time First
    """
    num_orders = len(orders.orders_dict)
    finished = 0
    time = 0
    
    while(finished != num_orders):
        # find the minimal remaining time's order
        min_rm_time = None
        order_id = None
        for id, order in orders.orders_dict.items():
            order: ORDER
            if order.finished:
                continue
            if min_rm_time is None or min_rm_time > order.rm_time:
                min_rm_time = order.rm_time
                order_id = id
        order = orders.orders_dict[order_id]
        order: ORDER
        # begin work
        time = order.begin_order(time)
        finished += 1
    return orders


###############################################
#             Models for Problem 2            #
###############################################

def lip(work_num, workers, times):
    """
    Linear Integer Programming
    """
    ots = times / np.sum(times)
    # create problem
    problem = pulp.LpProblem("Worker Allocation", pulp.LpMaximize)
    # target
    x = [[pulp.LpVariable(f"x_{i}_{j}", lowBound=0, upBound=1, cat=pulp.LpInteger) for j in range(12)] for i in range(20)]
    # object
    object = pulp.lpSum(ots[j] * x[i][j] * workers[i][j]  for i in range(20) for j in range(12))
    problem += object
    # constraint
    for i in range(20):
        problem += pulp.lpSum(x[i][j] for j in range(12)) <= 1
    for j in range(12):
        problem += pulp.lpSum(x[i][j] for i in range(20)) <=  work_num[j] 
    # get result
    problem.solve()
    result = np.zeros(shape=(20, 12))
    for i in range(20):
        for j in range(12):
            result[i][j] = pulp.value(x[i][j]) 
    return result    


###############################################
#             Models for Problem 3            #
###############################################

