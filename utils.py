class PRODUCT:
    def __init__(self, name, need_time, product_line):
        self.name = name
        self.need_time = need_time
        self.product_line = product_line
        self.num = 0
    
    def add_num(self):
        self.num += 1
        
    def finished(self, time):
        self.finished_time = time
    
    
class ORDER:
    def __init__(self, id, deadline):
        self.order_id = id
        self.deadline = deadline
        self.products = dict()
    
    def add_product(self, product_name, product:PRODUCT):
        self.products[product_name] = product

    def cal_overtime(self):
        self.latest_time = 0
        for product in self.products.values():
            self.latest_time = max(self.latest_time, product.finished_time)
        self.overtime = self.latest_time - self.deadline
            
            
class ORDERS:
    def __init__(self):
        self.orders_dict = dict()
    
    def add_order(self, order_id, order:ORDER):
        self.orders_dict[order_id] = order

