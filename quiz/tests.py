from django.test import TestCase
import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from .models import *
from django.utils import timezone


class InterviewTests(APITestCase):

    def setUp(self):
        self.one_interview = Interview.objects.create(
            title='Тестовый опрос 1',
            finish_date=timezone.now().date(),
            description='Текст тестового опроса 1',
            is_active=True)

        self.two_interview = Interview.objects.create(
            title='Неактивный (ответов к нему нет)',
            finish_date=timezone.now().date(),
            description='Текст тестового опроса 2',
            is_active=False)

        self.three_interview = Interview.objects.create(
            title='Неактивный (ответ есть только на первый вопрос)',
            finish_date=timezone.now().date(),
            description='Текст тестового опроса 3',
            is_active=False)

        self.que_first = Question.objects.create(
            is_first=True,
            interview=self.one_interview,
            text='Первый вопрос(текстовый)',
            type_que=1,
        )

        self.second_que = Question.objects.create(
            is_first=False,
            interview=self.one_interview,
            text='Второй вопрос(с выбором)',
            type_que=2,
            previous=self.que_first
        )

        self.third_que = Question.objects.create(
            is_first=False,
            interview=self.one_interview,
            text='Третий вопрос(можно несколько вариантов)',
            type_que=3,
            previous=self.second_que
        )

        self.que_not_activ_but_with_answer = Question.objects.create(
            is_first=True,
            interview=self.two_interview,
            text='ВНИМАНИЕ вопрос',
            type_que=1,
        )

        self.que_not_activ = Question.objects.create(
            is_first=False,
            interview=self.two_interview,
            text='ВНИМАНИЕ вопрос',
            type_que=1,
            previous=self.que_not_activ_but_with_answer
        )

        self.first_var = VariantsAnswer.objects.create(
            question=self.second_que,
            text='Первый вариант'
        )

        self.second_var = VariantsAnswer.objects.create(
            question=self.second_que,
            text='Второй вариант'
        )

        self.var3 = VariantsAnswer.objects.create(
            question=self.second_que,
            text='Третий вариант'
        )

        self.var4 = VariantsAnswer.objects.create(
            question=self.second_que,
            text='Четвертый вариант'
        )

        self.var5 = VariantsAnswer.objects.create(
            question=self.second_que,
            text='Пятый вариант'
        )
        user_test1 = User.objects.create_user(username='test', password="Djangosila123")
        user_test1.save()
        self.user_test1_token = Token.objects.create(user=user_test1)
        Answer.objects.create(user=User.objects.first(),interview=self.two_interview, text='ответ',
                              question=self.que_not_activ_but_with_answer)

    def test_que_invalid(self):
        response = self.client.get(
                reverse('que_first', kwargs={"pk": self.one_interview.id}), format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_que_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.get(
                reverse('que_first', kwargs={"pk": self.one_interview.id}), format='json'
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_answer_invalid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.post(
            reverse('que_first', kwargs={"pk": self.one_interview.id}), format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_answer_valid(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.post(
            reverse('que_first', kwargs={"pk": self.one_interview.id}), {'text': 'лалалал', 'user': 1,
                                                                         'interview': '1', 'question': '1',
                                                                         }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_not_aktiv_interview_first_que_get(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.get(
                reverse('que_first', kwargs={"pk": self.two_interview.id})
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_not_aktiv_interview_first_que_post(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.post(
            reverse('que_first', kwargs={"pk": self.two_interview.id}), {'text': 'лалалал', 'user': 1,
                                                                         'interview': '1', 'question': '1'}
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_aktiv_interview_que_post(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.post(
            reverse('que', kwargs={"pk": self.que_not_activ.id}), {'text': 'лалалал', 'user': 1,
                                                                    'interview': '1', 'question': '1'}
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_not_aktiv_interview_que_get(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.get(
            reverse('que', kwargs={"pk": self.que_not_activ.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_three_que(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user_test1_token.key)
        response = self.client.post(
            reverse('que', kwargs={"pk": self.que_not_activ.id}), {'text': 'лалалал', 'user': 1,
                                                                    'interview': '1', 'question': '1'}
        )
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


