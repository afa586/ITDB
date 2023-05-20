from django.contrib import admin
from django.urls import include, path
from itdc import views

urlpatterns = [
    path('', views.HomeView.as_view()),
    path('search', views.SearchView.as_view()),
    path('asset/<action>', views.AssetView.as_view()),       
    path('port/<action>', views.PortView.as_view()),             
    path('software/<action>', views.SoftwareView.as_view()),       
    path('ip/<action>', views.IpView.as_view()),       
    path('report/<reportname>', views.ReportView.as_view()),       
    path('import/<tablename>', views.ImportView.as_view()),       

]