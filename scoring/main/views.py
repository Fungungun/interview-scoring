from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder

from .config import scoring_items, draw_id
from .models import SingleScoreForm

import json 
import logging
import re
import base64

logger = logging.getLogger(__name__) 


# Create your views here.
@login_required
def index(request):
    

    examiner = request.user.examiner
    logger.info(f"Examiner {examiner.examiner_id} in room {examiner.room_id} logged in")
    
    # get the first unfinished form
    all_forms = SingleScoreForm.objects.filter(examiner=examiner)
    
    if len(all_forms) == 0:
        return HttpResponse("所有考生均已打分完毕")

    finished_forms = all_forms.filter(formFinished=True)
    finished_forms_dic = finished_forms.values("pk", "score", "comment", "interviewer", "formFinished")
    finished_forms_json = json.dumps(list(finished_forms_dic), cls=DjangoJSONEncoder)

    current_form = all_forms.filter(formFinished=False).order_by('id')[0]
    current_form_json = serializers.serialize("json", [current_form])

    context = {
        "examiner": examiner,
        "current_form": current_form,
        "current_form_json": current_form_json,
        "finished_forms": finished_forms,
        "finished_forms_json": finished_forms_json,
        "scoring_items": scoring_items,
        "colspan": len(scoring_items) - 2,
        }
    return render(request, 'main/index.html', context)


def saveSignature(sig_filename, ImageData):
    dataUrlPattern = re.compile('data:image/(png|jpeg);base64,(.*)$')
    ImageData = dataUrlPattern.match(ImageData).group(2)

    # If none or len 0, means illegal image data
    if ImageData == None or len(ImageData) == 0:
        # PRINT ERROR MESSAGE HERE
        logger.error("No Signature")

    # Decode the 64 bit string into 32 bit
    ImageData = base64.b64decode(ImageData)
    output = open(sig_filename, 'wb')
    output.write(ImageData)
    output.close()

def saveForm(request):
    
    try:
        draw_id = request.POST["draw_id"]
        logger.info(f"draw id: {draw_id}")
        print(type(draw_id))

        examiner_id = request.POST["examiner_id"]
        logger.info(f"examiner id: {examiner_id}")

        current_date = request.POST["current_dt"]
        logger.info(f"current date: {current_date}")

        comment = request.POST["comment"]
        logger.info(f"comment: {comment}")

        # for k in 
        
        output_signature_filename = f"signatures/({draw_id})-({examiner_id})-({current_date}).png"
        ImageData = request.POST.get("sig_url")
        saveSignature(output_signature_filename, ImageData)
        
        
    except Exception as e:
        logger.error(e)
    
    # logger.info(request.POST)
    
    ImageData = request.POST.get("sig_url")
    saveSignature("output.png", ImageData)
    
    return redirect("home")

  
