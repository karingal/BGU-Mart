from persistence import *

def main():
    #TODO: implement
    print("Activities")
    temp ='SELECT * FROM activities'
    for r in repo.execute_command(temp):
        print(r.__str__())
        
    print("Branches")
    temp ='SELECT * FROM branches'
    for r in repo.execute_command(temp):
        print(r.__str__())      
         
    print("Employees")
    temp ='SELECT * FROM employees'
    for r in repo.execute_command(temp):
        print(r.__str__())
    
    print("Products")
    temp ='SELECT * FROM products'
    for r in repo.execute_command(temp):
        print(r.__str__())    
    
    print("Suppliers")
    temp ='SELECT * FROM suppliers'
    for r in repo.execute_command(temp):
        print(r.__str__())    
        
    print("")
    print("Employees report")
    for item in repo.get_employees_report():
        print(item.name, item.salary, item.branche, item.income)
    
    print("")
    print("Activities report")
    for item in repo.get_activities_report():
        if item.nameOfSeller == None:
            print("('",item.date,"', ","'",item.description,"', ",item.quantity,", ",item.nameOfSeller,", '", item.nameOfSupplier,"')", sep='')
        if item.nameOfSupplier == None:
            print("('",item.date,"', ","'",item.description,"', ",item.quantity,", '",item.nameOfSeller,"', ", item.nameOfSupplier,")", sep='')

if __name__ == '__main__':
    main()