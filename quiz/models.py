from django.contrib.auth.models import User
from django.db import models


class Interview(models.Model):
    title = models.CharField(verbose_name='Название', max_length=30)
    start_date = models.DateField(auto_now_add=True, verbose_name='Дата старта')
    finish_date = models.DateField(verbose_name='Дата окончания')
    description = models.TextField(verbose_name='Описание')
    is_active = models.BooleanField(default=False, verbose_name='Активно')
    passed = models.ManyToManyField(User, blank=True, related_name='passed_interviews', verbose_name='Пройдено')

    def __str__(self):
        return self.title


class Question(models.Model):
    TYPE_CHOICES = (
        (1, "Text"),
        (2, "One_version"),
        (3, "Several_variants"),
    )
    is_first = models.BooleanField(default=False, verbose_name='Первый')
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='interview_questions', verbose_name='К опросу')
    text = models.TextField(verbose_name='Текст вопроса')
    type_que = models.IntegerField(choices=TYPE_CHOICES, default=1, verbose_name='Тип вопроса')
    previous = models.ForeignKey('self', on_delete=models.CASCADE, related_name='next_question', blank=True, null=True, verbose_name ='Предыдущий')

    def __str__(self):
        return self.text


class VariantsAnswer(models.Model):
    question = models.ForeignKey(Question, related_name='variants_question', on_delete=models.CASCADE, verbose_name='К вопросу')
    text = models.TextField(verbose_name='Вариант ответа')

    def __str__(self):
        return f'Вариант |{self.text}'


class Answer(models.Model):
    interview = models.ForeignKey(Interview, on_delete=models.CASCADE, related_name='interview_answers', verbose_name='К вопросу')
    user = models.ForeignKey(User, verbose_name='Юзер', on_delete=models.CASCADE, related_name='user_answers')
    question = models.ForeignKey(Question, related_name='question_answers', on_delete=models.CASCADE, verbose_name='На вопрос')
    text = models.TextField(verbose_name='Ответ', null=True, blank=True)
    variant = models.ManyToManyField(VariantsAnswer, blank=True, verbose_name='Вариант', related_name='answer_variants')

    def __str__(self):
        return f'ответ на {self.question}'