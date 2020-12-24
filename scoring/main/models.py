from django.db import models

# Create your models here.
from django.db import models
from datetime import date

class Interviewer(models.Model):
    draw_id = models.CharField(max_length=10)

    def __str__(self):
        return self.draw_id


class Examiner(models.Model):
    examiner_id = models.IntegerField(default=0)

    def __str__(self):
        return self.examiner_id

class SingleScoreForm(models.Model):
    score_1 = models.IntegerField(default=0)
    score_2 = models.IntegerField(default=0)
    score_3 = models.IntegerField(default=0)
    score_4 = models.IntegerField(default=0)
    score_5 = models.IntegerField(default=0)
    comment = models.CharField(max_length=1000)
    sig_filename = models.CharField(max_length=1000)
    date = models.DateField(default=date.today)

    interviewer = models.ForeignKey(Interviewer, on_delete=models.CASCADE)
    examiner = models.ForeignKey(Examiner, on_delete=models.CASCADE)

    def __str__(self):
        return f"({self.interviewer.draw_id})-({self.examiner.examiner_id})-({self.date})"
