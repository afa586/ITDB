from django.urls import include, path
from .views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', login_view,name='login'),
    path('logout/', logout_view,name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(),name='password_change'),
    path('password_change/done/', passwordChangeDone_view,name='password_change_done'),

]
