from django.urls import path,include
from django.views.generic import TemplateView
from .views import test_views,ProductDetailView,login,register


urlpatterns = [
    path('',test_views,name='base'),
    path('products/<str:ct_model>/<str:slug>/',ProductDetailView.as_view(),name='product_detail'),

]