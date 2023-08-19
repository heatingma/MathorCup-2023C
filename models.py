from utils import ORDERS, ORDER, PRODUCT


def dmlf(orders: ORDERS, work_num):
    """
    Dealine & Min Left Time First
    """
    num_orders = len(orders.orders_dict)
    finished = 0
    time = 0
    
    while(finished != num_orders):
        min_deadline = None
        min_left_time = None
        order_id = None
        for id, order in orders.orders_dict.items():
            order: ORDER
            if order.finished:
                continue
            if min_deadline is None or min_deadline > order.deadline:
                min_deadline = order.deadline
                min_left_time = order.left_time
                order_id = id
            elif min_deadline == order.deadline and min_left_time > order.left_time:
                min_left_time = order.left_time
                order_id = id
                    
        order = orders.orders_dict[order_id]
        order: ORDER
        # begin work
        if order.begin_time is None:
            order.begin_order(time)
        time, num = order.begin_work(work_num, time)
        finished += num
    return orders


def mlf(orders: ORDERS, work_num):
    """
    Min Left Time First
    """
    num_orders = len(orders.orders_dict)
    finished = 0
    time = 0
    
    while(finished != num_orders):
        # find the minimal remaining time's order
        min_left_time = None
        order_id = None
        for id, order in orders.orders_dict.items():
            order: ORDER
            if order.finished:
                continue
            if min_left_time is None or min_left_time > order.left_time:
                min_left_time = order.left_time
                order_id = id
        order = orders.orders_dict[order_id]
        order: ORDER
        # begin work
        if order.begin_time is None:
            order.begin_order(time)
        time, num = order.begin_work(work_num, time)
        finished += num
    return orders


def derf(orders: ORDERS, work_num):
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
        if order.begin_time is None:
            order.begin_order(time)
        time, num = order.begin_work(work_num, time)
        finished += num
    return orders


def erf(orders: ORDERS, work_num):
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
        if order.begin_time is None:
            order.begin_order(time)
        time, num = order.begin_work(work_num, time)
        finished += num
    return orders


def dmsf(orders: ORDERS, work_num):
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
        if order.begin_time is None:
            order.begin_order(time)
        time, num = order.begin_work(work_num, time)
        finished += num
    return orders


def msf(orders: ORDERS, work_num):
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
        if order.begin_time is None:
            order.begin_order(time)
        time, num = order.begin_work(work_num, time)
        finished += num
    return orders


