from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.db import IntegrityError
import requests
import json

def homeView (request,*args, **kwargs):
	return render(request, 'index.html')

class GetNameView(APIView):
	def get(self,request,*args,**kwargs):
		user_id = request.query_params.get('user_id')
		user = User.objects.get(id = user_id)
		return Response({str(user.username)},status= status.HTTP_200_OK)


class RegisterView(APIView):
	def post(self,request,*args,**kwargs):
		username = request.data.get('username')
		email = request.data.get('email')
		password = request.data.get('password')
		# confirm_password = request.data.get('confirm_password')

		try:
			user = User.objects.create_user(username, email, password)
			uri = 'https://etracker.herokuapp.com/api/token/'

			if settings.DEBUG:
				uri = 'http://localhost:8000/api/token/'

			header = {
				"Content-Type": "application/json",
				'username': username,
				'password': password,
			}
			# body = {
			# 	'username': 'kaushal',
			# 	'password': 'hazard54321',
			# }
			# newrequest = Request(uri=uri,http_method=http_method,body=body)
			user.save()
			newreq = requests.post(uri,header)
			# print(newreq.content)
			# print(newreq.json())
			# return Response({"Hahah"},status= status.HTTP_201_CREATED)
			return Response(newreq.json(),status= status.HTTP_201_CREATED)
		
		except IntegrityError:
			return Response({'Username Already Exists. Please Try New Username'},status=status.HTTP_400_BAD_REQUEST)

		except Exception as e:
			return Response({"Unknown Error Occured. Please Try Later"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CheckUser(APIView):
	def get(self,request,*args,**kwargs):
		username = request.query_params.get('username')
		email = request.query_params.get('email')

		if email == '':
			try:
				User.objects.get(username = username)
				return Response({'True'},status=status.HTTP_200_OK)

			except User.DoesNotExist:
				return Response({"False"},status = status.HTTP_200_OK)

			except Exception as e:
				return Response({'Some error occured'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

		else:
			try:
				User.objects.get(email = email)
				return Response({'True'},status=status.HTTP_200_OK)

			except User.DoesNotExist:
				return Response({"False"},status = status.HTTP_200_OK)

			except Exception as e:
				return Response({'Some error occured'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
