import sqlite3
import atexit
from DAO import _Vaccines, _Logistics, _Clinics, _Suppliers
from DTO import Vaccine, Logistic, Clinic, Supplier


class _Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect("database.db")
        self.vaccines = _Vaccines(self._conn)
        self.suppliers = _Suppliers(self._conn)
        self.clinics = _Clinics(self._conn)
        self.logistics = _Logistics(self._conn)

    def _close(self):
        self._conn.commit()
        self._conn.close()

    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE vaccines (
                id          INTEGER     PRIMARY KEY,
                date        DATE        NOT NULL,
                supplier    INTEGER     REFERENCES suppliers(id),
                quantity    INTEGER     NOT NULL
            );

            CREATE TABLE suppliers (
                id          INTEGER     PRIMARY KEY,
                name        STRING      NOT NULL,
                logistic    INTEGER     REFERENCES logistics(id)
            );

            CREATE TABLE clinics (
                id          INTEGER     PRIMARY KEY,
                location    STRING      NOT NULL,
                demand      INTEGER     NOT NULL,
                logistic    INTEGER     REFERENCES logistics(id)
            );

            CREATE TABLE logistics (
                id              INTEGER     PRIMARY KEY,
                name            STRING      NOT NULL,
                count_sent      INTEGER     NOT NULL,
                count_received  INTEGER     NOT NULL
            ); 
        """)

    def parse_file(self, input_file):
        with open(input_file, encoding='UTF-8') as config_file:
            lines = []
            for line in config_file:
                lines.append(line)
            first_line = lines[0]
            first_line = first_line[0:len(first_line)-1]
            counters = first_line.split(',')
            vaccines_counter = int(counters[0])
            suppliers_counter = int(counters[1])
            clinics_counter = int(counters[2])
            logistics_counter = int(counters[3])
            counter = 1
            for index in range(counter, counter + vaccines_counter):
                line = lines[index]
                line = line[0:len(line)-1]
                line = line.split(",")
                self.vaccines.insert(Vaccine(*line))
                counter = counter + 1
            for index in range(counter, counter + suppliers_counter):
                line = lines[index]
                line = line[0:len(line)-1]
                line = line.split(",")
                self.suppliers.insert(Supplier(*line))
                counter = counter + 1
            for index in range(counter, counter + clinics_counter):
                line = lines[index]
                line = line[0:len(line)-1]
                line = line.split(",")
                self.clinics.insert(Clinic(*line))
                counter = counter + 1
            for index in range(counter, counter + logistics_counter - 1):
                line = lines[index]
                line = line[0:len(line)-1]
                line = line.split(",")
                self.logistics.insert(Logistic(*line))
                counter = counter + 1
            line = lines[counter]
            line = line.split(",")
            self.logistics.insert(Logistic(*line))

    def operate_orders(self, orders_file):
        with open(orders_file, encoding='UTF-8') as orders:
            output = []
            lines = []
            for line in orders:
                lines.append(line)
            for i in range(0, len(lines)-1):
                line = lines[i]
                line = line[0:len(line)-1]
                operation = line.split(',')
                if len(operation) is 3:
                    name = operation[0]
                    operation[0] = self.suppliers.get_supplier_id(name)
                    result = repo.receive_shipment(operation[0], operation[1], operation[2], name)
                    output.append(result)
                else:
                    result = repo.send_shipment(*operation)
                    output.append(result)
            line = lines[len(lines)-1]
            operation = line.split(',')
            if len(operation) is 3:
                name = operation[0]
                operation[0] = self.suppliers.get_supplier_id(name)
                result = repo.receive_shipment(operation[0], operation[1], operation[2], name)
                output.append(result)
            else:
                result = repo.send_shipment(*operation)
                output.append(result)
        return output

    def receive_shipment(self, id_supplier, amount, date, name):
        id = self.get_id()
        self.vaccines.insert(Vaccine(id, date, id_supplier, amount))
        logistic_id = self.suppliers.get_logistic_id(name)
        self.logistics.update_received(logistic_id, amount)
        inventory = str(self.vaccines.total_inventory())
        demand = str(self.clinics.total_demand())
        received = str(self.logistics.total_received())
        sent = str(self.logistics.total_sent())
        output = inventory + "," + demand + "," + received + "," + sent
        return output

    def send_shipment(self, location, amount):
        self.clinics.reduce(location, amount)
        self.vaccines.remove_inventory(amount)
        logistic_id = self.clinics.get_logistic_name(location)
        self.logistics.update_sent(logistic_id, amount)
        inventory = str(self.vaccines.total_inventory())
        demand = str(self.clinics.total_demand())
        received = str(self.logistics.total_received())
        sent = str(self.logistics.total_sent())
        output = inventory + "," + demand + "," + received + "," + sent
        return output

    def get_id(self):
        return self.vaccines.get_max_id()+1


repo = _Repository()
atexit.register(repo._close)