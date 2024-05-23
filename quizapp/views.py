import requests
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from utils.imports import success, restricted, get_model_serializer, \
    paginate
from .functions import get_quiz
from .models import Quiz, Result, Category, User, Answer
from .serializers import AnswerSerializer, QuizGetSerializer, QuizSerializer, QuestionSerializer, FullQuizSerializer, \
    AnswersSerializer, FinishQuizSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


@extend_schema(request=get_model_serializer(Category), tags=['category'])
class CategoryApi(ModelViewSet):
    permission_classes = [AllowAny,]
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
    quiz = Quiz.objects.filter(id=pk).prefetch_related('questions__answers')
    serializer = FullQuizSerializer(quiz, many=True)

    return Response(serializer.data)


@extend_schema(request=FinishQuizSerializer)
@api_view(['GET'])
def send_answer(request):
    serializer = FinishQuizSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    count = 0
    for answer_id in serializer.validated_data['answers']:
        answer = Answer.objects.get(id=answer_id)
        if answer.is_true:
            count+=1
    quiz_id = serializer.validated_data['quiz_id']
    Result.objects.create(quiz=quiz_id, user=request.user, correct=count)

    return success


@api_view(['GET'])
def get_category(request):
    cat = Category.objects.all()
    cat_serializer = get_model_serializer(Category)
    return paginate(cat, cat_serializer, request)


@api_view(['GET'])
def try_api(request):
    token = '6798739793:AAGZ8hFVcg-z4S5avYDFwo5doSRe0zqBNX8'
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {
        'chat_id': 6050173548,
        'text': "It is working"
    }
    response = requests.post(url, params=data)
    return Response(response.json())


@api_view(['GET'])
def quizes(request, category_id):
    quizes = Quiz.objects.filter(category__id=category_id)
    serializer = QuizGetSerializer(quizes, many=True)
    return Response(serializer.data)