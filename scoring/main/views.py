from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
# from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt


from .config import scoring_items, draw_id
from .models import SingleScoreForm, Interviewer

import json 
import logging
import re
import base64
import functools 


logger = logging.getLogger(__name__) 


# Create your views here.
@login_required
def index(request):
    if request.user.is_staff:
        return HttpResponse("请勿使用管理员账户登录打分页面")
    
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
        
        score = []
        for k in request.POST.keys():
            if "selected-score" in k:
                score.append(request.POST[k])
        score = ",".join(score)
        # logger.info(f"score: {score}")
        
        singlescoreform_id = request.POST["singlescoreform_id"]
        # logger.info(f"singlescoreform_id: {singlescoreform_id}")

        interviewer_pk = request.POST["draw_id"]
        # logger.info(f"interviewer_pk: {interviewer_pk}")

        examiner_pk = request.POST["examiner_pk"]
        # logger.info(f"examiner_pk: {examiner_pk}")

        current_date = request.POST["current_dt"]
        # logger.info(f"current date: {current_date}")

        comment = request.POST["comment"]
        # logger.info(f"comment: {comment}")

        singlescoreform = SingleScoreForm.objects.get(id=singlescoreform_id)
        # logger.info(f"singlescoreform: {singlescoreform}")

        
        singlescoreform.score = score
        singlescoreform.current_date = current_date
        singlescoreform.comment = comment
        singlescoreform.formFinished = True 
        # singlescoreform.interviewer = interviewer_pk
        # singlescoreform.examiner = examiner_pk

        singlescoreform.save()

        
        output_signature_filename = f"signatures/({interviewer_pk})-({examiner_pk})-({current_date}).png"
        ImageData = request.POST.get("sig_url")
        saveSignature(output_signature_filename, ImageData)
        
        
    except Exception as e:
        logger.error(e)
    
    # logger.info(request.POST)
    
    ImageData = request.POST.get("sig_url")
    saveSignature("output.png", ImageData)
    
    return redirect("home")

  

def final(request):
    if not request.user.is_staff:
        return HttpResponse("请使用管理员账户登录")

    interviewers = Interviewer.objects.all()

    context = {
        "interviewers": interviewers,
    }
    return render(request, 'main/final.html', context)

@csrf_exempt
def fetchScore(request):
    interviewer_pk = request.POST["interviewer_pk"]
    logger.info(f"interviewer_pk is {interviewer_pk}")

    finished_forms = SingleScoreForm.objects.filter(interviewer=interviewer_pk, formFinished=True).order_by("examiner")
    if len(finished_forms) <= 2:
        raise Exception("Waiting for more scores")
    
    finished_examiners = [x.examiner.examiner_id for x in finished_forms]
    # print(finished_examiners)
    
    raw_score = finished_forms.values("score")
    data = process_score(raw_score)

    data["finished_examiners"] = finished_examiners
    return JsonResponse(json.dumps(data), safe=False)


def process_score(raw_score):
    
    
    raw_score = [x["score"] for x in raw_score]
    raw_score = [x.split(",") for x in raw_score]
    total_scores = []
    for x in raw_score:
        total_score = functools.reduce(lambda a,b: a+b, [int(y) for y in x])
        total_scores.append(total_score)
    
    all_total_score = functools.reduce(lambda a,b: a+b, total_scores)

    max_score = max(total_scores)
    min_score = min(total_scores)

    final_total_score = all_total_score - max_score - min_score
    final_avg_score = round(final_total_score / (len(total_scores) - 2), 1)

    
    data = {
        "total_scores": total_scores,
        "max_score": max_score,
        "min_score": min_score,
        "final_total_score": final_total_score,
        "final_avg_score": final_avg_score,
    }

    return data