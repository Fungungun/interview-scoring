from django.db import models

# Create your models here.
from django.db import models
from datetime import date


from django.contrib.auth.models import User
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

class Examiner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    examiner_id = models.IntegerField(default=0)
    room_id = models.IntegerField(default=1)

    is_examiner = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room_id}-{self.examiner_id}"

@receiver(post_save, sender=User)
def create_user_examiner(sender, instance, created, **kwargs):
    if created:
        Examiner.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_examiner(sender, instance, **kwargs):
    instance.examiner.save()

@receiver(post_delete, sender=Examiner)
def post_delete_user(sender, instance, *args, **kwargs):
    instance.user.delete()


class Interviewer(models.Model):
    draw_id = models.CharField(max_length=10)
    room_id = models.IntegerField(default=1)

    def __str__(self):
        return self.draw_id

class SingleScoreForm(models.Model):
    score = models.CharField(max_length=1000, default="")
    comment = models.CharField(max_length=1000)
    sig_filename = models.CharField(max_length=1000)
    date = models.DateField(default=date.today)

    interviewer = models.ForeignKey(Interviewer, on_delete=models.CASCADE)
    examiner = models.ForeignKey(Examiner, on_delete=models.CASCADE)

    formFinished = models.BooleanField(default=False)

    def __str__(self):
        return f"({self.interviewer.draw_id})-({self.examiner.examiner_id})-({self.formFinished})"
