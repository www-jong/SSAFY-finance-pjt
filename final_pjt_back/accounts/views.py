from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from django.shortcuts import get_object_or_404, get_list_or_404
from .serializers import CustomUserDetailSerializer
from .models import CustomUser
from rest_framework.decorators import permission_classes
@api_view(['GET'])
def Detail(request, search_name):
    try:
        print(request)
        user = CustomUser.objects.get(username=search_name)
        serializer = CustomUserDetailSerializer(user)
        return Response({'data':serializer.data,'message':'success'}, status=status.HTTP_200_OK)
    except:
        return Response({'message':'error'}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def follow(request):
    print('도달',request.data['from_user_id'])
    from_user=get_object_or_404(get_user_model(),pk=request.data['from_user_id'])
    to_user=get_object_or_404(get_user_model(),pk=request.data['to_user_id'])
    message=''
    if to_user.followers.filter(pk=request.data['from_user_id']).exists():
        to_user.followers.remove(from_user)
        message='unfollowed'
    else:
        to_user.followers.add(from_user)
        message='followed'
        
    print('성공')
    return Response({'message':message}, status=status.HTTP_200_OK)
