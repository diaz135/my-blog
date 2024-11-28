from django.urls import path
from.import views

urlpatterns = [
        path('', views.index, name='index'),
        path('is_newsletter', views.is_newsletter, name='is_newsletter'),
]