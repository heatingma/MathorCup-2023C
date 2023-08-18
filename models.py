import numpy as np
from utils import ORDERS, ORDER, PRODUCT


def edf(orders: ORDERS, work_num):
    num_orders = len(orders.orders_dict)
    finished = 0
    time = 0
    import pdb
    
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
                