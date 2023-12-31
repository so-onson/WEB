from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.db.models import Sum
from django.db.models.functions import Coalesce

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    avatar = models.ImageField()


class Tag(models.Model):
    tag_name = models.CharField(max_length=25)

    def __str__(self):
        return self.tag_name


class QuestionManager(models.Manager):
    def in_rating_order(self):
        queryset = self.get_queryset()
        return queryset.order_by('-likes')


    def by_tag(self, tag_name):
        queryset = self.get_queryset()
        return queryset.filter(tags__tag_name__exact=tag_name)


class Question(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    likes = models.IntegerField(default=0)

    @property
    def answers_count(self):
        return self.answers.count()

    objects = QuestionManager()


class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    likes = models.IntegerField(default=0)



class QuestionLike(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=0)


class AnswerLike(models.Model):
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.SmallIntegerField(default=0)