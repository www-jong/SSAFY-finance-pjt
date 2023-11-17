from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .serializers import CustomUserDetailSerializer
from .models import CustomUser
@api_view(['GET'])
def Detail(request, search_name):
    try:
        user = CustomUser.objects.get(username=search_name)
        serializer = CustomUserDetailSerializer(user)
        return Response({'data':serializer.data,'message':'success'}, status=status.HTTP_200_OK)
    except:
        return Response({'message':'error'}, status=status.HTTP_404_NOT_FOUND)