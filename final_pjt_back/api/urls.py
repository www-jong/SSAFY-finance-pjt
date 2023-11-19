from django.urls import path
from . import views


urlpatterns = [
    path('exchange/', views.exchange_v2),
    path('save_deposit_products/',views.save_deposit_products),
    path('save_saving_products/',views.save_saving_products),
    path('test/',views.api_test),
]
