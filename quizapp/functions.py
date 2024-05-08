from quizapp.models import Quiz


def get_quiz(**kwargs):
    return Quiz.objects.get(**kwargs)