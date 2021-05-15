from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import resolve, reverse
from django.contrib.auth.models import User
from datetime import date,timedelta
from mainapp.models import *
import json

class TestExpenseView(APITestCase):
    today = date.today()  # django takes this yy--mm-dd format while saving in database
    month_ago = today - timedelta(days=30)

    today_django_format = today.strftime('%d-%m-%Y')  #  but django returns date in str in this dd--mm--yy format 
    url = reverse('expense')

    def setUp(self):
        self.user = User.objects.create(username = "testUserrrr",password = "testinguser12345")
        self.expense = Expense.objects.create(user = self.user,category = "shopping",amount = 500.00,date = self.today,details = "test details")
        self.url_slug = reverse('expense_slug',args = [str(self.expense.id)])
        self.client.force_authenticate(user = self.user)

    def test_expense_get(self):

        data = {'user_id': self.user.id}
        res = self.client.get(self.url,data)

        self.assertEquals(res.status_code,200)

    def test_expense_post(self):

        data = {'source':'shopping','amount':600.00,'date':self.today,'details':"test details"}

        res = self.client.post(self.url,data,format = "json")
        
        self.assertEquals(res.status_code,201)
        self.assertEquals(res.data,{'success from expense'})


    def test_expense_put(self):

        yesterday = self.today - timedelta(days=1)
        data = {'source':'education','amount':400.00,'date':yesterday,'details':"test details modified"}

        res = self.client.put(self.url_slug,data,format = "json")
        
        self.assertEquals(res.status_code,201)
        self.assertEquals(res.data,{'successfully updated'})

    def test_expense_delete(self):
        res = self.client.delete(self.url_slug)
        self.assertEquals(res.status_code,200)
        self.assertEquals(res.data,{'deleted'})


class TestIncomeView(APITestCase):
    today = date.today()  # django takes this yy--mm-dd format while saving in database
    month_ago = today - timedelta(days=30)

    today_django_format = today.strftime('%d-%m-%Y')  #  but django returns date in str in this dd--mm--yy format 
    url = reverse('income')

    def setUp(self):
        self.user = User.objects.create(username = "testUserrrr",password = "testinguser12345")
        self.income = Income.objects.create(user = self.user,category = "salary",amount = 500.00,date = self.today,details = "test details")
        self.url_slug = reverse('income_slug',args = [str(self.income.id)])
        self.client.force_authenticate(user = self.user)

    def test_income_get(self):

        data = {'user_id': self.user.id}
        res = self.client.get(self.url,data)

        self.assertEquals(res.status_code,200)

    def test_income_post(self):

        data = {'source':'salary','amount':600.00,'date':self.today,'details':"test details"}

        res = self.client.post(self.url,data,format = "json")
        
        self.assertEquals(res.status_code,201)
        self.assertEquals(res.data,{'success from income'})


    def test_income_put(self):

        yesterday = self.today - timedelta(days=1)
        data = {'source':'business','amount':400.00,'date':yesterday,'details':"test details modified"}

        res = self.client.put(self.url_slug,data,format = "json")
        
        self.assertEquals(res.status_code,201)
        self.assertEquals(res.data,{'successfully updated'})

    def test_income_delete(self):
        res = self.client.delete(self.url_slug)
        self.assertEquals(res.status_code,200)
        self.assertEquals(res.data,{'deleted'})
         

class TestIncomeExpenseTotalView(APITestCase):
    
    def setUp(self):
        self.user = User.objects.create(username = "testUserrrr",password = "testinguser12345")
        self.url = reverse('total')
        self.data = {'user_id':self.user.id}

    def test_get(self):
        res = self.client.get(self.url,self.data)
        self.assertEquals(res.status_code,200)

class TestGetNameView(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username = "testUserrrr",password = "testinguser12345")
        self.url = reverse('getname')
        self.data = {'user_id':self.user.id}

    def test_get(self):
        res = self.client.get(self.url,self.data)
        self.assertEquals(res.status_code,200)
        self.assertEquals(res.data,{str(self.user.username)})


# class TestRegsiterView(APITestCase):

#     def test_post(self):
#         url = reverse('register')
#         data = {'username':"newuserrr","email":"testemail@testuser.com","password":"testinguser54321"}
#         res = self.client.post(url,data,format = "json")
#         print(res)
#         print(res.data)
#         self.assertEquals(res.status_code,201)


class TestCheckUser(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username = "testUserrrr",email = "testuser@localhost.com",password = "testinguser12345")
        self.url = reverse('checkuser')

    def test_get_with_email_exists(self):
        res = self.client.get(self.url,{'username':"",'email':self.user.email})
        self.assertEquals(res.status_code,200)
        self.assertEquals(res.data,{"True"})

    def test_get_with_email_doesnt_exists(self):
        res = self.client.get(self.url,{'username':"",'email':"dummyemail@localhost.com"})
        self.assertEquals(res.status_code,200)
        self.assertEquals(res.data,{"False"})

    def test_get_with_username_exists(self):
        res = self.client.get(self.url,{'username':self.user.username,'email':""})
        self.assertEquals(res.status_code,200)
        self.assertEquals(res.data,{"True"})

    def test_get_with_username_doesnt_exists(self):
        res = self.client.get(self.url,{'username':"dummyName",'email':""})
        self.assertEquals(res.status_code,200)
        self.assertEquals(res.data,{"False"})

class TestTodoView(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username = "testUserrrr",password = "testinguser12345")
        self.url = reverse('todo')
        self.todo = Todo.objects.create(user = self.user,todo_text = "dummy text")
        self.client.force_authenticate(user = self.user)


    def test_get(self):
        # data = {'user_id': self.user.id}
        res = self.client.get(self.url)
        self.assertEquals(len(res.data),1)
        self.assertEquals(res.status_code,200) 

    def test_post(self):
        data = {'todo_text':"dummy text"}
        res =  self.client.post(self.url,data,format = "json")
        self.assertEquals(res.status_code,201) 

    def test_patch(self):
        todo_text = "dummy text"
        data = {'todo_id':self.todo.id, 'todo_text':todo_text}
        res =  self.client.patch(self.url,data,format = "json")
        self.assertEquals(res.data['todo_text'],todo_text) 
        self.assertEquals(res.status_code,201) 

    def test_delete(self):
        data = {'todo_id':self.todo.id}
        res =  self.client.delete(self.url,data,format = "json")
        self.assertEquals(res.data,{'successfully deleted'}) 
        self.assertEquals(res.status_code,200) 
