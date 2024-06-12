from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryApi, QuizApi, put_quiz, delete_quiz, post_question, post_answer, full_quiz, send_answer, \
    get_category, try_api, quizes, quiz_get_one, create_quiz, ResultApi, get_my_results

router = DefaultRouter()
router.register(r'category', CategoryApi)
router.register(r'result', ResultApi)


urlpatterns = [
    path('viewset/', include(router.urls)),
    path('quiz/', QuizApi.as_view()),
    path('quiz_update/<int:pk>/', put_quiz),
    path('quiz_delete/<int:pk>/', delete_quiz),
    path('question_create/', post_question),
    path('answer_create/', post_answer),
    path('full_quiz/<int:pk>/', full_quiz),
    path('send_answers/', send_answer),
    path('category_get/', get_category),
    path('try_api/', try_api),
    path('category_quizes/<int:category_id>/', quizes),
    path('quiz/<int:pk>/', quiz_get_one),
    path('quiz_create/', create_quiz),
    path('my_results/', get_my_results)
]
