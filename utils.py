class PRODUCT:
    def __init__(self, name, need_time, deadline, product_line):
        self.name = name
        self.need_time = need_time
        self.deadline = deadline
        self.product_line = product_line
        self.num = 0
    
    def add_num(self):
        self.num += 1
        
    
class ORDER:
    def __init__(self, id):
        self.order_id = id
        self.products = dict()
    
    def add_product(self, product_name, product:PRODUCT):
        self.products[product_name] = product


class ORDERS:
    def __init__(self):
        self.orders_dict = dict()
    
    
    def add_order(self, order_id, order:ORDER):
        self.orders_dict[order_id] = order

