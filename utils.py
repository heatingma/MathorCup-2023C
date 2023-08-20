import numpy as np
import math

WORK = np.array([1, 2, 1, 3, 1, 1, 2, 1, 1, 3, 1, 1])
THEORY = np.array([450, 675, 450, 675, 450, 450, 675, 450, 675, 675, 675, 450])
PRACTICE = np.array([900, 1125, 900, 1125, 900, 900, 1125, 900, 1125, 1125, 1125, 900])
EXCELLENT = PRACTICE + 150 * 60


###############################################
#                 Utils Class                 #
###############################################


class WORKER:
    def __init__(self, id, cap: np.ndarray):
        self.id = id
        self.cap = cap
        self.work = False
        self.finish_theory = list()
        self.finish_practice = list()
        self.teach_ratio = [1 for _ in range(len(cap))]
        self.data_process()
    
    def data_process(self):
        length = len(self.cap)
        self.theo = np.zeros(length)
        self.prac = np.zeros(length)
        for i in range(length):
            if self.cap[i] != 0:
                # no need to study
                self.theo[i] = THEORY[i]
                self.prac[i] = PRACTICE[i] \
                    if self.cap[i] == 0.8 else EXCELLENT[i]
                self.finish_theory.append(True)
                self.finish_practice.append(True)
            else:
                self.finish_theory.append(False)
                self.finish_practice.append(False)

    def begin_work(self):
        self.work = True
    
    def finish_work(self):
        self.work = False
    
    def begin_teach(self, line_id):
        self.teach_ratio[line_id] = 0.6 
    
    def end_teach(self, line_id):
        self.teach_ratio[line_id] = 1
        
    def practice(self, line_id):
        self.prac[line_id] += 1
        if self.prac[line_id] >= EXCELLENT[line_id]:
            self.cap = 1
        elif self.prac[line_id] >= PRACTICE[line_id]:
            self.cap = 0.8
            self.finish_practice[line_id] = True
            
    def theory(self, line_id):
        self.theo[line_id] += 1
        if self.theo[line_id] >= THEORY[line_id]:
            self.finish_theory[line_id] = True
         
    def check_theory(self, line_id):
        return self.theo[line_id]

    def __repr__(self):
        message = "id, cap, work, finish_theory, finish_practice, "
        message += "theo, prac"
        return f"{self.__class__.__name__}({message})"                

           
class PRODUCT:
    def __init__(self, name, need_time, deadline, product_line):
        self.name = name
        self.need_time = need_time
        self.deadline = deadline
        self.product_line = int(product_line[-2:]) - 1
        self.num = 0
        self.sum_need_time = None
        self.workers = None
        self.workstations = WORK[self.product_line]
    
    def cal_sum_need_time(self):
        if self.workers is None:
            turn = math.ceil(self.num / self.workstations)
        elif self.workstations == 1:
            turn = 1 / self.workers[0].cap[self.product_line] / \
                    self.workers[0].teach_ratio[self.product_line]
        else:
            turns_list = list()
            for worker in self.workers:
                worker: WORKER
                turns_list.append(1 / worker.cap[self.product_line] / \
                    worker.teach_ratio[self.product_line])
            num = self.num
            begin = [0 for _ in range(len(self.workers))]
            while(num > 0):
                id = (turns_list + begin).index(min(turns_list + begin))
                begin[id] + turns_list[id]
                num += 1
            turn = max(begin)
        self.sum_need_time = turn * self.need_time   
    
    def add_worker(self, worker:WORKER):
        if self.workers is None:
            self.workers = list()
        self.workers.append(worker)           
                
    def add_num(self):
        self.num += 1
        self.cal_sum_need_time()
        
    def __repr__(self):
        message = "name, need_time, deadline, product_line, "
        message += "sum_need_time, num, workers"
        return f"{self.__class__.__name__}({message})"       
    
    
class ORDER:
    def __init__(self, id, deadline):
        self.id = id
        self.deadline = deadline
        self.products = dict()
        self.begin_time = None
        self.rm_time = None
        self.sum_time = None
        self.finished = False
        self.workers = None    
        self.message = "id, deadline, products, begin_time, "
        self.message += "rm_time, finished, sum_time, workers"
        
    def add_product(self, product:PRODUCT):
        name = product.name
        if name not in self.products.keys():
            self.products[name] = product
            self.products[name].add_num()
        else:
            self.products[name].add_num()
        self.cal_time()
    
    def begin_order(self, time):
        self.begin_time = time
        self.finished_time = time + self.sum_time
        self.finished = True
        self.message += ", fnished_time"
        return self.finished_time
    
    def cal_time(self):
        sum_need_time = 0
        for product in self.products.values():
            product: PRODUCT
            sum_need_time += product.sum_need_time
        self.rm_time = self.deadline - sum_need_time
        self.sum_time = sum_need_time
                 
    def cal_overtime(self):
        self.overtime = self.finished_time - self.deadline
        if self.overtime < 0:
            self.overtime = 0
        self.message += ", overtime"
    
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
    
    
class LINE:
    def __init__(self, id):
        self.id = id
        self.finished = True
        self.busy = False
        self.next_not_busy_time = None
        self.work_order = None
        self.wait_queue = list()
        self.block_queue = dict()
        self.deadlines = list()
        self.cur_deadline = 0
    
    def add_order(self, order:ORDER):
        self.finished = False
        if order.deadline not in self.block_queue.keys():
            self.block_queue[order.deadline] = list()
        self.block_queue[order.deadline].append(order)
        if order.deadline not in self.deadlines:
            self.deadlines.append(order.deadline)
            self.deadlines = sorted(self.deadlines)
            
    def update_queue(self, time):
        if len(self.wait_queue) == 0 or time > self.cur_deadline:
            if len(self.deadlines) != 0:
                deadline = self.deadlines[0]
                for order in self.block_queue[deadline]:
                    self.wait_queue.append(order)
                self.deadlines.remove(deadline)
                self.cur_deadline = deadline
    
    def find_next_order(self, time):
        min_overs = None
        best_order = None
        for order in self.wait_queue:
            order: ORDER
            vir_time = time + order.sum_time
            num_overs = 0
            for order in self.wait_queue:
                if order.deadline - order.sum_time < vir_time:
                    num_overs += 1
            for order in self.block_queue:
                if order.deadline - order.sum_time < vir_time:
                    num_overs += 1
            if min_overs is None or min_overs > num_overs:
                min_overs = num_overs
                best_order = order
            elif min_overs == num_overs:
                if best_order.sum_time > order.sum_time:
                    best_order = order      
        return order

    def begin_next_order(self, order:ORDER, time):
        self.wait_queue.remove(order)
        self.work_queue = order
        order.begin_order(time)
        # finshed_time
        # self.next_not_busy_time = 

    def check_busy(self, time):
        return self.next_not_busy_time == time
    
    def __repr__(self):
        message = "id, busy, work_queue, wait_queue, block_queue, "
        message += "deadlines, cur_deadline"
        return f"{self.__class__.__name__}({message})"      


class LINES:
    def __init__(self):
        self.lines_dict = dict()
    
    def add_line(self, line:LINE):
        self.lines_dict[line.id] = line
        
    def next_orders(self):
        next_orders_list = list()
        for line in self.lines_dict.keys():
            line: LINE
            # if line.busy == False
            
###############################################
#               Utils Function                #
###############################################

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


def get_lines(data: np.ndarray):
    pass
