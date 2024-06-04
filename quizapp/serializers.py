from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers
from quizapp.models import Answer, Quiz, Question


class AnswerSerializer(ModelSerializer):
    class Meta:
        model = Answer
        fields = "__all__"
        write_only_fields = ('is_true', 'question')


class QuizGetSerializer(Serializer):
    id = serializers.IntegerField(required=False)


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
    num_question = serializers.IntegerField()

    class Meta:
        model = Quiz
        fields = "__all__"


class AnswersSerializer(serializers.Serializer):
    answers = serializers.ListSerializer(child=serializers.IntegerField())


class FinishQuizSerializer(Serializer):
    answers = serializers.ListField(child=serializers.IntegerField())
    quiz_id = serializers.IntegerField()


class QuestionCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    options = serializers.ListField(child=serializers.CharField())
    correct_index = serializers.IntegerField()


class QuizCreateSerializer(serializers.Serializer):
    quiz_name = serializers.CharField()
    comment = serializers.CharField()
    category_id = serializers.IntegerField()
    duration = serializers.IntegerField(max_value=120)
    questions = serializers.ListField(child=QuestionCreateSerializer())
