from django.contrib import admin
from django.urls import include, path
from itasset import views

urlpatterns = [
    path('', views.Home.as_view()),      
    path('search', views.SearchView.as_view()),      
    path('asset/<action>',views.AssetView.as_view()),      
    path('user/<action>',views.UserView.as_view()),        
    path('import/<tablename>',views.ImportView.as_view()),        
    path('report/<reportname>',views.ReportView.as_view()),      
    path('api/<apiname>',views.API.as_view()),      
  
]