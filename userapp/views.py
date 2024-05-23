from .serializers import UserRegisterSerializer
import quiz_service.utils.imports


class RegisterUserApi(APIView):

    @extend_schema(request=UserRegisterSerializer)
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return success
