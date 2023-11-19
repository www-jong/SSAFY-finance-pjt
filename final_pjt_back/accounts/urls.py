from django.urls import path
from . import views


urlpatterns = [
    path('get_user_data/<search_name>/', views.Detail),
    path('follow/', views.follow),
    path('edit/',views.edit)
]
