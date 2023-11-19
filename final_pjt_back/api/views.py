from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
import requests
from datetime import datetime,date
from pytz import timezone
from .models import ExchangeDate,ExchangeInfo,DepositProducts,DepositOptions
from .serializers import ExchangeDateSerializer,ExchangeInfoSerializer,DepositOptionsserializer,DepositProductsSerializer
from .forms import ExchangeInfoForm

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

def finance_data_handling(URL,params):
    #data,max_page_no,total_count,err_cd=finance_data_handling(URL,params)
    res_data=requests.get(URL,params=params).json()['result']
    data=res_data['baseList']
    max_page_no=res_data['max_page_no']
    total_count=res_data['total_count']
    err_cd=res_data['err_cd']
    return data,max_page_no,total_count,err_cd

@api_view(['GET'])
def exchange(request):
    '''
    [
        {
        "result": 1, 조회결과 1:성공, 2:오류, 3: 인증코드오류
        "cur_unit": "AED", 통화코드
        "ttb": "356.51", 송금받을때
        "tts": "363.72", 송금보낼때
        "deal_bas_r": "360.12", 매매기준율
        "bkpr": "360", 장부가격
        "yy_efee_r": "0",
        "ten_dd_efee_r": "0",
        "kftc_bkpr": "360",
        "kftc_deal_bas_r": "360.12",
        "cur_nm": "아랍에미리트 디르함" 나라이름
    },
    ...
    ]
    '''
    api_key=settings.KOREAEXIM_KEY
    # Construct the URL with the API key and date
    url = f'https://www.koreaexim.go.kr/site/program/financial/exchangeJSON?authkey={api_key}&data=AP01'
    print(api_key)
    exchange_date, created = ExchangeDate.objects.get_or_create(date_info=time_formmating(type="from_db"))
    if created: #오늘날짜가 조회된 적 없을경우
        try:
            response = requests.get(url)
            print(response.json())
            if response.status_code == 200:
                data = response.json()
                if not data: #요청시간이 지났을 경우, 503상태 반환
                    print('노노')
                    exchange_date.delete()
                    return Response({'message': '영업시간이 아닙니다'}, status=503)
                print('?')
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
                return Response(data)
            else:
                return Response({'error': 'API request failed'}, status=500)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
    exchange_info = ExchangeInfo.objects.filter(exchangeDate=exchange_date)
    serializer = ExchangeInfoSerializer(exchange_info, many=True)
    print('???')
    return Response(serializer.data)

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
        'pageNo':5
    }
    res_data = requests.get(URL,params=params).json()['result']
    print(res_data)
    return Response({'data':'good'})

@api_view(["GET"])
def save_deposit_products(request):
    URL = BASE_URL+DEPOSIT_API_URL
    result=[]
    all_res_data=[]
    for FinGrpNo in ['020000','030200','030300','050000','060000']:
        page_no=1
        print('now',page_no,FinGrpNo)
        while True:
            params = {
                'auth':settings.FSS_KEY,
                'topFinGrpNo':FinGrpNo,
                'pageNo':page_no
            }
            data,max_page_no,total_count,err_cd=finance_data_handling(URL,params)
            if total_count==0 or err_cd!='000': # 데이터없으면 나가기
                break
            result.extend(data)
            #data, max_page_no,total_count = func
        #res_data = requests.get(URL,params=params).json()['result']
            print(data)
            print(total_count,FinGrpNo,page_no,max_page_no,len(data))
            if page_no>=max_page_no:
                break
            page_no+=1
        print('next_bank')
    print('총 결과',len(result))
        #return Response(res_data)
    return Response({'message':'good','data':result})

@api_view(["GET"])
def save_saving_products(request):
    URL = BASE_URL+SAVING_API_URL
    result=[]
    all_res_data=[]
    for FinGrpNo in ['020000','030200','030300','050000','060000']:
        page_no=1
        print('now',page_no,FinGrpNo)
        while True:
            params = {
                'auth':settings.FSS_KEY,
                'topFinGrpNo':FinGrpNo,
                'pageNo':page_no
            }
            data,max_page_no,total_count,err_cd=finance_data_handling(URL,params)
            if total_count==0 or err_cd!='000': # 데이터없으면 나가기
                break
            result.extend(data)
            #data, max_page_no,total_count = func
        #res_data = requests.get(URL,params=params).json()['result']
        
            print(total_count,FinGrpNo,page_no,max_page_no,len(data))
            if page_no>=max_page_no:
                break
            page_no+=1
        print('next_bank')
    print('총 결과',len(result))
        #return Response(res_data)
    return Response({'message':'good','data':result})
'''
        baseList=res_data['baseList']
        optionList=res_data['optionList']
        for data in baseList:
            serial= DepositProductsSerializer(data=data)
            if serial.is_valid():
                serial.save()
                result.append({'data': data, 'status': 'Success', 'result': serial.data})
            else:
                result.append({'data': data, 'status': 'Error', 'result': serial.data})
        for data in optionList:
            try:
                Depositproduct=DepositProducts.objects.get(fin_prdt_cd=data['fin_prdt_cd'])
            except:
                result.append({'data': data, 'status': 'Error', 'result': 'No data'})
                print(data)
            serial = DepositOptionsserializer(data=data)
            if serial.is_valid(raise_exception=True):
                serial.save(product=Depositproduct)
                result.append({'data': data, 'status': 'Success', 'result': serial.data})
            else:
                result.append({'data': data, 'status': 'Error', 'result': serial.data})

    return Response(result, status=201)
'''
# 전체 정기예금 상품 목록 출력
# 정기예금 상품 추가하기
@api_view(["GET", "POST"])
def deposit_products(request):
    if request.method == "GET":
        data = DepositProducts.objects.all()
        serializer = DepositProductsSerializer(data, many=True)
        return Response(serializer.data)
    else:
        result=[]
        data=request.data['data']
        serial= DepositProductsSerializer(data=data)
        if serial.is_valid():
            serial.save()
            return Response({'data': data, 'status': 'Success', 'result': serial.data}, status=201)
        else:
            return Response({'data': data, 'status': 'Error', 'result': serial.data}, status=400)

# 특정 상품의 옵션 리스트 출력
@api_view(["GET"])
def deposit_product_options(request,fin_prdt_cd):
    try:
        data = DepositProducts.objects.get(fin_prdt_cd=fin_prdt_cd)
        options=DepositOptions.objects.filter(product=data)
        serial=DepositOptionsserializer(data=options,many=True)
        serial.is_valid()
        return Response(serial.data, status=201)
    except:
        return Response({'error': 'Product not found'}, status=404)

# 금리가 가장 높은 상품의 정보 출력
@api_view(["GET"])
def top_rate(request):
    datas=DepositOptions.objects.all()
    max_g=[-10,'']
    for data in datas:
        if data.intr_rate2>max_g[0]:
            max_g=[data.intr_rate2,data.fin_prdt_cd]
    print('@@@',max_g)
    # 최고 금리를 가진 상품의 정보 가져오기
    try:
        Depositproduct = DepositProducts.objects.get(fin_prdt_cd=max_g[1])
    except DepositProducts.DoesNotExist:
        return JsonResponse({'error': 'Product not found'}, status=404)
    
    # 해당 상품 정보를 시리얼라이즈
    data = DepositProductsSerializer(Depositproduct)
    
    # 시리얼라이즈된 데이터를 JSON 응답으로 반환
    return Response(data.data, status=200)
