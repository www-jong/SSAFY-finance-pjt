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
from boards.models import Article,Comment
from boards.serializers import ArticleSerializer,CommentSerializer
from api.serializers import DepositOptionSerializer,DepositProductSerializer
@api_view(['GET'])
def Detail(request, search_name):
    try:
        print(request)
        user = CustomUser.objects.get(username=search_name)
        serializer = CustomUserDetailSerializer(user)
        print('!!!',user)
        user_articles=ArticleSerializer(Article.objects.filter(user=user),many=True)
        user_comments=CommentSerializer(Comment.objects.filter(user=user),many=True)
        user_products=user.joined_deposit_products.all()
        return_product_and_option=[]
        for item in user_products:
            options=item.option.all()
            print(DepositProductSerializer(item).data)
            return_product_and_option.append({'product':DepositProductSerializer(item).data,'option':DepositOptionSerializer(options,many=True).data})
        print(return_product_and_option)
        result={'message':'success','user_articles': user_articles.data, 'user_comments': user_comments.data,'user_data':serializer.data,'user_products':return_product_and_option}
        return Response(result, status=status.HTTP_200_OK)
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

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def edit(request):
    if request.method =='DELETE':
        try:
            user_id=request.data['user_id']
            user=CustomUser.objects.get(id=user_id)
            user.delete()
            print('삭제 완료')
            return Response({'message':'success'},status=status.HTTP_200_OK)  # 추후 스테이터스 변경 필요
        except:
            return Response({'message':'error'},status=status.HTTP_404_NOT_FOUND)
        


