from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from utils.imports import success, value_e, error, none, restricted, CustomOffSetPagination, get_model_serializer, \
    CustomException
from .functions import get_quiz
from .models import Quiz, Question, Answer, Result, Category
from .serializers import AnswerSerializer, QuizGetSerializer, QuizSerializer, QuestionSerializer, FullQuizSerializer
from rest_framework.response import Response


@extend_schema(request=get_model_serializer(Category), tags=['category'])
class CategoryApi(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = get_model_serializer(Category)


class QuizApi(APIView):
    @extend_schema(parameters=[QuizGetSerializer], tags=['quiz'])
    def get(self, request):
        serializer_param = QuizGetSerializer(data=request.GET)
        serializer_param.is_valid(raise_exception=True)
        queryset = Quiz.objects.all()
        if serializer_param.validated_data.get('my_quiz',None):
            if request.user.is_anonymous:
                raise restricted
            queryset = queryset.filter(user=request.user)
        elif serializer_param.validated_data.get('quiz_id', None):
            queryset = queryset.filter(id=serializer_param.validated_data['quiz_id'])
        quiz_serializer = get_model_serializer(Quiz)
        serializer = quiz_serializer(queryset, many=True)

        return Response(serializer.data)

    @extend_schema(request=QuizSerializer, tags=['quiz'])
    def post(self, request):
        serializer = QuizSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        quiz = serializer.save()
        quiz.user = request.user
        quiz.save()
        return Response(serializer.data)


@extend_schema(request=QuizSerializer, tags=['quiz'])
@api_view(['PUT'])
def put_quiz(request, pk):
    quiz = get_quiz(id=pk, user=request.user)
    serializer = QuizSerializer(instance=quiz, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@extend_schema(request=QuizSerializer, tags=['quiz'])
@api_view(['DELETE'])
def delete_quiz(request, pk):
    quiz = get_quiz(id=pk, user=request.user)
    quiz.delete()
    return success


@extend_schema(request=QuestionSerializer, tags=['question'])
@api_view(['POST'])
def post_question(request):
    serializer = QuestionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success


@extend_schema(request=AnswerSerializer, tags=['answer'])
@api_view(['POST'])
def post_answer(request):
    serializer = AnswerSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return success


@extend_schema(request=FullQuizSerializer, tags=['quiz'])
@api_view(['GET'])
def full_quiz(request, pk):

    quiz = Quiz.objects.filter(id=pk).all().prefetch_related('questions__answers')
    serializer = FullQuizSerializer(quiz, many=True)
    return Response(serializer.data)

