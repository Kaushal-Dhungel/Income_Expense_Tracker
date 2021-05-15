from django.test import TestCase, SimpleTestCase
from django.urls import resolve, reverse
from mainapp.views import *
from Itracker.views import *

class TestMainappUrls(SimpleTestCase):
    
    def test_income_url(self):
        url = resolve(reverse("income"))
        self.assertEquals(url.func.view_class,IncomeView) # only func for function based views

    def test_income_slug_url(self):
        url = resolve(reverse("income_slug",args = ["test_slug"]))
        self.assertEquals(url.func.view_class,IncomeView)

    def test_expense_url(self):
        url = resolve(reverse("expense"))
        self.assertEquals(url.func.view_class,ExpenseView) # only func for function based views

    def test_expense_slug_url(self):
        url = resolve(reverse("expense_slug",args = ["test_slug"]))
        self.assertEquals(url.func.view_class,ExpenseView)

    def test_todo_url(self):
        url = resolve(reverse("todo"))
        self.assertEquals(url.func.view_class,TodoView)

class TestProjectUrl(SimpleTestCase):
    
    def test_register_url(self):
        url = resolve(reverse("register"))
        self.assertEquals(url.func.view_class,RegisterView)

    def test_checkuser_url(self):
        url = resolve(reverse("checkuser"))
        self.assertEquals(url.func.view_class,CheckUser)

    def test_getname_url(self):
        url = resolve(reverse("getname"))
        self.assertEquals(url.func.view_class,GetNameView)