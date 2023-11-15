from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.conf import settings
import requests
from datetime import datetime,date
from pytz import timezone
from .models import ExchangeDate,ExchangeInfo
from .serializers import ExchangeDateSerializer,ExchangeInfoSerializer
from .forms import ExchangeInfoForm
def time_formmating(now="",type="to_db"):
    if not now:
        now=datetime.now()
    print('now :',now)
    kr_timezone = timezone('Asia/Seoul')
    now_kr = now.astimezone(kr_timezone)
    formatted_date = now_kr.strftime('%Y%m%d') if type=="to_db" else now_kr.strftime('%Y-%m-%d')
    return formatted_date

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
                    latest_exchange_date=ExchangeDate.objects.latest('date_info')
                    exchange_info_list = ExchangeInfo.objects.filter(exchangeDate=latest_exchange_date)
                    data = ExchangeInfoSerializer(exchange_info_list, many=True)
                    #print('@@@@@@@@@@@@@@@@',data.data)
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