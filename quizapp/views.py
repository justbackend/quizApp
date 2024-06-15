import requests
from django.db.models import Count
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from utils.imports import success, restricted, get_model_serializer, \
    paginate, send_me
from .functions import get_quiz
from .models import Quiz, Result, Category, User, Answer, Question
from .serializers import AnswerSerializer, QuizGetSerializer, QuizSerializer, QuestionSerializer, FullQuizSerializer, \
    AnswersSerializer, FinishQuizSerializer, QuizCreateSerializer, ResultSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


@extend_schema(request=get_model_serializer(Category), tags=['category'])
class CategoryApi(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = get_model_serializer(Category)


@extend_schema(request=get_model_serializer(Result), tags=['result'])
class ResultApi(ModelViewSet):
    queryset = Result.objects.all()
    serializer_class = get_model_serializer(Result)


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
    question = serializer.save()
    return Response(serializer.data)


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
    quiz = Quiz.objects.filter(id=pk).prefetch_related('questions__answers').annotate(num_question=Count('questions')).first()
    serializer = FullQuizSerializer(quiz)

    return Response(serializer.data)


@extend_schema(request=FinishQuizSerializer)
@api_view(['POST'])
def send_answer(request):
    serializer = FinishQuizSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    count = 0
    for answer_id in serializer.validated_data['answers']:
        answer = Answer.objects.get(id=answer_id)
        if answer.is_true:
            count+=1
    quiz_id = serializer.validated_data['quiz_id']
    quiz = Quiz.objects.get(id=quiz_id)
    Result.objects.create(quiz=quiz, user=request.user, correct=count)

    return Response({'response': count})


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
    serializer = QuizSerializer(quizes, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def quiz_get_one(request, pk):
    quiz = Quiz.objects.get(id=pk)
    serializer = QuizSerializer(quiz)
    return Response(serializer.data)


@extend_schema(request=QuizCreateSerializer)
@api_view(['POST'])
def create_quiz(request):
    serializer = QuizCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    category_id = serializer.validated_data['category_id']
    category = Category.objects.get(id=category_id)
    duration = serializer.validated_data['duration']
    quiz_name = serializer.validated_data['quiz_name']
    comment = serializer.validated_data['comment']
    quiz = Quiz.objects.create(category=category, user=request.user, duration=duration, name=quiz_name, comment=comment)
    questions = serializer.validated_data['questions']
    for question_data in questions:
        count = 0
        question = Question.objects.create(text=question_data['title'], quiz=quiz)
        for answer in question_data['options']:
            count += 1
            is_correct = True if count == question_data['correct_index'] else False
            Answer.objects.create(is_true=is_correct, question=question, text=answer)
    return Response('hi')


@extend_schema(tags=['result'])
@api_view(['GET'])
def get_my_results(request):
    if request.user.is_anonymous:
        raise restricted
    result = Result.objects.filter(user=request.user)
    serializer = ResultSerializer(result, many=True)
    return Response(serializer.data)


