from rest_framework import serializers
from .models import *

class ExpenseSerializer(serializers.ModelSerializer):
    # date = serializers.DateField(format="%m-%d-%Y")
    get_todays_expenses = serializers.ReadOnlyField()
    class Meta:
        model = Expense
        fields = "__all__"  

class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Income
        fields = "__all__"  

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = "__all__"  