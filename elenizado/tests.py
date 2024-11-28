from django.db import models
from tinymce.models import HTMLField
from django.utils.text import slugify
from datetime import datetime
from website.models import SiteInfo
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify
from django.http import JsonResponse
from django.core.validators import validate_email
from .models import about_models  

# Models
class Categorie(models.Model):
    nom = models.CharField(max_length=255)
    description = models.TextField()
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Categorie'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.nom

class Publication(models.Model):
    titre = models.CharField(max_length=255)
    description = HTMLField()
    image = models.ImageField(upload_to='image/publication')
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE, related_name='categorie_publication')
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = '-'.join((slugify(self.titre), slugify(datetime.now().microsecond)))
        super(Publication, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Publication'
        verbose_name_plural = 'Publications'

    def __str__(self):
        return self.titre

class Commentaire(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='publication_commentaire')
    nom = models.CharField(max_length=255)
    email = models.EmailField(null=True)
    commentaire = models.TextField(null=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Commentaire'
        verbose_name_plural = 'Commentaires'

    def __str__(self):
        return self.nom

class ReponseCommentaire(models.Model):
    commentaire = models.ForeignKey(Commentaire, on_delete=models.CASCADE, related_name='reponse_commentaire', null=True)
    nom = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    reponse = models.TextField(null=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Reponse Commentaire'
        verbose_name_plural = 'Reponses Commentaires'

    def __str__(self):
        return self.nom

class Like(models.Model):
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='like_publication')
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'like'
        verbose_name_plural = 'likes'

    def __str__(self):
        return self.publication.titre

class Evenement(models.Model):
    image = models.ImageField(upload_to='evenemant/image')
    description = HTMLField()
    titre = models.CharField(max_length=255)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)
    slug = models.SlugField(unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = '-'.join((slugify(self.titre), slugify(datetime.now().microsecond)))
        super(Evenement, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Evenement'
        verbose_name_plural = 'Evenements'

    def __str__(self):
        return self.titre

class Cours(models.Model):
    titre = models.CharField(max_length=255)
    niveau = models.CharField(max_length=255)
    annee = models.IntegerField()
    description = models.TextField()
    image = models.ImageField(upload_to="cours/image", default="cours/pdf.png")
    cours = models.FileField(upload_to='cours/cours')
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Cours'
        verbose_name_plural = 'Cours'

    def __str__(self):
        return self.titre

class Textes(models.Model):
    titre = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to="textes/image", default="cours/pdf.png")
    pdf = models.FileField(upload_to="pdf/textes", null=True)
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Texte de référence'
        verbose_name_plural = 'Textes de références'

    def __str__(self):
        return self.titre

class Video(models.Model):
    titre = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to="video/image", default="video/video.png")
    video = models.URLField()
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Vidéo'
        verbose_name_plural = 'Vidéos'

    def __str__(self):
        return self.titre

    @property
    def get_video(self):
        try:
            data = self.video.rsplit("=")
            return data[1]
        except:
            pass


# Views
def timeline(request):
    site_info = SiteInfo.objects.filter(status=True)[:1].get()
    gallerie = about_models.Gallerie.objects.filter(status=True)
    events_r = Evenement.objects.all().order_by('-date_add')[:3] 
    publication = Publication.objects.filter(status=True).all()
    page = request.GET.get('page', 1)
    paginator = Paginator(publication, 4)
    try:
        pub = paginator.page(page)
    except PageNotAnInteger:
        pub = paginator.page(1)
    except EmptyPage:
        pub = paginator.page(paginator.num_pages)
    datas = {
        "publication": publication,
        "gallerie": gallerie,
        "events_r": events_r,
        'pub': pub,
    }
    return render(request, "pages/list-two-column.html", datas)

def detail(request, slug):
    site_info = SiteInfo.objects.filter(status=True)[:1].get()
    publication_r = Publication.objects.all().order_by('-date_add')[:3]
    publication = Publication.objects.get(slug=slug)
    gallerie = about_models.Gallerie.objects.filter(status=True)
    events_r = Evenement.objects.all().order_by('-date_add')[:3]
    datas = {
        "publication": publication,
        "publication_r": publication_r,
        "events_r": events_r,
        "gallerie": gallerie,
        'site_info': site_info,
    }
    return render(request, "pages/detail-standart.html", datas)

def cours(request):
    site_info = SiteInfo.objects.filter(status=True)[:1].get()
    events_r = Evenement.objects.all().order_by('-date_add')[:3]
    gallerie = about_models.Gallerie.objects.filter(status=True)
    cours = Cours.objects.filter(status=True).all()
    page = request.GET.get('page', 1)
    paginator = Paginator(cours, 4)
    try:
        cour = paginator.page(page)
    except PageNotAnInteger:
        cour = paginator.page(1)
    except EmptyPage:
        cour = paginator.page(paginator.num_pages)
    datas = {
        "cours": cours,
        "events_r": events_r,
        "gallerie": gallerie,
        "cour": cour,
    }
    return render(request, "pages/cours.html", datas)

def video(request):
    site_info = SiteInfo.objects.filter(status=True)[:1].get()
    video = Video.objects.filter(status=True)
    datas = {
        "video": video,
    }
    return render(request, "pages/video-custom-player.html", datas)

def evenement(request):
    site_info = SiteInfo.objects.filter(status=True)[:1].get()
    evenement = Evenement.objects.filter(status=True).all()
    events_r = Evenement.objects.all().order_by('-date_add')[:3]
    gallerie = about_models.Gallerie.objects.filter(status=True)
    publication = Publication.objects.filter(status=True).all()
    page = request.GET.get('page', 1)
    paginator = Paginator(evenement, 4)
    try:
        even = paginator.page(page)
    except PageNotAnInteger:
        even = paginator.page(1)
    except EmptyPage:
        even = paginator.page(paginator.num_pages)
    datas = {
        "evenement": evenement,
        "events_r": events_r,
        "gallerie": gallerie,
        "pub": publication,
        "even": even,
    }
    return render(request, "pages/evenement.html", datas)

# Helper function for AJAX response
def verify_email(request):
    email = request.GET.get('email', None)
    try:
        validate_email(email)
        return JsonResponse({'valid': True})
    except:
        return JsonResponse({'valid': False})
