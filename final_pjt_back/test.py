import requests
import pandas as pd
import numpy as np
from pprint import pprint
BASE_URL = 'http://finlife.fss.or.kr/'
DEPOSIT_API_URL = 'finlifeapi/depositProductsSearch.json'
SAVING_API_URL = 'finlifeapi/savingProductsSearch.json'

URL = BASE_URL+SAVING_API_URL
product_result=[]
option_result=[]

def finance_data_divider(URL,params):
    res_data=requests.get(URL,params=params).json()['result']
    data=res_data['baseList']
    tmp={i:data[i-1]['fin_co_no']+'_'+data[i-1]['fin_prdt_cd'] for i in range(1,len(data)+1)}
    return tmp,data

params = {
    'auth':"30d0aa193f68302232f7c844e67d4f21",
    'topFinGrpNo':'020000',
    'pageNo':1
}
filtered_data,data=finance_data_divider(URL,params)
#print(filtered_data)
print(len(filtered_data),len(data))

# 랜덤 데이터 생성 (0~5 사이의 정수)
NUM_USERS=100
NUM_ITEMS=len(data)
np.random.seed(0)
point_data = np.random.randint(0, 6, size=(NUM_USERS, NUM_ITEMS))

# 'user_id', 'item_id', 'point' 형식의 DataFrame 생성
df_long = pd.DataFrame({
    'user_id': np.repeat(range(1, NUM_USERS + 1), NUM_ITEMS),
    'item_id': np.tile(range(1, NUM_ITEMS + 1), NUM_USERS),
    'point': point_data.ravel()
})

print(df_long.head(62))  # 처음 몇 줄만 출력하여 확인

'''
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

'''