from rest_framework.decorators import api_view

from .serializers import UserRegisterSerializer
from utils.imports import *


class RegisterUserApi(APIView):

    @extend_schema(request=UserRegisterSerializer)
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success


@api_view(['GET'])
def user_info(request):

    user_serializer = get_model_serializer(User)
    serializer = user_serializer(request.user)
    return Response(serializer.data)
