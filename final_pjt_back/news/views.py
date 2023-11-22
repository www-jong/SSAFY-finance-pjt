from django.shortcuts import render
from django.conf import settings
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
import requests
import urllib.request
import os
import sys
import json

client_id = 'Q1bhPqB15oORhjvRNp48'
client_secret = 'p5UktXCI8P'
encText = urllib.parse.quote('금융')
URL = 'https://openapi.naver.com/v1/search/news.json?query=' + encText

@api_view(['GET'])
def news(request):
    request = urllib.request.Request(URL)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    # if(rescode==200):
    #     response_body = response.read()
    #     print(response_body.decode('utf-8'))
    #     return JsonResponse({ 'response' : response_body.decode('utf-8') })
    # else:
    #     print("Error Code:" + rescode)
    #     return Response({"error": "조회에 실패했습니다"}, status=status.HTTP_404_NOT_FOUND)
    if(rescode==200):
        response_body = response.read()
        return Response(json.loads(response_body.decode('utf-8')), status=status.HTTP_200_OK)
    else:
        return Response({"message": "조회에 실패했습니다."}, status=status.HTTP_404_NOT_FOUND)