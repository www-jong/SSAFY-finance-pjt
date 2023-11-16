from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import ArticleSerializer,CommentSerializer
from .models import Article,Comment


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def article_list(request,board_type):
    print('!!!!',board_type)
    if request.method == 'GET':
        articles = get_list_or_404(Article,board_type=board_type)
        print('게시글들',articles)
        for data in articles:
            print(data.user)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        print('!!!!',request.data,request.user) #여기서 지금 request.user는 username 
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET'])
def article_detail(request,board_type ,article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment= Comment.objects.filter(article=article).order_by('created_at')
    if request.method == 'GET':
        ar_serializer = ArticleSerializer(article)
        co_serializer=CommentSerializer(comment,many=True)
        print('게시글들',ar_serializer.data)
        print('댓글들',co_serializer.data,article_pk)
        return Response({'article':ar_serializer.data,'comments':co_serializer.data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def comments_create(request, article_pk,parent_pk):
    print('댓글작성!!')
    article=get_object_or_404(Article,pk=article_pk)
    serializer = CommentSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        if parent_pk:
            parent_Comment=Comment.objects.get(pk=parent_pk)
            serializer.save(user=request.user,article=article,parent_comment=parent_Comment)
        else:
            serializer.save(user=request.user,article=article)
        return Response({'message':'success'})
    return Response({'message': 'fail'})


@api_view(['POST'])
def comments_delete(request, article_pk, comment_pk):
    '''
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, pk=comment_pk)
        if request.user == comment.user:
            comment.delete()
    return redirect('articles:detail', article_pk)
    '''