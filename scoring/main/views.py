from django.shortcuts import render
from .config import scoring_items

# Create your views here.
def index(request):
    
    context = {scoring_items}
    return render(request, 'main/index.html', context)