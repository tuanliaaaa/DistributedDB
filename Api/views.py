from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import pyodbc
import json
from .models import Employee,EmployeeInvoice
def delete_raw_sql(sql_query):
    try:
        connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=MSI\TUAN3;DATABASE=Tuan;UID=sa;PWD=2'
        with pyodbc.connect(connection_string) as connection:
            cursor = connection.cursor()
            cursor.execute(sql_query)
            connection.commit()
            return {"access": "Xóa dữ liệu thành công"}
    except pyodbc.Error as e:
        error_message = str(e)
        start_index = error_message.find("[SQL Server]") + 12
        end_index = error_message.rfind(".") + 1
        error_message = error_message[start_index:end_index]
        return {"message": error_message}

def execute_raw_sql(sql_query):
    try:
        connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=MSI\TUAN3;DATABASE=Tuan;UID=sa;PWD=2'
        with pyodbc.connect(connection_string) as connection:
            cursor = connection.cursor()
            cursor.execute(sql_query)
            results = cursor.fetchall()
            return results
    except pyodbc.Error as e:
        error_message = str(e)  # Chuyển đổi lỗi thành chuỗi
        start_index = error_message.find("[SQL Server]") + 12  # Tìm vị trí bắt đầu của thông báo lỗi
        end_index = error_message.rfind(".")+1  # Tìm vị trí kết thúc của thông báo lỗi
        error_message = error_message[start_index:end_index]  # Trích xuất thông báo lỗi cụ thể
        return {"message":error_message}
def update_raw_sql(sql_query):
    try:
        connection_string = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=MSI\TUAN3;DATABASE=Tuan;UID=sa;PWD=2'
        with pyodbc.connect(connection_string) as connection:
            cursor = connection.cursor()
            cursor.execute(sql_query)
            connection.commit()
            return {"accsess":"thành công"}
    except pyodbc.Error as e:
        error_message = str(e)  # Chuyển đổi lỗi thành chuỗi
        start_index = error_message.find("[SQL Server]") + 12  # Tìm vị trí bắt đầu của thông báo lỗi
        end_index = error_message.rfind(".")+1  # Tìm vị trí kết thúc của thông báo lỗi
        error_message = error_message[start_index:end_index]  # Trích xuất thông báo lỗi cụ thể
        return {"message":error_message}
class ListUser(APIView):
    
    def get(self,request):
        sql_query = "SELECT employee_id,employee_name,phone_number,email FROM Employees"
        results = execute_raw_sql(sql_query)
        if 'message' in results:
            return Response(results,status=400)
        else:
            employeeList=[]
            for result in results:
                employeeList.append(Employee(result[0],result[1],result[2],result[3]))
        return Response([emp.__dict__ for emp in employeeList],status=200)
    def post(self,request):
        sql_query="INSERT INTO Employees(employee_id,employee_name,branch_id,phone_number,email)VALUES('"+request.data['employee_id']+"','"+request.data['employee_name']+"','"+request.data['branch_id']+"','"+request.data['phone_number']+"','"+request.data['email']+"')"
        results = update_raw_sql(sql_query)
        if 'message' in results:
            return Response(results,status=400)
        else:
            employeeList=[]
            for result in results:
                employeeList.append(Employee(result[0],result[1],result[2],result[3]))
        return Response([emp.__dict__ for emp in employeeList],status=201)
class ListInvoice(APIView):
     def get(self,request):
        sql_query = "Select Top 10 e.employee_id, e.employee_name, e.phone_number, sum(i.quantity) as quantity from Employees as e join Invoices as i on i.employee_id=e. employee_id group by e.employee_id,e.employee_name,e.phone_number order by quantity DESC "
        results = execute_raw_sql(sql_query)
        if 'message' in results:
            return Response(results,status=400)
        else:
            employeeInvoiceList=[]
            for result in results:
                employeeInvoiceList.append(EmployeeInvoice(result[0],result[1],result[2],result[3]))
        return Response([emp.__dict__ for emp in employeeInvoiceList],status=200)
class EmployeeByID(APIView):
    def patch(self,request,employeeID):
       
        sql_query="Update Employees SET "
        if 'employee_name' in request.data:
            sql_query+="employee_name='"+ request.data['employee_name']+"'"
        if 'phone_number' in request.data:
            sql_query+=", phone_number='"+ request.data['phone_number']+"'"
        if 'email' in request.data:
            sql_query+=", email='"+ request.data["email"]+"' "
        sql_query+="WHERE employee_id ='"+employeeID+"' "
        results = update_raw_sql(sql_query)
        print(sql_query)
        if 'message' in results:
            return Response(results,status=400)
        else:
            return Response(results,status=200)
    def delete(self,request,employeeID):
        sql_query="DELETE FROM Employees WHERE employee_id = '"+employeeID+"'"
        results = delete_raw_sql(sql_query)
        if 'message' in results:
            return Response(results,status=400)
        else:
            return Response(results,status=204)


