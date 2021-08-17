from django.contrib import admin

from .models import *

admin.site.register(Interview)
admin.site.register(Answer)
admin.site.register(Question)
admin.site.register(VariantsAnswer)
