import sqlite3
import atexit
from dbtools import Dao
 
# Data Transfer Objects:
class Employee(object):
    #TODO: implement
    def __init__(self, id, name, salary, branche):
        self.id =id
        self.name = name
        self.salary = salary
        self.branche = branche
 
class Supplier(object):
    #TODO: implement
    def __init__(self, id, name, contact_information):
        self.id =id
        self.name = name
        self.contact_information = contact_information

class Product(object):
    #TODO: implement
    def __init__(self, id, description, price, quantity):
        self.id =id
        self.description = description
        self.price = price
        self.quantity = quantity

class Branche(object):
    #TODO: implement
    def __init__(self, id, location, number_of_employees):
        self.id =id
        self.location = location
        self.number_of_employees = number_of_employees

class Activitie(object):
    #TODO: implement
    def __init__(self, product_id, quantity, activator_id, date):
        self.product_id = product_id
        self.quantity = quantity
        self.activator_id = activator_id
        self.date = date
 
class EmployeeReport(object):
    def __init__(self,name,salary,branche,income):
        self.name = name
        self.salary = salary
        self.branche = branche
        self.income = income
        
class ActivitieReport(object):
    def __init__(self,date,description,quantity,nameOfSeller,nameOfSupplier):
        self.date = date
        self.description = description
        self.quantity = quantity
        self.nameOfSeller = nameOfSeller
        self.nameOfSupplier = nameOfSupplier
 
#Repository
class Repository(object):
    def __init__(self):
        self._conn = sqlite3.connect('bgumart.db')
        # self._conn.text_factory = bytes
        #TODO: complete
        self.products= Dao(Product,self._conn)
        self.suppliers= Dao(Supplier,self._conn)
        self.employees= Dao(Employee,self._conn)
        self.branches= Dao(Branche,self._conn)
        self.activities= Dao(Activitie,self._conn)
    def _close(self):
        self._conn.commit()
        self._conn.close()
 
    def create_tables(self):
        self._conn.executescript("""
            CREATE TABLE employees (
                id              INT         PRIMARY KEY,
                name            TEXT        NOT NULL,
                salary          REAL        NOT NULL,
                branche    INT REFERENCES branches(id)
            );
    
            CREATE TABLE suppliers (
                id                   INTEGER    PRIMARY KEY,
                name                 TEXT       NOT NULL,
                contact_information  TEXT
            );

            CREATE TABLE products (
                id          INTEGER PRIMARY KEY,
                description TEXT    NOT NULL,
                price       REAL NOT NULL,
                quantity    INTEGER NOT NULL
            );

            CREATE TABLE branches (
                id                  INTEGER     PRIMARY KEY,
                location            TEXT        NOT NULL,
                number_of_employees INTEGER
            );
    
            CREATE TABLE activities (
                product_id      INTEGER REFERENCES products(id),
                quantity        INTEGER NOT NULL,
                activator_id    INTEGER NOT NULL,
                date            TEXT    NOT NULL
            );
        """)
 
    def get_employees_report(self):
        all = self._conn.cursor().execute("""
            SELECT employees.name, employees.salary, branches.location, COALESCE(SUM(activities.quantity * products.price * (-1)), 0)
            FROM (((employees LEFT OUTER JOIN branches ON employees.branche = branches.id) 
            LEFT OUTER JOIN activities ON activities.activator_id = employees.id) 
            LEFT OUTER JOIN products ON activities.product_id = products.id) 
            GROUP BY employees.id, employees.name ORDER BY employees.name ASC
            """).fetchall()
        return [EmployeeReport(*row) for row in all]
    
    def get_activities_report(self):
        all = self._conn.cursor().execute("""
            SELECT activities.date, products.description, activities.quantity, employees.name, suppliers.name
            FROM (((activities INNER JOIN products ON activities.product_id = products.id) 
            LEFT JOIN employees ON activities.activator_id = employees.id) 
            LEFT JOIN suppliers ON activities.activator_id = suppliers.id) 
            ORDER BY activities.date ASC
            """).fetchall()
        return [ActivitieReport(*row) for row in all]
    
    def execute_command(self, script: str) -> list:
        return self._conn.cursor().execute(script).fetchall()
 
# singleton
repo = Repository()
atexit.register(repo._close)