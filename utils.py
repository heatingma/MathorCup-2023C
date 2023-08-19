import numpy as np
import math

WORK = [1, 2, 1, 3, 1, 1, 2, 1, 1, 3, 1, 1]

class PRODUCT:
    def __init__(self, name, need_time, deadline, product_line):
        self.name = name
        self.need_time = need_time
        self.deadline = deadline
        self.product_line = product_line
        self.line_work = WORK[int(product_line[-2:]) - 1]
        self.num = 0
        self.all_need_time = None
        self.message = "name, need_time, deadline, product_line, all_need_time, num"
        
    def cal_all_need_time(self):
        turn = math.ceil(self.num / self.line_work)
        self.all_need_time = turn * self.need_time   
        
    def add_num(self):
        self.num += 1
        self.cal_all_need_time()
        
    def finished_part(self):
        self.num -= 1
        self.cal_all_need_time()
    
    def finished(self, time):
        self.finished_time = time
        self.message += ", finished_time"
        
    def __repr__(self):
        return f"{self.__class__.__name__}({self.message})"       
    
    
class ORDER:
    def __init__(self, id, deadline):
        self.id = id
        self.deadline = deadline
        self.products = dict()
        self.rm_time = None
        self.begin_time = None
        self.finished = False
        self.sum_time = None
        self.left_time = None        
        self.message = "id, deadline, products, begin_time, "
        self.message += "left_time, rm_time, finished, sum_time"
        
    def add_product(self, product:PRODUCT):
        name = product.name
        if name not in self.products.keys():
            self.products[name] = product
            self.products[name].add_num()
        else:
            self.products[name].add_num()
        self.cal_time()
        
    def add_worker(self):
        pass
    
    def begin_order(self, time):
        self.begin_time = time
    
    def begin_work(self, num, time):
        max_num = 0
        for name, product in self.products.items():
            product: PRODUCT
            if product.num == 0:
                continue
            if max_num < product.num:
                max_num = product.num
                max_name = name
        num = min(max_num, num)
        product = self.products[max_name]
        finish_time = time + product.need_time
        for _ in range(num):
            self.finish_product(product, finish_time)
        return finish_time, int(self.finished)
            
    def finish_product(self, product:PRODUCT, time):
        self.products[product.name].finished_part()
        if self.products[product.name].num == 0:
            self.products[product.name].finished(time)
        self.finished = True
        for product in self.products.values():
            if product.num > 0:
                self.finished = False
        self.cal_time()
    
    def cal_time(self):
        all_need_time = 0
        for product in self.products.values():
            product: PRODUCT
            all_need_time += product.all_need_time
        self.rm_time = self.deadline - all_need_time
        self.left_time = all_need_time
                 
    def cal_overtime(self):
        self.finished_time = 0
        for product in self.products.values():
            self.finished_time = max(self.finished_time, product.finished_time)
        self.overtime = max(self.finished_time - self.deadline , 0)
        self.message += ", fnished_time, overtime"
    
    def get_msg(self):
        self.cal_overtime()
        return [self.id, self.begin_time, self.finished_time, self.deadline, self.overtime, self.sum_time]
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.message})"                
            
            
class ORDERS:
    def __init__(self):
        self.orders_dict = dict()
        
    def add_order(self, order:ORDER):
        self.orders_dict[order.id] = order
        order.sum_time = order.deadline - order.rm_time
    
    def print(self):
        print_msg = list()
        for order in self.orders_dict.values():
            order: ORDER
            print_msg.append(order.get_msg())
        return print_msg
    
    def __repr__(self):
        message = "orders_dict"
        return f"{self.__class__.__name__}({message})"    
    

class WORKER:
    def __init__(self, id, cap):
        self.id = id
        self.cap = cap
        self.times = [0 for _ in range(len(cap))]
        



def get_orders(data: np.ndarray):
    orders = ORDERS()
    cur_order = None
    cur_id = None
    for order_data in data:
        product = PRODUCT(*order_data[1:5])
        if order_data[0] != cur_id:
            if cur_order is not None:
                orders.add_order(cur_order)
            cur_id = order_data[0]
            cur_order = ORDER(cur_id, order_data[3])
            cur_order.add_product(product)
        else:
            cur_order.add_product(product)
    return orders



