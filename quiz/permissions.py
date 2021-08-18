from rest_framework.permissions import BasePermission


class IsPassed(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user
        if obj.interview_questions.count() == user.user_answers.filter(interview=obj).count():
            return True
        return False
