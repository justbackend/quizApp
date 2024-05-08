from userapp.serializers import UserRegisterSerializer
from utils.imports import *


class RegisterUserApi(APIView):

    @extend_schema(request=UserRegisterSerializer)
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success
