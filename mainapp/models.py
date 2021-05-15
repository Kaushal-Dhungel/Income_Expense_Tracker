from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.
class Expense(models.Model):
    CHOICES = (
    ('shopping', 'shopping'),
    ('education', 'education'),
    ('entertainment_travel', 'entertainment/travel'),
    ('health', 'health'),
    ('assets', 'assets'),
    ('others', 'others'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length=30, choices = CHOICES)
    amount = models.DecimalField(max_digits= 10, decimal_places=2)
    date = models.DateField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    details = models.TextField(null= False, blank = False)

    def __str__(self):
        return f"{self.user.username}--{self.category}--{self.amount}--{self.created.strftime('%d-%m-%Y')}"

    @property
    def get_todays_expenses(self):
        query = Expense.objects.filter(user = self.user,date = date.today())
        count = query.count()
        if count == 0:
            return "N/A"
        else:
            total = 0
            for x in query:
                total += x.amount
            return total

class Income(models.Model):
    CHOICES = (
    ('salary', 'salary'),
    ('business', 'business'),
    ('sales', 'sales'),
    ('others', 'others'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    category = models.CharField(max_length=30, choices = CHOICES)
    amount = models.DecimalField(max_digits= 10, decimal_places=2)
    date = models.DateField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    details = models.TextField(null= False, blank = False)

    def __str__(self):
        return f"{self.user.username}--{self.category}--{self.created.strftime('%d-%m-%Y')}"

class Todo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    todo_text = models.TextField(null= False, blank = False)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username}--{self.id}"