from django.urls import path
from .views import *

urlpatterns = [
    path('income/<slug>/',IncomeView.as_view(), name = "income_slug"),
    path('income/',IncomeView.as_view(), name = "income"),
    path('expense/<slug>/',ExpenseView.as_view(), name = "expense_slug"),
    path('expense/',ExpenseView.as_view(), name = "expense"),
    path('total',IncomeExpenseTotalView.as_view(), name = "total"),
    path('todo/',TodoView.as_view(), name = "todo"),

]
