from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from quizapp.models import Answer, Quiz, Question


class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"
        write_only_fields = ('is_true', 'question')


class QuizGetSerializer(Serializer):
    my_quiz = serializers.BooleanField(required=False)
    quiz_id = serializers.IntegerField(required=False)


class QuizSerializer(ModelSerializer):
    class Meta:
        model = Quiz
        fields = "__all__"
        read_only_fields = ('user',)


class QuestionSerializer(ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class FullAnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'text']


class FullQuestionSerializer(ModelSerializer):
    answers = FullAnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ['text', 'answers']
# , 'answers'


class FullQuizSerializer(ModelSerializer):
    questions = FullQuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = "__all__"


class AnswersSerializer(serializers.Serializer):
    answers = serializers.ListSerializer(child=serializers.IntegerField())
