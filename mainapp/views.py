from django.shortcuts import render
from .models import *
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
import json
from datetime import date,timedelta

# Create your views here.
 
class ExpenseView(APIView):
    def get(self,request,*args, **kwargs):
        user_id = request.query_params.get('user_id')
        startDate = request.query_params.get('startDate')
        endDate = request.query_params.get('endDate')

        today = date.today()
        month_ago = today - timedelta(days=30)

        if startDate == "":
            startDate = None

        if endDate == "":
            endDate = None

        try:
            if startDate == None and endDate == None:
                expenses = Expense.objects.filter(user = user_id)
            
            else:
                if startDate == None or startDate == '':
                    expenses = Expense.objects.filter(user = user_id,date__range = [month_ago,endDate])
                
                elif endDate == None:
                    expenses = Expense.objects.filter(user = user_id,date__range = [startDate,today])

                else:
                    expenses = Expense.objects.filter(user = user_id,date__range = [startDate,endDate])


            expenses = ExpenseSerializer(expenses,many = True)
            return Response(expenses.data, status = status.HTTP_200_OK)

        except Exception as e:
            return Response({"not found"},status=status.HTTP_400_BAD_REQUEST)


    def post(self,request,*args,**kwargs):

        parsed = json.loads(request.body)

        # hardcode this shit, js sucks man
        category =  parsed['source']
        
        data = {
            'user' : request.user.id,
            'category' : category,
            'amount' : parsed['amount'],
            'date' : parsed['date'],
            'details' : parsed['details']
        }

        try:
            serializer = ExpenseSerializer(data = data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"success from expense"}, status = status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response({"success from expense"}, status = status.HTTP_201_CREATED)

    
    def put(self,request,slug,*args,**kwargs):
        parsed = json.loads(request.body)
        item = Expense.objects.get(id = slug,user = request.user.id)
        # print(item)
        data = {
            'user' : request.user.id,
            'category': parsed['source'],
            'amount': parsed['amount'],
            'date': parsed['date'],
            'details': parsed['details'],
        }
        serializer = ExpenseSerializer(item,data = data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({"successfully updated"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,slug,*args, **kwargs):
        try:
            item = Expense.objects.get(id = slug,user = request.user.id)
            item.delete()
            return Response({'deleted'}, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({'sorry'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IncomeView(APIView):
    def get(self,request,*args, **kwargs):
        user_id = request.query_params.get('user_id')
        startDate = request.query_params.get('startDate')
        endDate = request.query_params.get('endDate')

        today = date.today()
        month_ago = today - timedelta(days=30)

        if startDate == "":
            startDate = None

        if endDate == "":
            endDate = None

        try:

            if startDate == None and endDate == None:
                incomes = Income.objects.filter(user = user_id)
                
            else:
                if startDate == None or startDate == '':
                    incomes = Income.objects.filter(user = user_id,date__range = [month_ago,endDate])
                
                elif endDate == None:
                    incomes = Income.objects.filter(user = user_id,date__range = [startDate,today])

                else:
                    incomes = Income.objects.filter(user = user_id,date__range = [startDate,endDate])

            incomes = IncomeSerializer(incomes,many = True)
            return Response(incomes.data, status = status.HTTP_200_OK)

    
        except Exception as e:
            return Response({"not found"},status=status.HTTP_400_BAD_REQUEST)

    def post(self,request,*args,**kwargs):
        parsed = json.loads(request.body)

        # hardcode this shit, js sucks man
        category =  parsed['source']
        data = {
            'user' : request.user.id,
            'category' : category,
            'amount' : parsed['amount'],
            'date' : parsed['date'],
            'details' : parsed['details']
        }

        try:
            serializer = IncomeSerializer(data = data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"success from income"}, status = status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response({"success from income"}, status = status.HTTP_201_CREATED)


    def put(self,request,slug,*args,**kwargs):
        parsed = json.loads(request.body)
        item = Income.objects.get(id = slug,user = request.user.id)
        data = {
            'user' : request.user.id,
            'category': parsed['source'],
            'amount': parsed['amount'],
            'date': parsed['date'],
            'details': parsed['details'],
        }
        serializer = IncomeSerializer(item,data = data)
        try:
            if serializer.is_valid():
                serializer.save()
                return Response({"successfully updated"}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,slug,*args, **kwargs):
        try:
            item = Income.objects.get(id = slug,user = request.user.id)
            item.delete()
            return Response({'deleted'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'sorry'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class IncomeExpenseTotalView(APIView):

    def get_total(self,query):
        count = query.count()
        if count == 0:
            return 0
        else:
            total = 0
            for x in query:
                total += x.amount
            return total

    def get_todays_total(self,modal,user_id):
        try:
            query = modal.objects.filter(user = user_id,date = date.today())
            return self.get_total(query)

        except Exception as e:
            print(e)
            return 0

    def get_monthly_total(self,modal,user_id):
        try:
            today = date.today()
            month_ago = today - timedelta(days=30)
            # print(today,month_ago)
            query = modal.objects.filter(user = user_id,date__range = [month_ago,today])
            return self.get_total(query)

        except Exception as e:
            print(e)
            return 0

    def get(self,request,*args,**kwargs):
        user_id = request.query_params.get('user_id')
        total_dict = []
        total_dict.append(self.get_todays_total(Expense,user_id))
        total_dict.append(self.get_monthly_total(Expense,user_id))
        total_dict.append(self.get_todays_total(Income,user_id))
        total_dict.append(self.get_monthly_total(Income,user_id))
        return Response(total_dict,status = status.HTTP_200_OK)

class TodoView(APIView):
    def get(self,request,*args,**kwargs):
        # user_id = request.query_params.get('user_id')
        user_id = request.user
        try:
            todos = Todo.objects.filter(user = user_id).order_by('-id')[0:]
            serializer = TodoSerializer(todos,many= True)
            return Response(serializer.data, status = status.HTTP_200_OK)

        except Exception as e:
            return Response([], status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self,request,*args,**kwargs):
        parsed = json.loads(request.body)
        data = {
            'user' : request.user.id,
            'todo_text': parsed['todo_text']
        }

        try:
            serializer = TodoSerializer(data = data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response({"some error occured"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self,request,*args,**kwargs):
        parsed = json.loads(request.body)
        item_id = parsed['todo_id']
        data = {
            'user' : request.user.id,
            'todo_text': parsed['todo_text']
        }

        todo_item = Todo.objects.get(id = item_id)

        if todo_item.user != request.user:
            return Response({"some error occured"}, status = status.HTTP_401_UNAUTHORIZED)  # verify this

        try:
            serializer = TodoSerializer(todo_item,data = data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status = status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({"some error occured"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self,request,*args,**kwargs):
        parsed = json.loads(request.body)
        item_id = parsed['todo_id']
        todo_item = Todo.objects.get(id = item_id)

        if todo_item.user != request.user:
            return Response({"some error occured"}, status = status.HTTP_401_UNAUTHORIZED)  # verify this

        try:
            todo_item.delete()
            return Response({"successfully deleted"}, status = status.HTTP_200_OK)
        
        except Exception as e:
            print(e)
            return Response({"some error occured"}, status = status.HTTP_500_INTERNAL_SERVER_ERROR)