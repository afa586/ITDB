from django.contrib import admin
from django.urls import include, path
from document.views import *

urlpatterns = [
    path('', HomeView.as_view()), 
    path('search', SearchView.as_view()),    
    path('documentFilter', DocumentFilterView.as_view()),    
    path('customsearch', CustomSearchView.as_view()),     
    path('report', ReportView.as_view()),    
    path('api/<apiname>', APIView.as_view()),      

]