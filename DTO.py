class Vaccine:
    def __init__(self, id, date, supplier_id, quantity):
        self.id = id
        self.date = date
        self.supplier = supplier_id
        self.quantity = quantity

    def get_id(self):
        return self.id

    def get_date(self):
        return self.date

    def get_supplier(self):
        return self.supplier

    def get_quantity(self):
        return self.quantity


class Supplier:
    def __init__(self, id, name, logistic):
        self.id = id
        self.name = name
        self.logistic = logistic


class Clinic:
    def __init__(self, id, location, demand, logistic):
        self.id = id
        self.location = location
        self.demand = demand
        self.logistic = logistic


class Logistic:
    def __init__(self, id, name, count_sent, count_received):
        self.id = id
        self.name = name
        self.count_sent = count_sent
        self.count_received = count_received

