

from django.core.management.base import BaseCommand
from main.models import Examiner, Interviewer, SingleScoreForm
from main.config import room_interviewer, room_examiner
from django.contrib.auth.models import User




class Command(BaseCommand):
    def handle(self, *args, **options):
        for room in room_examiner:
            for i in range(1, room_examiner[room] + 1):
                user = User.objects.create_user(f"kaoguan{room}-{i}", '', f"kaoguan{room}-{i}")
                
                user.examiner.room_id = room
                user.examiner.examiner_id = i
                user.save()
                
        for room in room_interviewer:
            for i in range(1, room_interviewer[room] + 1):
                Interviewer.objects.create(
                    draw_id = f"{room}-{i}",
                    room_id = room,
                )

        for examiner in Examiner.objects.all():
            if examiner.examiner_id == 0:
                continue
            for interviewer in Interviewer.objects.all():
                if interviewer.room_id != examiner.room_id:
                    continue
                SingleScoreForm.objects.create(
                    score="",
                    comment="",
                    sig_filename="",
                    interviewer=interviewer,
                    examiner=examiner,
        )




