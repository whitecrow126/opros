from django.shortcuts import get_object_or_404
from rest_framework.exceptions import NotFound, MethodNotAllowed
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .permissions import IsPassed
from .serializers import InterviewSerializer, AnswerSerializer, QuestionSerializer, InterviewUpdatePassedSerializer, \
    StaffInterviewSerializer, VariantsAnswerSerializer, PassedInterviewSerializer
from rest_framework import generics
from .models import VariantsAnswer, Answer, Question, Interview


# список всех опросов
class Home(generics.ListAPIView):
    serializer_class = InterviewSerializer
    queryset = Interview.objects.filter(is_active=True)


# посмотреть первый вопрос опроса и сделать ответ
class InterviewQuestionFirst(generics.RetrieveAPIView, generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AnswerSerializer
        return QuestionSerializer
    
    # если пользователь не ответил на предыдущий вопрос то нельзя посмотреть на этот
    def get_object(self):
        interview = get_object_or_404(Interview, pk=self.kwargs['pk'])
        que = get_object_or_404(Question, interview=interview, is_first=True)
        if interview.is_active:
            return que
        else:
            if que.question_answers.filter(user=self.request.user):
                return que
            raise NotFound()

    # и если не ответит на прошлый вопрос то ответить на этот нельзя
    def perform_create(self, serializer):
        user = self.request.user
        interview = Interview.objects.filter(pk=self.kwargs['pk'])
        que = Question.objects.filter(interview=interview[0], is_first=True)
        if not interview or not que:
            raise MethodNotAllowed('POST')
        if que[0].question_answers.filter(user=user) or not interview[0].is_active:
            raise MethodNotAllowed('POST')
        if que[0].type_que > 1:
            serializer.text = ''
        serializer.save(user=user, question=que[0], interview=interview[0])


# Смотреть вопрос и делать коммент
class InterviewQuestion(generics.RetrieveAPIView, generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AnswerSerializer
        return QuestionSerializer

    # если пользователь не ответил на предыдущий вопрос то нельзя посмотреть на этот
    def get_object(self):
        qu = get_object_or_404(Question, pk=self.kwargs['pk'])
        previous = qu.previous
        user = self.request.user
        if isinstance(previous, Question):
            if qu.question_answers.filter(user=user):
                return qu
            if qu.interview.is_active and previous.question_answers.filter(user=user):
                return qu
        raise NotFound()

    # если пользователь отвечал на вопрос то опять ответить нельзя
    # и если не ответит на прошлый вопрос то ответить на этот нельзя
    def perform_create(self, serializer):
        user = self.request.user
        que = Question.objects.filter(pk=self.kwargs['pk'], is_first=False)
        if not que:
            raise MethodNotAllowed('POST')
        que = que[0]
        interview = que.interview
        if not que.interview.is_active or que.question_answers.filter(user=user):
            raise MethodNotAllowed('POST')
        if not que.previous.question_answers.filter(user=user):
            raise MethodNotAllowed('POST')
        if que.type_que > 1:
            serializer.text = ''
        serializer.save(user=user, question=que, interview=interview)


# добавляем пользователя в пройденные
class InterviewPassed(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, IsPassed)
    serializer_class = InterviewUpdatePassedSerializer

    def get_object(self):
        inter = get_object_or_404(Interview, pk=self.kwargs['pk'])
        user = self.request.user
        inter.passed.add(user)
        return inter


# активируем опрос (для админа)
class ActivateInterview(generics.RetrieveAPIView):
    permission_classes = (IsAdminUser,)
    serializer_class = InterviewSerializer

    def get_object(self):
        interview = get_object_or_404(Interview, pk=self.kwargs['pk'])
        interview.is_active = True
        interview.save()
        return interview


# список опросов (для админа) + создание
class StaffHome(generics.ListCreateAPIView):
    serializer_class = StaffInterviewSerializer
    queryset = Interview.objects.all()
    permission_classes = (IsAdminUser,)

    def perform_create(self, serializer):
        serializer.save(is_active=False)


# редактировать опрос
class StaffInterviewDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = StaffInterviewSerializer
    queryset = Interview
    permission_classes = (IsAdminUser,)


# создать вопрос
class StaffQuestionsCreate(generics.CreateAPIView):
    serializer_class = QuestionSerializer
    permission_classes = (IsAdminUser,)


# редактировать вопрос
class QuestionsRetrieve(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = QuestionSerializer
    queryset = Question
    permission_classes = (IsAdminUser,)


# создать вариант ответа
class AnswerVariantsCreate(generics.CreateAPIView):
    serializer_class = VariantsAnswerSerializer
    permission_classes = (IsAdminUser,)


# редактировать вариант ответа
class AnswerVariantsRetrieve(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = VariantsAnswerSerializer
    permission_classes = (IsAdminUser,)


# пройденные опросы
class PassedQuiz(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PassedInterviewSerializer

    def get_queryset(self):
        user = self.request.user
        return user.passed_interviews.all()
