from django.test import TestCase

from mainapp.models import *
from django.contrib.auth.models import User
from datetime import date

class TestModel(TestCase):
    today = date.today()  # django takes this yy--mm-dd format while saving in databse
    today_django_format = today.strftime('%d-%m-%Y')  #  but django returns date in str in this dd--mm--yy format 

    # this gets called before every test method , the instances of models defined inside of this get destroyed after testing, so put everythin inside of this
    def setUp(self):
        user = User.objects.create(username = "testUserrrr",password = "testinguser12345")
        self.expense = Expense.objects.create(user = user,category = "shopping",amount = 500.00,date = self.today,details = "test details")
        self.income = Income.objects.create(user = user,category = "salary",amount = 500.00,date = self.today,details = "test details")
        self.todo = Todo.objects.create(user = user, todo_text = "dummy text")

    def test_expense_str(self):
        expense_str = f"testUserrrr--shopping--500.0--{self.today_django_format}"
        self.assertEqual(str(self.expense),expense_str)

    def test_income_str(self):
        income_str = f"testUserrrr--salary--{self.today_django_format}"
        self.assertEqual(str(self.income),income_str)

    def test_todo_str(self):
        todo_str = f"testUserrrr--{self.todo.id}"
        self.assertEqual(str(self.todo),todo_str)
