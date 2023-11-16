from django.urls import path
from . import views


urlpatterns = [
    path('comment/<int:article_pk>/<int:parent_pk>/', views.comments_create),
    path('<str:board_type>/', views.article_list),
    path('<str:board_type>/<int:article_pk>/', views.article_detail),
]
