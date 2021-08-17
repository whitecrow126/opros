from .views import *
from django.urls import path

urlpatterns = [
    # список актвных опросов(для всех пользователей)
    path('', Home.as_view()),

    # пользователь после выбора опроса попадает на первый вопрос
    path('interview/<int:pk>/que_first/', InterviewQuestionFirst.as_view(), name='que_first'),

    # потом он дальше ходит по вопросам и делает ответы
    path('question/<int:pk>/', InterviewQuestion.as_view(), name='que'),

    # добавить пользователя в пройденные
    path('interview_passed_create/<int:pk>/', InterviewPassed.as_view(), name='passed_interview'),

    # посмотреть пройденные опросы
    path('passed_interview/', PassedQuiz.as_view(), name='my_passed_interview'),

    # список всех опрос + создать опрос(только админ)
    path('staff/', StaffHome.as_view()),

    # активировать опрос (админ)
    path('staff/activete_interview/<int:pk>/', ActivateInterview.as_view()),

    # посмотретьи и редактировать вопрос по айди(админ)
    path('staff/question/<int:pk>/', QuestionsRetrieve.as_view()),

    # создать вопрос (админ)
    path('staff/question/create/', StaffQuestionsCreate.as_view()),

    # редактировать опрос(админ)
    path('staff/interview/<int:pk>/', StaffInterviewDetail.as_view()),

    # сделать вариант ответа
    path('staff/variants_answer/create/', AnswerVariantsCreate.as_view()),

    # редактировать вариант ответа
    path('staff/variants_answer/<int:pk>/', AnswerVariantsRetrieve.as_view()),

]
