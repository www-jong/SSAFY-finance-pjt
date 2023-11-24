from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
import requests
from datetime import datetime,date,timedelta
from pytz import timezone
from .models import ExchangeDate,ExchangeInfo,DepositProduct,DepositOption,SavingProduct,SavingOption
from .serializers import ExchangeDateSerializer,ExchangeInfoSerializer,DepositProductSerializer,DepositOptionSerializer,SavingOptionSerializer,SavingProductSerializer
from .forms import ExchangeInfoForm
import pprint
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import urllib.request
import os
import sys
import json
import quandl
import numpy as np
import pandas as pd
import random
from sklearn.metrics.pairwise import cosine_similarity
from accounts.models import CustomUser
from accounts.serializers import CustomUserDetailSerializer
BASE_URL = 'http://finlife.fss.or.kr/'
DEPOSIT_API_URL = 'finlifeapi/depositProductsSearch.json'
SAVING_API_URL = 'finlifeapi/savingProductsSearch.json'




def time_formmating(now="",type="to_db"):
    if not now:
        now=datetime.now()
    print('now :',now)
    kr_timezone = timezone('Asia/Seoul')
    now_kr = now.astimezone(kr_timezone)
    formatted_date = now_kr.strftime('%Y%m%d') if type=="to_db" else now_kr.strftime('%Y-%m-%d')
    return formatted_date

def finance_data_divider(URL,params):
    res_data=requests.get(URL,params=params).json()['result']
    data=res_data['baseList']
    option_data=res_data['optionList']
    max_page_no=res_data['max_page_no']
    total_count=res_data['total_count']
    err_cd=res_data['err_cd']
    return data,max_page_no,total_count,err_cd,option_data

def finance_data_handler(product_result,option_result):
    tmp={}
    for item in product_result:
        item['code']=item['fin_co_no']+'_'+item['fin_prdt_cd']
        if item['code'] not in tmp:
            tmp[item['code']]={'product':item}
        else:
            print('겹침')
    for item in option_result:
        item['code']=item['fin_co_no']+'_'+item['fin_prdt_cd']
        if 'option' in tmp[item['code']]:
            tmp[item['code']]['option'].append(item)
        else:
            tmp[item['code']]['option']=[item]
    print('tmp 결과',len(tmp))
    return tmp


@api_view(['GET'])
def exchange_v2(request):
    REQUEST_DATE=request.GET.get('REQUEST_DATE',None)
    print('오늘?',date.today())
    if REQUEST_DATE:
        REQUEST_DATE=datetime.strptime(REQUEST_DATE,'%Y-%m-%d')
    else:
        REQUEST_DATE=date.today()
        REQUEST_DATE=datetime(REQUEST_DATE.year,REQUEST_DATE.month,REQUEST_DATE.day)
    print(REQUEST_DATE)

    api_key=settings.KOREAEXIM_KEY
    url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={api_key}&data=AP01'
    exchange_date, created = ExchangeDate.objects.get_or_create(date_info=time_formmating(REQUEST_DATE,type="from_db"))
    print('조회날짜',exchange_date.date_info)
    if created: #오늘날짜가 조회된 적 없을경우
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                if not data: #요청시간이 지났을 경우, 503상태 반환
                    exchange_date.delete()
                    #영업시간이 아니므로, 가장 최근데이터 보내기
                    print('영업시간 아님')
                    latest_exchange_date=ExchangeDate.objects.latest('date_info')
                    exchange_info_list = ExchangeInfo.objects.filter(exchangeDate=latest_exchange_date)
                    data = ExchangeInfoSerializer(exchange_info_list, many=True)
                    if not data:
                        data={'nodata'}
                    return Response({'message': '영업시간이 아닙니다','data':data.data,'datetime':'latest'})
                for item in data:
                    item.pop('result',None)
                    form = ExchangeInfoForm(data=item)
                    if form.is_valid():
                        exchange_info = form.save(commit=False)
                        exchange_info.exchangeDate = exchange_date
                        exchange_info.save()
                        print('저장됨',item['cur_nm'])
                    else:
                        print('저장안됨')
                return Response({'data':data,'datetime':REQUEST_DATE})
            else:
                return Response({'error': 'API request failed'}, status=500)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    exchange_info = ExchangeInfo.objects.filter(exchangeDate=exchange_date)
    serializer = ExchangeInfoSerializer(exchange_info, many=True)
    print('이미 데이터 존재')
    return Response({'data':serializer.data,'datetime':REQUEST_DATE})


@api_view(["GET"])
def api_test(request):
    URL = BASE_URL+DEPOSIT_API_URL
    params = {
        'auth':settings.FSS_KEY,
        'topFinGrpNo':'020000',
        'pageNo':1
    }
    res_data = requests.get(URL,params=params).json()['result']
    print(res_data)
    return Response({'data':res_data})



@api_view(["GET"])
def save_deposit_products(request):
    print('저장되있음')
    URL = BASE_URL+DEPOSIT_API_URL
    product_result=[]
    option_result=[]
    products=DepositProduct.objects.all()
    if not products:
        for FinGrpNo in ['020000','030200','030300','050000','060000']: 
            page_no=1
            print('now',page_no,FinGrpNo)
            while True:
                params = {
                    'auth':settings.FSS_KEY,
                    'topFinGrpNo':FinGrpNo,
                    'pageNo':page_no
                }
                data,max_page_no,total_count,err_cd,option_data=finance_data_divider(URL,params)
                if total_count==0 or err_cd!='000': # 데이터없으면 나가기
                    break
                product_result.extend(data)
                option_result.extend(option_data)
                if page_no>=max_page_no:
                    break
                page_no+=1
        filtered_data=finance_data_handler(product_result,option_result)
        returned_data=[]
        for item_code in filtered_data:
            returned_data.append(filtered_data[item_code])
            product,created=DepositProduct.objects.get_or_create(code=item_code)
            if created:
                #print('생성',item_code)
                product.delete()
                product_serializer=DepositProductSerializer(data=filtered_data[item_code]['product'])
                if product_serializer.is_valid(raise_exception=True):
                    product=product_serializer.save()
                for option in filtered_data[item_code]['option']:
                    option_serializer=DepositOptionSerializer(data=option)
                    if option_serializer.is_valid(raise_exception=True):
                        option_serializer.save(product=product)
            else:
                print('aleady')
                pass
    products=DepositProduct.objects.all()
    returned_data = []
    for item in products:
        product_serializer = DepositProductSerializer(item)
        options = DepositOption.objects.filter(code=item.code)
        option_serializer = DepositOptionSerializer(options, many=True)
        returned_data.append({
            'product': product_serializer.data,
            'option': option_serializer.data
        })
    print('완료')
    return Response({'message': 'success', 'data': returned_data})


@api_view(["GET"])
def save_saving_products(request):
    URL = BASE_URL+SAVING_API_URL
    product_result=[]
    option_result=[]
    products=SavingProduct.objects.all()
    print('있나?',len(products))
    if not products:
        for FinGrpNo in ['020000','030200','030300','050000','060000']: 
            page_no=1
            #print('now',page_no,FinGrpNo)
            while True:
                params = {
                    'auth':settings.FSS_KEY,
                    'topFinGrpNo':FinGrpNo,
                    'pageNo':page_no
                }
                data,max_page_no,total_count,err_cd,option_data=finance_data_divider(URL,params)
                if total_count==0 or err_cd!='000': # 데이터없으면 나가기
                    break
                product_result.extend(data)
                option_result.extend(option_data)
                if page_no>=max_page_no:
                    break
                page_no+=1
        filtered_data=finance_data_handler(product_result,option_result)
        returned_data=[]
        for item_code in filtered_data:
            returned_data.append(filtered_data[item_code])
            product,created=SavingProduct.objects.get_or_create(code=item_code)
            if created:
                #print('생성',item_code)
                product.delete()
                product_serializer=SavingProductSerializer(data=filtered_data[item_code]['product'])
                if product_serializer.is_valid(raise_exception=True):
                    product=product_serializer.save()
                for option in filtered_data[item_code]['option']:
                    option_serializer=SavingOptionSerializer(data=option)
                    if option_serializer.is_valid(raise_exception=True):
                        option_serializer.save(product=product)
            else:
                print('aleady')
                pass
    products=SavingProduct.objects.all()
    returned_data = []
    for item in products:
        product_serializer = SavingProductSerializer(item)
        options = SavingOption.objects.filter(code=item.code)
        option_serializer = SavingOptionSerializer(options, many=True)
        returned_data.append({
            'product': product_serializer.data,
            'option': option_serializer.data
        })
    print('완료')
    return Response({'message': 'success', 'data': returned_data})


@api_view(["POST"])
def join_deposit_product(request):
    # 요청에서 'code'를 받아 해당 상품 조회
    code = request.data['code']
    try:
        product = DepositProduct.objects.get(code=code)
    except DepositProduct.DoesNotExist:
        return Response({'message': 'error','data':'상품을 찾을 수 없습니다.'}, status=404)
    print(product.join_user.all(),request.user)
    user = request.user
    if user in product.join_user.all():
        # 사용자가 이미 join_user 목록에 있다면 제거
        product.join_user.remove(user)
        message = '구독취소 완료'
        print('delete_ok')
    else:
        # 그렇지 않다면 추가
        product.join_user.add(user)
        message = '구독 완료'
        print('add_ok')
    print(message,DepositProductSerializer(product).data)
    return Response({'message': message,'data':DepositProductSerializer(product).data})

@api_view(["POST"])
def join_saving_product(request):
    # 요청에서 'code'를 받아 해당 상품 조회
    code = request.data['code']
    try:
        product = SavingProduct.objects.get(code=code)
    except SavingProduct.DoesNotExist:
        return Response({'message': '상품을 찾을 수 없습니다.'}, status=404)
    print(product.join_user.all(),request.user)
    user = request.user
    if user in product.join_user.all():
        # 사용자가 이미 join_user 목록에 있다면 제거
        product.join_user.remove(user)
        message = '구독취소 완료'
        print('delete_ok')
    else:
        # 그렇지 않다면 추가
        product.join_user.add(user)
        message = '구독 완료'
        print('add_ok')
    return Response({'message': message,'data':SavingProductSerializer(product).data})



@api_view(['GET'])
def news(request):
    encText = urllib.parse.quote('금융')
    URL = 'https://openapi.naver.com/v1/search/news.json?query=' + encText+"&sim"
    request = urllib.request.Request(URL)
    request.add_header("X-Naver-Client-Id",settings.NAVER_CLIENT_ID)
    request.add_header("X-Naver-Client-Secret",settings.NAVER_CLIENT_SECRET)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        return Response(json.loads(response_body.decode('utf-8')), status=status.HTTP_200_OK)
    else:
        return Response({"message": "조회에 실패했습니다."}, status=status.HTTP_404_NOT_FOUND)
    
@api_view(['GET'])
def golds(request):
# 오늘 날짜를 년-월-일 형식으로 가져오기
    today = datetime.now().strftime("%Y-%m-%d")
    two_months_ago = (datetime.now() - timedelta(days=60)).strftime("%Y-%m-%d")
    quandl.ApiConfig.api_key=settings.NASDAQ_KEY
    df=quandl.get(dataset='LBMA/GOLD',start_date=two_months_ago,end_date=today)
    df.reset_index(inplace=True)
    json_data = df.to_json(orient='records')
    return Response({'message': 'success', 'data': json_data})

@api_view(['GET'])
def silvers(request):
# 오늘 날짜를 년-월-일 형식으로 가져오기
    today = datetime.now().strftime("%Y-%m-%d")
    two_months_ago = (datetime.now() - timedelta(days=360)).strftime("%Y-%m-%d")
    quandl.ApiConfig.api_key=settings.NASDAQ_KEY
    df=quandl.get(dataset='LBMA/SILVER',start_date=two_months_ago,end_date=today)
    df.reset_index(inplace=True)
    json_data = df.to_json(orient='records')
    return Response({'message': 'success', 'data': json_data})


@api_view(['GET'])
def recommend(request,user_id):
    print(user_id)
    req_user=CustomUser.objects.get(id=user_id)
    serializer = CustomUserDetailSerializer(req_user)
    serializer.data.get('age')
    print(serializer.data.get('age'),serializer.data.get('capital'),serializer.data.get('salary'))
# 오늘 날짜를 년-월-일 형식으로 가져오기
    params = {
        'auth':"30d0aa193f68302232f7c844e67d4f21",
        'topFinGrpNo':'020000',
        'pageNo':1
    }
    URL = BASE_URL+DEPOSIT_API_URL
    res_data=requests.get(URL,params=params).json()['result']
    data=res_data['baseList']
    filtered_item={str(i):data[i-1]['fin_co_no']+'_'+data[i-1]['fin_prdt_cd'] for i in range(1,len(data)+1)}

    NUM_USERS=20000
    NUM_ITEMS=len(filtered_item)
    SALARY_LIST=[i*500000 for i in range(21)]
    CAPITAL_LIST=[i*10000000 for i in range(100)]

    np.random.seed(0)
    user_salary=[SALARY_LIST[int(random.random()*21)] for i in range(NUM_USERS)]
    user_capital=[CAPITAL_LIST[int(random.random()*100)] for i in range(NUM_USERS)]
    user_age=[20+int(random.random()*50) for i in range(NUM_USERS)]
    target=[1+int(random.random()*NUM_ITEMS) for i in range(NUM_USERS)]
    data = pd.DataFrame({"user_id":[i for i in range(1,NUM_USERS+1)],
        "salary":user_salary,
        "capital":user_capital,
        "age":user_age,
        "target":target
        })

    for item in range(1, NUM_ITEMS + 1):
        data[f'{item}'] = (data['target'] == item).astype(int)
    data = data.drop('target', axis=1)
    df = pd.DataFrame(data)
    df = df.set_index('user_id')

    # 코사인 유사도 계산
    user_features = data[['age', 'capital', 'salary']]

    rounded_salary = min(SALARY_LIST, key=lambda x: abs(x - serializer.data.get('salary')))
    rounded_capital = min(CAPITAL_LIST, key=lambda x: abs(x - serializer.data.get('capital')))

    if serializer.data.get('salary') >= SALARY_LIST[-1]:
        rounded_salary = SALARY_LIST[-1]
    if serializer.data.get('capital') >= CAPITAL_LIST[-1]:
        rounded_capital = CAPITAL_LIST[-1]
    new_user_data={'age':serializer.data.get('age'),'capital':rounded_capital,'salary':rounded_salary}
    num_recommendations= 3 #추천할 종목 수

    new_user_features = pd.DataFrame([new_user_data], columns=['age', 'capital', 'salary'])
    print('co',user_features,new_user_features)

    # 기존 사용자 데이터와의 유사도 계산
    new_user_similarities = cosine_similarity(user_features, new_user_features)
    # 유사도가 높은 사용자들 찾기
    similar_users = pd.Series(new_user_similarities.flatten()).sort_values(ascending=False)
    # 추천할 종목 리스트
    recommended_items = []
    for similar_user_index in similar_users.index:
        # 유사한 사용자의 종목 데이터
        similar_user_subscriptions = data.iloc[similar_user_index, 3:]
        # 새로운 종목 추천
        new_recommendations = similar_user_subscriptions.index[
            similar_user_subscriptions == 1
        ]
        for item in new_recommendations:
            if item not in recommended_items:
                recommended_items.append(item)

        if len(recommended_items) >= num_recommendations:
            break

    tt=[]
    result=[filtered_item[i] for i in recommended_items[:num_recommendations]]
    for i in recommended_items[:num_recommendations]:
        tmp=DepositProduct.objects.get(code=filtered_item[i])
        tt.append(tmp.kor_co_nm+'-'+tmp.fin_prdt_nm)
    print('done',tt)
    return Response({'message':'success','data':tt})
