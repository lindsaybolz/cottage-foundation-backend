from django.contrib import admin
from django.urls import path
from rest_api.views import EmailList, PersonCreate, OneEmail

urlpatterns = [
    path('emails/add/', PersonCreate.as_view(), name='add'),
    path('emails/', EmailList.as_view(), name='emails'),
    path('emails/<int:pk>', OneEmail.as_view(), name='one_email')
]

app_name = 'rest_api'