from django.urls import path
from .views import test_views


urlpatterns = [
    path('',test_views,name='base')
]