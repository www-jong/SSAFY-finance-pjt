from django.urls import path
from . import views


urlpatterns = [
    path('exchange/', views.exchange_v2),
    path('save_deposit_products/',views.save_deposit_products),
    path('show_deposit_products/',views.show_deposit_products),
    path('save_saving_products/',views.save_saving_products),
    path('show_saving_products/',views.show_saving_products),
    path('join_deposit_product/',views.join_deposit_product),
    path('join_saving_product/',views.join_saving_product),
    path('news/',views.news),
    path('test/',views.api_test),
]
