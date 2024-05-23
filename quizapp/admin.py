from django.contrib import admin

from quizapp.models import Quiz, Question, Result, Category

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Result)
admin.site.register(Category)