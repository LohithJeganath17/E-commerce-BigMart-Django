from django.contrib import admin
from django.urls import path
from .views import register,login,logout,activate,dashboard,forgotpassword,resetpassword_validate,resetpassword


urlpatterns = [
    path('register/',register,name = 'register'),
    path('login/',login,name = 'login'),
    path('logout/',logout,name = 'logout'),
    path('dashboard/',dashboard,name = 'dashboard'),
    #path('',dashboard,name = 'dashboard'),
    
    path('activate/<uidb64>/<token>/',activate,name = 'activate'),
    path('forgotpassword/',forgotpassword,name = 'forgotpassword'),
    path('resetpassword_validate/<uidb64>/<token>/',resetpassword_validate,name = 'resetpassword_validate'),
    path('resetpassword/',resetpassword,name = 'resetpassword'),
] 
