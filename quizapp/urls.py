from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryApi, QuizApi, put_quiz, delete_quiz, post_question, post_answer, full_quiz

router = DefaultRouter()
router.register(r'category', CategoryApi)


urlpatterns = [
    path('viewset/', include(router.urls)),
    path('quiz/', QuizApi.as_view()),
    path('quiz_update/<int:pk>/', put_quiz),
    path('quiz_delete/<int:pk>/', delete_quiz),
    path('question_create/', post_question),
    path('answer_create/', post_answer),
    path('full_quiz/<int:pk>', full_quiz),
]