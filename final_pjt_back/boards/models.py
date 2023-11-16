from django.db import models
from django.conf import settings

class Article(models.Model):
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='liked_articles')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image= models.ImageField(blank=True)
    board_type=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    article=models.ForeignKey(Article, on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content= models.TextField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='liked_comments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)