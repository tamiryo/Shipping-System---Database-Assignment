import sqlite3


class _Vaccines:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, vaccine):
        self._conn.execute("""
            INSERT INTO vaccines (id, date, supplier, quantity) VALUES (?, ?, ?, ?)
        """, [vaccine.get_id(), vaccine.get_date(), vaccine.get_supplier(), vaccine.get_quantity()])

    def get_max_id(self):
        index = self._conn.cursor()
        index.execute("""
            SELECT MAX(id) FROM vaccines
        """)
        return index.fetchone()[0]

    def total_inventory(self):
        total = self._conn.cursor()
        total.execute("""
            SELECT SUM(quantity) FROM vaccines
        """)
        return total.fetchone()[0]

    def remove_inventory(self, amount):
        oldest = self._conn.cursor()
        oldest.execute("""
            SELECT * FROM vaccines ORDER BY date ASC
        """)
        amount = int(amount)
        while amount > 0:
            current = oldest.fetchone()
            id = current[0]
            quantity = current[3]
            if quantity <= amount:
                self._conn.execute("""
                    DELETE FROM vaccines WHERE id = (?) 
                """, (id,))
                amount = amount - quantity
            else:
                new_quantity = quantity - amount
                self._conn.execute("""
                    UPDATE vaccines
                    SET quantity = (?)
                    WHERE id = (?)
                """, (new_quantity, id))
                amount = 0


class _Suppliers:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, supplier):
        self._conn.execute("""
               INSERT INTO suppliers (id, name, logistic) VALUES (?, ?, ?)
           """, [supplier.id, supplier.name, supplier.logistic])

    def get_logistic_id(self, name):
        id = self._conn.cursor()
        id.execute("""
            SELECT logistic FROM suppliers WHERE name = (?)
        """, (name,))
        return id.fetchone()[0]

    def get_supplier_id(self, name):
        id = self._conn.cursor()
        id.execute("""
            SELECT id FROM suppliers WHERE name = (?)
        """, (name,))
        return id.fetchone()[0]


class _Clinics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, clinic):
        self._conn.execute("""
            INSERT INTO clinics (id, location, demand, logistic) VALUES (?, ?, ?, ?)
        """, [clinic.id, clinic.location, clinic.demand, clinic.logistic])

    def total_demand(self):
        total = self._conn.cursor()
        total.execute("""
            SELECT SUM(demand) FROM clinics
        """)
        return total.fetchone()[0]

    def reduce(self, location, amount):
        current_demand = self._conn.cursor()
        current_demand.execute("""
            SELECT demand FROM clinics WHERE location=(?)
        """, (location,))
        current_demand = current_demand.fetchone()[0]
        new_demand = current_demand - int(amount)
        self._conn.execute("""
            UPDATE clinics
            SET demand = (?)
            WHERE location = (?) 
        """, (new_demand, location))

    def get_logistic_name(self, location):
        name = self._conn.cursor()
        name.execute("""
            SELECT logistic FROM clinics WHERE location = (?) 
        """, (location,))
        return name.fetchone()[0]


class _Logistics:
    def __init__(self, conn):
        self._conn = conn

    def insert(self, logistic):
        self._conn.execute("""
            INSERT INTO logistics (id, name, count_sent, count_received) VALUES (?, ?, ?, ?)
        """, [logistic.id, logistic.name, logistic.count_sent, logistic.count_received])

    def update_received(self, id, amount):
        current = self._conn.cursor()
        current.execute("""
            SELECT count_received FROM logistics WHERE id = (?)
        """, (id,))
        current = int(current.fetchone()[0])
        new = current + int(amount)
        self._conn.execute("""
            UPDATE logistics
            SET count_received = (?)
            WHERE id = (?) 
        """, (new, id))

    def total_received(self):
        total = self._conn.cursor()
        total.execute("""
            SELECT SUM(count_received) FROM logistics
        """)
        return total.fetchone()[0]

    def total_sent(self):
        total = self._conn.cursor()
        total.execute("""
            SELECT SUM(count_sent) FROM logistics
        """)
        return total.fetchone()[0]

    def update_sent(self, id, amount):
        current = self._conn.cursor()
        current.execute("""
            SELECT count_sent FROM logistics WHERE id = (?)
                """, (id,))
        current_amount = int(current.fetchone()[0])
        new = current_amount + int(amount)
        self._conn.execute("""
            UPDATE logistics
            SET count_sent = (?)
            WHERE id = (?) 
            """, (new, id))


