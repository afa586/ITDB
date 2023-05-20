from django.contrib import admin
from django.urls import include, path
from api import views

urlpatterns = [
    path('taniumimport', views.TaniumImport.as_view()),    
    path('documentsimport', views.DocumentImport.as_view()),  
  
]