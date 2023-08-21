import numpy as np
import math
from itertools import permutations
import copy
import pdb
WORK = np.array([1, 2, 1, 3, 1, 1, 2, 1, 1, 3, 1, 1])
THEORY = np.array([450, 675, 450, 675, 450, 450, 675, 450, 675, 675, 675, 450])
PRACTICE = np.array([900, 1125, 900, 1125, 900, 900, 1125, 900, 1125, 1125, 1125, 900])
EXCELLENT = PRACTICE + 150 * 60
BADTIME = 100
EXCELLENT_SCORE = 500
OUTSTANDING_SCORE = 1000
THEORY_SCORE = 100
N_O_SCORE = 0.3
O_E_SCORE = 0.2
SCORE = 0.1
PRIO = 50

###############################################
#                 Utils Class                 #
###############################################


class WORKER:
    def __init__(self, id, cap: np.ndarray):
        self.id = id
        self.cap = cap
        self.ori_cap = copy.deepcopy(cap)
        self.work = False
        self.next_not_work_time = None
        self.work_line = None
        self.finish_theory = list()
        self.finish_practice = list()
        self.teach_ratio = [1 for _ in range(len(cap))]
        self.teacher_cap = [0 for _ in range(len(cap))]
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

    def check_work(self, time):
        if self.next_not_work_time is not None:
            if time == self.next_not_work_time:
                self.work = False
                self.next_not_work_time = None
            else:
                self.work = True
                
    def begin_work(self, work_line, finished_time):
        self.next_not_work_time = finished_time
        self.work_line = work_line
        self.work = True
    
    def finish_work(self):
        self.work = False
    
    def begin_teach(self, line_id):
        self.teach_ratio[line_id] = 0.6 
    
    def end_teach(self, line_id):
        self.teach_ratio[line_id] = 1
    
    def add_teacher(self, teacher, line_id):
        self.work_line = line_id
        self.teacher = teacher
        teacher.begin_teach(line_id)
        self.teacher_cap[line_id] = teacher.cap[line_id] * 0.6
    
    def del_teacher(self):
        self.teacher.end_teach(self.work_line)
        
    def update_state(self):
        if self.work == True:
            self.practice(self.work_line)
    
    def ept_prac_improve(self, prac_time, line_id):
        if self.cap[line_id] == 1:
            return 0
        ept_prac = self.prac[line_id] + prac_time
        if self.cap[line_id] == 0.8:
            if ept_prac >= EXCELLENT[line_id]:
                return prac_time*O_E_SCORE + EXCELLENT_SCORE
            else:
                return prac_time*O_E_SCORE
        else:
            if ept_prac >= PRACTICE[line_id]:
                return prac_time*N_O_SCORE + OUTSTANDING_SCORE
            else:
                return prac_time*N_O_SCORE
            
    def ept_theo_improve(self, theo_time, line_id):
        if self.theo[line_id] == True:
            return 0
        ept_prac = self.theo[line_id] + theo_time
        if ept_prac >= THEORY[line_id]:
            return theo_time*SCORE + THEORY_SCORE
        else:
            return theo_time*SCORE   
                    
    def practice(self, line_id):
        self.prac[line_id] += 1
        if self.prac[line_id] >= EXCELLENT[line_id]:
            self.cap[line_id] = 1
        elif self.prac[line_id] >= PRACTICE[line_id]:
            self.cap[line_id] = 0.8
            self.finish_practice[line_id] = True
            
    def theory(self, line_id):
        self.theo[line_id] += 1
        if self.theo[line_id] >= THEORY[line_id]:
            self.finish_theory[line_id] = True
         
    def check_theory(self, line_id):
        return self.theo[line_id]
    
    def get_msg(self):
        return np.concatenate([[self.id], self.ori_cap , self.cap])

    def get_msg_2(self):
        return np.concatenate([[self.id], self.theo, self.prac])
    
    def __repr__(self):
        message = "id, cap, work, finish_theory, finish_practice, "
        message += "theo, prac"
        return f"{self.__class__.__name__}({message})"                


class WORKERS:
    def __init__(self):
        self.workers_dict = dict()
        
    def add_worker(self, worker: WORKER):
        self.workers_dict[worker.id] = worker
    
    def get_free_worker(self):
        free = list()
        for worker in self.workers_dict.values():
            worker: WORKER
            if worker.work == False:
                free.append(worker)
        return free
    
    def find_workers(self, work_ids):
        workers_list = list()
        for worker in self.workers_dict.values():
            worker: WORKER
            if worker.id in work_ids:
                workers_list.append(worker)
        return workers_list
    
    def get_msg(self):
        data = list()
        for worker in self.workers_dict.values():
            data.append(worker.get_msg())
        return data

    def get_msg_2(self):
        data = list()
        for worker in self.workers_dict.values():
            data.append(worker.get_msg_2())
        return data
    
    def __repr__(self):
        message = "workers_dict"
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
            if self.workers[0].cap[self.product_line] == 0:
                cap = self.workers[0].teacher_cap[self.product_line]
            else:
                cap = self.workers[0].cap[self.product_line]
            turn = self.num / cap
        else:
            turns_list = list()
            for worker in self.workers:
                worker: WORKER
                if worker.cap[self.product_line] == 0:
                    add_data = 1 / worker.teacher_cap[self.product_line]
                else:
                    add_data = 1 / worker.cap[self.product_line]
                turns_list.append(add_data)
            turns_list = np.array(turns_list)
            begin = np.array([0.0 for _ in range(len(self.workers))])
            num = self.num
            while(num > 0):
                id = np.argmin(turns_list + begin)
                begin[id] += turns_list[id]
                num -= 1
            turn = max(begin)
        self.sum_need_time = turn * self.need_time   
    
    def add_worker(self, worker:WORKER):
        if self.workers is None:
            self.workers = list()
        self.workers.append(worker)
        self.cal_sum_need_time()           
                
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
    
    def change_workers(self, workers):
        self.workers = workers
        for product in self.products.values():
            product: PRODUCT
            for worker in self.workers:
                product.add_worker(worker)
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
        data = [self.id, self.begin_time, self.finished_time, self.deadline, self.overtime, self.sum_time]
        for worker in self.workers:
            worker: WORKER
            data.append(worker.id + 1)
        return data
    
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
        self.all_orders = list()
        self.cur_deadline = 0
        self.orders_num = 0
        self.cur_workers = None
    
    def add_order(self, order:ORDER):
        self.finished = False
        if order.deadline not in self.block_queue.keys():
            self.block_queue[order.deadline] = list()
        self.block_queue[order.deadline].append(order)
        if order.deadline not in self.deadlines:
            self.deadlines.append(order.deadline)
            self.deadlines = sorted(self.deadlines)
        self.all_orders.append(order)
        self.orders_num += 1
            
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
            for _order in self.wait_queue:
                if _order.deadline - _order.sum_time < vir_time:
                    num_overs += 1
            for deadline in self.block_queue.keys():
                for _order in self.block_queue[deadline]:
                    if _order.deadline - _order.sum_time < vir_time:
                        num_overs += 1
            if min_overs is None or min_overs > num_overs:
                min_overs = num_overs
                best_order = order
            elif min_overs == num_overs:
                if best_order.sum_time > order.sum_time:
                    best_order = order    
        return best_order

    def find_order(self, order_id):
        for order in self.wait_queue:
            order: ORDER
            if order.id == order_id:
                return order
        return None
    
    def begin_next_order(self, order_id, time, workers, line_id):
        order = self.find_order(order_id)
        order: ORDER
        order.change_workers(workers)
        self.wait_queue.remove(order)
        self.work_order = order
        finshed_time = int(order.begin_order(time))
        self.next_not_busy_time = finshed_time
        self.orders_num -= 1
        self.finished = True if self.orders_num == 0 else False
        for worker in workers:
            worker: WORKER
            worker.begin_work(line_id, finshed_time)
        self.cur_workers = workers
    
    def check_busy(self, time):
        if self.next_not_busy_time is None:
            self.busy = False
        elif self.next_not_busy_time == time:
            self.busy = False
        elif self.finished == False:
            self.busy = True
    
    def get_msg(self):
        data = list()
        for order in self.all_orders:
            order: ORDER
            data.append(order.get_msg())
        return data
        
    def __repr__(self):
        message = "id, busy, work_order, wait_queue, block_queue, "
        message += "deadlines, cur_deadline, next_not_busy_time"
        return f"{self.__class__.__name__}({message})"      


class LINES:
    def __init__(self, workers:WORKERS):
        self.lines_dict = dict()
        self.workers = workers
        self.finished = True        
        self.times = np.load("processed_data/problem_2/overtime-sumtime.npy", allow_pickle=True)
        self.get_lines_priority()   
    
    def time_zero(self, assign):
        for line in self.lines_dict.values():
            line: LINE
            order = line.find_next_order(0)
            order: ORDER
            assign_workers = self.workers.find_workers(assign[line.id])
            line.begin_next_order(order.id, 0, assign_workers, line.id)
            line.check_busy(0)
            
    def get_lines_priority(self):
        index_dict = {num: i for i, num in enumerate(self.times)}
        sorted_array = sorted(self.times, reverse=True)
        priority = np.zeros(len(sorted_array))
        for i in range(len(sorted_array)):
            priority[i] = index_dict[sorted_array[i]]
        self.lines_priority = priority
    
    def add_line(self, line:LINE):
        self.finished = False
        self.lines_dict[line.id] = line
    
    def update_state(self, time):
        for line in self.lines_dict.values():
            line: LINE
            line.update_queue(time)
        for worker in self.workers.workers_dict.values():
            worker: WORKER
            worker.update_state()
            worker.check_work(time)
        self.theory()
        self.finished = True
        for line in self.lines_dict.values():
            line: LINE
            line.check_busy(time)
            if line.busy == False and line.finished == False:
                self.times[line.id] += PRIO
                self.get_lines_priority()
            if line.finished == False:
                self.finished = False
      
    def next_orders(self, time):
        for line_id in self.lines_priority:
            line_id = int(line_id)
            line = self.lines_dict[line_id]
            line: LINE
            if line.busy == False and line.finished == False:
                order = line.find_next_order(time)
                free_workers = self.workers.get_free_worker()
                chooses = list(permutations(free_workers, int(WORK[line_id])))
                min_sum_time = order.sum_time
                best_choose = line.cur_workers
                best_score, _ = self.get_score(order, best_choose, line_id, min_sum_time)
                best_teachers = None
                for choose in chooses:
                    if check_theo(choose, line_id) == False:
                        continue
                    score, teachers = self.get_score(order, choose, line_id, min_sum_time)
                    if score is None:
                        continue
                    if best_choose is None or score > best_score:
                        best_score = score
                        best_choose = choose
                        best_teachers = teachers
                if best_choose is None:
                    continue
                if best_teachers is not None:
                    for i, teacher in enumerate(best_teachers):
                        best_choose[i].add_teacher(teacher, line_id)
                line.begin_next_order(order.id, time, best_choose, line_id)
                line.check_busy(time)
    
    def get_score(self, order, choose, line_id, min_sum_time):
        n_nums, n_workers = cal_n_nums(choose, line_id)
        teachers = None
        if n_nums != 0:
            teachers, tea_num = find_teachers(choose, self.workers, n_nums, line_id)
            if tea_num != n_nums:
                return None, None
            for i in range(tea_num):
                n_workers[i].add_teacher(teachers[i], line_id)
        copy_order = copy.deepcopy(order)
        copy_order.change_workers(choose)
        bad_time = (min_sum_time - copy_order.sum_time) * BADTIME
        ipv_score = 0
        for worker in choose:
            worker: WORKER
            ipv_score += worker.ept_prac_improve(copy_order.sum_time, line_id)
        if n_nums != 0:
            for i in range(tea_num):
                n_workers[i].del_teacher()
                ipv_score -= teachers[i].ept_theo_improve(copy_order.sum_time, line_id)
        score = ipv_score - bad_time
        return score, teachers
    
    def theory(self):
        free_workers = self.workers.get_free_worker()
        for line_id in self.lines_priority:
            line_id = int(line_id)
            teachers_list = list()
            students_list = list()
            if len(free_workers) == 0 or len(free_workers) == 1:
                break
            for worker in free_workers:
                worker: WORKER
                if worker.cap[line_id] != 0:
                    teachers_list.append(worker)
                if worker.finish_theory[line_id] == False:
                    students_list.append(worker)
            len_tea = len(teachers_list)
            len_stu = len(students_list)
            if len_tea >= len_stu:
                for student in students_list:
                    student: WORKER
                    student.theory(line_id)
                    free_workers.remove(student)
                    tea = worest_tea(teachers_list)
                    free_workers.remove(tea)
                    teachers_list.remove(tea)
            else:
                for teacher in teachers_list:
                    teacher: WORKER
                    stu = best_stu(students_list, line_id)
                    stu.theory(line_id)
                    students_list.remove(stu)
                    free_workers.remove(stu)
                    free_workers.remove(teacher)
                    
                
    def get_msg(self):
        data = list()
        for line in self.lines_dict.values():
            part_msg = line.get_msg()
            for msg in part_msg:
                msg.insert(0, line.id + 1)
                data.append(msg)
        return data
    
    def __repr__(self):
        message = "lines_dict, lines_priority, workers"
        return f"{self.__class__.__name__}({message})" 
                
            
###############################################
#               Utils Function                #
###############################################

def check_theo(workers, line_id):
    flag = True
    for worker in workers:
        worker: WORKER
        if worker.finish_theory[line_id] == False:
            flag = False
            break
    return flag


def best_stu(stu_list:list, line_id):
    best_stu = None
    best_cap = None
    for stu in stu_list:
        stu: WORKER
        cap =  np.sum(stu.cap[line_id])
        if best_cap is None or cap > best_cap:
            best_cap = cap
            best_stu = stu
    return best_stu


def worest_tea(tea_list:list):
    worest_tea = None
    worest_cap = None
    for tea in tea_list:
        tea: WORKER
        cap =  np.sum(tea.cap)
        if worest_cap is None or cap < worest_cap:
            worest_cap = cap
            worest_tea = tea
    return worest_tea
    
    
def find_teachers(cur_workers, all_workers:WORKERS, num, line_id):
    free_workers = list()
    for worker in all_workers.workers_dict.values():
        if worker not in cur_workers and worker.work == False:
            free_workers.append(worker)
    teachers = list()
    tea_num = 0
    for _ in range(num):
        cur_best = None
        cur_best_teacher = None
        for worker in free_workers:
            if cur_best is None or worker.cap[line_id] > cur_best:
                if worker not in teachers and worker.cap[line_id] != 0:
                    cur_best_teacher = worker
                    cur_best = worker.cap[line_id]
        if cur_best_teacher != None:
            teachers.append(cur_best_teacher)
            tea_num += 1
    return teachers, tea_num


def cal_n_nums(workers, line_id):
    num = 0
    n_workers = list()
    for worker in workers:
        worker: WORKER
        try:
            if worker.cap[line_id] == 0:
                num += 1
                n_workers.append(worker)
        except:
            print(worker.cap[line_id] == 0)
    return num, n_workers


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




def get_workers(data: np.ndarray):
    workers = WORKERS()
    for id, worker_data in enumerate(data):
        workers.add_worker(WORKER(id+1, worker_data))
    return workers


def get_line(data: np.ndarray, line_id):
    cur_order = None
    cur_id = None
    line = LINE(line_id)
    for order_data in data:
        product = PRODUCT(*order_data[1:5])
        if order_data[0] != cur_id:            
            if cur_order is not None:
                line.add_order(cur_order)
            cur_id = order_data[0]
            cur_order = ORDER(cur_id, order_data[3])
            cur_order.add_product(product)
        else:
            cur_order.add_product(product)
    return line
    

def get_lines(workers:WORKERS):
    lines = LINES(workers)
    dir_path = 'processed_data/problem_1/line_{}.npy'
    for i in range(12):
        data = np.load(dir_path.format(i+1), allow_pickle=True)
        lines.add_line(get_line(data, i))
    return lines   