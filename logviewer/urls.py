from django.contrib import admin
from django.urls import include, path
from logviewer import views

urlpatterns = [
    path('', views.NetEventLogList.as_view()),      
    path('netlog/list', views.NetEventLogList.as_view()),      
    path('netlogsolution/list', views.NetEventSolutionList.as_view()),      
    path('netlogsolution/add', views.NetEventSolutionAdd.as_view()),     
    path('netlogsolution/detail/<int:pk>', views.NetEventSolutionDetail.as_view()),     
    path('netlogsolution/edit/<int:pk>', views.NetEventSolutionEdit.as_view()),     
    path('netlogsolution/causeedit/<int:pk>', views.NetEventSolutionCauseEdit.as_view()),     
    path('netlogsolution/approve/<int:pk>', views.NetEventSolutionApprove.as_view()),    
    path('netlogsolution/review/<int:pk>', views.NetEventSolutionReview.as_view()),    
    path('netlogsolution/unapprove/<int:pk>', views.NetEventSolutionUnApprove.as_view()),    
    
  
]