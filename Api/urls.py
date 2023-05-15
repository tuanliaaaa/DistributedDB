
from django.urls import path
from .views import ListUser,ListInvoice,EmployeeByID
urlpatterns = [
    path('ListUser',ListUser.as_view()),
    path('ListInvoice',ListInvoice.as_view()),
    path('EmployeeByID/<str:employeeID>',EmployeeByID.as_view())
]
