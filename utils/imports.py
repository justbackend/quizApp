import inspect
import os
import time

import requests
from rest_framework.exceptions import APIException
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.pagination import LimitOffsetPagination
from dotenv import load_dotenv
load_dotenv()
token = os.getenv('TOKEN')
chat_id = os.getenv('MY_CHAT_ID')

User = get_user_model()


class CustomException(APIException):
    status_code = 400
    default_detail = {'response': 'Something went wrong'}


success = Response(data={'response': "Amaliyot muvaffaqiyatli bajarildi"}, status=200)
error = CustomException({'response': "Xatolik yuz berdi"})
none = CustomException({'response': "Kiritilganlar bo'yicha malumot topilmadi"})
value_e = CustomException({'response': "Malumotlarni to'g'ri shakilda jo'nating"})
restricted = CustomException({'response': "Bu amaliyot uchun sizda ruhsat mavjud emas"})


class CustomOffSetPagination(LimitOffsetPagination):
    default_limit = 25
    max_limit = 100


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


def get_model_serializer(model):
    class DynamicModelSerializer(ModelSerializer):
        class Meta:
            pass

    DynamicModelSerializer.Meta.model = model
    DynamicModelSerializer.Meta.fields = '__all__'
    return DynamicModelSerializer


def send_me(message):

    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        'chat_id': chat_id,
        'text': message
    }
    requests.post(url, params=data)



