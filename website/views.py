from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from.import models 
from elenizado import models as elenizado_models
from about import models as about_models
import json
from django.http import JsonResponse 
from django.core.validators import validate_email

# Create your views here.
def index(request):
    site_info = models.SiteInfo.objects.filter(status=True)[:1].get()
    publication_r = elenizado_models.Publication.objects.all().order_by('-date_add')[:4]
    events_r = elenizado_models.Evenement.objects.all().order_by('-date_add')[:3]
    gallerie = about_models.Gallerie.objects.filter(status=True)
    publication_list = elenizado_models.Publication.objects.all()
    page = request.GET.get('page', 1)
    paginator = Paginator(publication_list, 4)
    try:
        pub = paginator.page(page)
    except PageNotAnInteger:
        pub = paginator.page(1)
    except EmptyPage:
        pub = paginator.page(paginator.num_pages)
    datas = {
             'publication_r':publication_r,
             'events_r':events_r,
             'gallerie':gallerie,
             'site_info':site_info,
             'pub':pub,
    }
    return render(request,'pages/index.html',datas)

def is_newsletter(request):
    message = "" 
    email = request.POST.get('email')
    try:
        validate_email(email)
        isemail = True
        success = False
        print("1")
        newsletter = models.Newsletter(
            email = email,
        )
        newsletter.save()
        print("3")
        success = True
        message = "l'enregistrement a bien été effectué"
    except :
        message = "email incorrect"
        print("2")
    data =   {
    "success":success,
    "message":message,

    }
    return JsonResponse(data,safe=False)
