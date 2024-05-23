from drf_spectacular.utils import extend_schema
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from quiz_service.utils.imports import success, restricted, get_model_serializer, \
    paginate
from .functions import get_quiz
from .models import Quiz, Result, Category, User
from .serializers import AnswerSerializer, QuizGetSerializer, QuizSerializer, QuestionSerializer, FullQuizSerializer, \
    AnswersSerializer
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
    quiz_id = Quiz.objects.get(id=pk)
    quiz = Quiz.objects.filter(id=pk).prefetch_related('questions__answers')
    serializer = FullQuizSerializer(quiz, many=True)

    Result.objects.create(quiz=quiz_id, user=request.user)

    return Response(serializer.data)


@extend_schema(request=AnswersSerializer)
@api_view(['GET'])
def send_answer(request):
    # serializer = AnswersSerializer(data=request.data)
    # serializer.is_valid(raise_exception=True)
    #
    # questions_number = Quiz.objects.filter(id=pk).first().questions.count()
    # answers = serializer.validated_data['answers']
    # if questions_number < len(answers):
    #     raise CustomException("Javoblar soni savollar sonidan ko'p")

    # categories_create = [Category(name='categories') for i in range(50_000)]
    # Category.objects.bulk_create(categories_create)
    #
    # for i in range(1_000_000):
    #     Category.objects.create(name="character limit and difficulty of typing on feature phone keypads led to the abbreviations The word sent via iMessageText messaging, or texting, is the act of composing and sending electronic messages, typically consisting of alphabetic and numeric characters, between two or more users of mobile devices, desktops/laptops, or another type of compatible computer. Text mfjdsa;fjlsajf;jsfkladjf;jfsakl;fjsa;ljf;sdessages may be sent over a cellular network or may also be sent")
    category = Category.objects.get(id=1)
    user = User.objects.get(id=1)
    # Quiz.objects.bulk_create([Quiz(user=user, category=category, name='Just quiz') for i in range(1, 1000)])

    return Response('hi')


# {
# "answers":[1,2,3]
# }


@api_view(['GET'])
def get_category(request):
    cat = Category.objects.all()
    cat_serializer = get_model_serializer(Category)
    return paginate(cat, cat_serializer, request)
