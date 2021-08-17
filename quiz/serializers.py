from rest_framework import serializers
from .models import *


class VariantsAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantsAnswer
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class QuestionSerializer(serializers.ModelSerializer):
    next_question = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    variants_question = VariantsAnswerSerializer(many=True, read_only=True)
    question_answers = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = '__all__'

    def get_question_answers(self, obj):
        if obj.question_answers.filter(user=self.context['request'].user):
            return AnswerSerializer(obj.question_answers.filter(user=self.context['request'].user), many=True).data
        return []


class InterviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        exclude = ('passed', )


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class InterviewUpdatePassedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interview
        fields = ['id', 'description']


class StaffInterviewSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Interview
        fields = '__all__'


class PassedInterviewSerializer(serializers.ModelSerializer):
    interview_questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Interview
        exclude = ['passed']


