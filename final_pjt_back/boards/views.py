from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from django.contrib.auth import get_user_model
# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated,IsAdminUser

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import ArticleSerializer,CommentSerializer
from .models import Article,Comment


@api_view(['GET', 'POST','DELETE'])
@permission_classes([IsAuthenticated])
def article_list(request,board_type):
    print('!!!!',board_type)
    if request.method == 'GET':
        try:
            articles=Article.objects.filter(board_type=board_type)
            print('게시글들',articles)
            for data in articles:
                print(data.user)
            serializer = ArticleSerializer(articles, many=True)
            return Response({'data':serializer.data,'message':'success'})
        except:
            print('조회실패')
            return Response({'message':'fail'},status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        print('!!!!',request.data,request.user) #여기서 지금 request.user는 username 
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response({'data':serializer.data,'message':'success'}, status=status.HTTP_201_CREATED)
    elif request.method=='DELETE':
        article=Article.objects.get(pk=request.data['article_id'])
        article.delete()
        return Response({'message':'success'},status=status.HTTP_204_NO_CONTENT)
        print('DELETE')

@api_view(['GET', 'DELETE'])
def article_detail(request, board_type, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    comment= Comment.objects.filter(article=article).order_by('created_at')
    if request.method == 'GET':
        ar_serializer = ArticleSerializer(article)
        co_serializer=CommentSerializer(comment,many=True)
        print('게시글들',ar_serializer.data)
        print('댓글들',co_serializer.data,article_pk)
        return Response({'article':ar_serializer.data,'comments':co_serializer.data})
    if request.method == 'DELETE':
        article = get_object_or_404(Article, pk=article_pk)
        if request.user != article.user:
            return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)
        article.delete()
        return Response({'message': '게시글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)

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

    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def article_like(request):
    print('도달',request.data['from_user_id'])
    from_user=get_object_or_404(get_user_model(),pk=request.data['from_user_id'])
    to_article=get_object_or_404(Article,pk=request.data['to_article_id'])
    message=''
    if to_article.like_users.filter(pk=request.data['from_user_id']).exists():
        to_article.like_users.remove(from_user)
        message='unfollowed'
    else:
        to_article.like_users.add(from_user)
        message='followed'
        
    print('성공')
    return Response({'message':message}, status=status.HTTP_200_OK)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def comment_update(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, article_id=article_pk)

    if request.user != comment.user:
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = CommentSerializer(comment, data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def comments_delete(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk, article_id=article_pk)

    # 댓글 작성자와 현재 사용자가 같은지 확인
    if request.user != comment.user:
        return Response({'message': '권한이 없습니다.'}, status=status.HTTP_403_FORBIDDEN)

    comment.delete()
    return Response({'message': '댓글이 삭제되었습니다.'}, status=status.HTTP_204_NO_CONTENT)