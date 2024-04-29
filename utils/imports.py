import inspect
import os
import time

import requests
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound, APIException
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.pagination import LimitOffsetPagination
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('TOKEN')
chat_id = os.getenv('MY_CHAT_ID')


User = get_user_model()
success = {'response': "Amaliyot muvaffaqiyatli bajarildi"}
error = {'response': "Xatolik yuz berdi"}
none = {'response': "Kiritilganlar bo'yicha malumot topilmadi"}
value_e = {'response': "Malumotlarni to'g'ri shakilda jo'nating"}
restricted = {'response': "Bu amaliyot uchun sizda ruhsat mavjud emas"}


class CustomException(APIException):
    status_code = 400
    default_detail = {'response': 'Something went wrong'}


class CustomOffSetPagination(LimitOffsetPagination):
    default_limit = 500
    max_limit = 500


def get_user(**kwargs):
    try:
        user = User.objects.get(kwargs)
    except User.DoesNotExist:
        raise CustomException("Bunday foydalanuvchi topilmadi")

    return user


def paginate(instances, serializator, request, **kwargs):
    paginator = CustomOffSetPagination()
    paginated_order = paginator.paginate_queryset(instances, request)

    serializer = serializator(paginated_order, many=True, **kwargs)

    return paginator.get_paginated_response(serializer.data)


def send_me(message):

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message
    }
    requests.post(url, params=data)



