from django.contrib import admin

# Register your models here.

from .models import Interviewer, Examiner, SingleScoreForm, Examiner

admin.site.register(Interviewer)
admin.site.register(Examiner)
admin.site.register(SingleScoreForm)