from django.urls import path
from django.http import HttpResponse
from .views import web, result

urlpatterns = [
    path('', web),
    path('result/', result, name='result'),
    
]
