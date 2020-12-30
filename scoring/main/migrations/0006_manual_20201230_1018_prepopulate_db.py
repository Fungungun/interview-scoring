from django.db import migrations, models
from main.config import room_interviewer, room_examiner
from django.contrib.auth.models import User


def PrePopulateDB(apps, schema_editor):
    
    # populate examiner and user
    Examiner = apps.get_model('main', 'Examiner')
    for room in room_examiner:
        for i in range(1, room_examiner[room] + 1):
            user = User.objects.create_user(f"kaoguan{room}-{i}", '', f"kaoguan{room}-{i}")
            
            user.examiner.room_id = room
            user.examiner.examiner_id = i
            user.save()
            
    # populate interviewer 
    Interviewer = apps.get_model('main', 'Interviewer')
    for room in room_interviewer:
        for i in range(1, room_interviewer[room] + 1):
            Interviewer.objects.create(
                draw_id = f"{room}-{i}",
                room_id = room,
            )

    SingleScoreForm = apps.get_model('main', 'SingleScoreForm')
    for examiner in Examiner.objects.all():
        for interviewer in Interviewer.objects.all():
            SingleScoreForm.objects.create(
                score="",
                comment="",
                sig_filename="",
                interviewer=interviewer,
                examiner=examiner,
            )


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20201230_1407'),
    ]

    operations = [
        migrations.RunPython(PrePopulateDB),
    ]
