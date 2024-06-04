from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=500)
    comment = models.CharField(max_length=1000, null=True, blank=True)
    image = models.ImageField(upload_to='category_images', null=True, blank=True)


    def __str__(self):
        return self.name


class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    comment = models.CharField(max_length=1000, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    created_at = models.DateField(auto_now_add=True)
    duration = models.PositiveIntegerField(default=10)
    image = models.ImageField(upload_to='quiz_images', null=True, blank=True)

    def __str__(self):
        return f"{self.id}. {self.name}"


class Question(models.Model):
    text = models.TextField()
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')

    def __str__(self):
        return self.text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    text = models.TextField()
    is_true = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="results")
    quiz = models.ForeignKey(Quiz, on_delete=models.SET_NULL, related_name='results', null=True)
    correct = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.user.username)

