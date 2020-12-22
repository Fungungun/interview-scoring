from django.shortcuts import render, redirect
from .config import scoring_items, draw_id, examiner_id
import logging
import re
import base64

logger = logging.getLogger(__name__) 

# Create your views here.
def index(request):
    context = {
        "draw_id": draw_id,
        "scoring_items": scoring_items,
        "colspan": len(scoring_items) - 2,
        "examiner_id": examiner_id,
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

  
