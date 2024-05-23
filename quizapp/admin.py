from django.contrib import admin

from quizapp.models import Quiz, Question, Result, Category, Answer

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Result)
admin.site.register(Category)
admin.site.register(Answer)