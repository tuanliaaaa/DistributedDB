
class Employee:
    def __init__(self, employee_id, employee_name,phone_number,email):
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.phone_number = phone_number
        self.email=email
class EmployeeInvoice:
    def __init__(self, employee_id, employee_name,phone_number,quantity):
        self.employee_id = employee_id
        self.employee_name = employee_name
        self.phone_number = phone_number
        self.quantity=quantity

