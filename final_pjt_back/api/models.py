from django.db import models
from django.conf import settings

# Create your models here.
class ExchangeDate(models.Model):
    date_info = models.DateField() # 나중에 20230101이런식으로 변환 필요

class ExchangeInfo(models.Model):
    exchangeDate = models.ForeignKey(ExchangeDate, on_delete=models.CASCADE)
    cur_unit = models.TextField()
    ttb = models.TextField()
    tts = models.TextField()
    deal_bas_r = models.TextField()
    bkpr = models.TextField()
    yy_efee_r = models.TextField()
    ten_dd_efee_r = models.TextField()
    kftc_bkpr = models.TextField()
    kftc_deal_bas_r = models.TextField()
    cur_nm = models.TextField()

    def __str__(self):
        return self.cur_unit
    
'''
class DepositProduct(models.Model):
    fin_prdt_cd = models.TextField(unique=True)                                        #상품코드
    kor_co_nm = models.TextField()                                                     #금융회사명
    fin_prdt_nm = models.TextField()                                                   #금융상품명
    etc_note = models.TextField()                                                      #기타유의사항
    join_deny = models.IntegerField(null=True)                                         #가입제한
    join_member = models.TextField()                                                   #가입대상
    join_way =  models.TextField(null=True)                                            #가입경로
    spcl_cnd = models.TextField()                                                      #우대조건
    sub_user = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True, related_name='subscribed_deposit_products')  #구독
    join_user = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,  related_name='joined_deposit_products') #가입
    

class DepositOption(models.Model):
    product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE, related_name='option')# 저축 금리 유형명
    fin_prdt_cd = models.TextField()
    intr_rate_type_nm = models.TextField(max_length=100)# 저축 금리
    intr_rate = models.FloatField(default=-1,null=True,blank=True)# 최고 우대금리
    intr_rate2 = models.FloatField()# 저축 기간
    save_trm = models.FloatField()# 저축 금리 유형
    intr_rate_type = models.TextField()
'''
class DepositProduct(models.Model):
    code = models.TextField(unique=True)                                        #상품코드
    fin_prdt_cd = models.TextField()                                                   #은행이름
    kor_co_nm = models.TextField()                                                     #금융회사코드
    fin_prdt_nm = models.TextField()                                                   #금융상품명
    etc_note = models.TextField()                                                      #기타유의사항
    join_deny = models.IntegerField(null=True)                                         #가입제한
    join_member = models.TextField()                                                   #가입대상
    join_way =  models.TextField(null=True)                                            #가입경로
    spcl_cnd = models.TextField()                                                      #우대조건
    join_user = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,  related_name='joined_deposit_products') #가입
    

class DepositOption(models.Model):
    code = models.TextField()                                        #상품코드
    product = models.ForeignKey(DepositProduct, on_delete=models.CASCADE, related_name='option')# 저축 금리 유형명
    fin_prdt_cd = models.TextField()
    intr_rate_type_nm = models.TextField(max_length=100)# 저축 금리
    intr_rate = models.FloatField(default=-1,null=True,blank=True)# 최고 우대금리
    intr_rate2 = models.FloatField()# 저축 기간
    save_trm = models.FloatField()# 저축 금리 유형
    intr_rate_type = models.TextField()


class SavingProduct(models.Model):
    code = models.TextField(unique=True)      
    fin_prdt_cd = models.TextField()                                        #상품코드
    kor_co_nm = models.TextField()                                                     #금융회사명
    fin_prdt_nm = models.TextField()                                                   #금융상품명
    etc_note = models.TextField()                                                      #기타유의사항
    join_deny = models.IntegerField(null=True)                                         #가입제한
    join_member = models.TextField()                                                   #가입대상
    join_way =  models.TextField(null=True)                                            #가입경로
    spcl_cnd = models.TextField()                                                      #우대조건
    join_user = models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,  related_name='joined_saving_products') #가입
        
class SavingOption(models.Model):
    code = models.TextField()                                        #상품코드
    product = models.ForeignKey(SavingProduct, on_delete=models.CASCADE, related_name='option') # 저축 금리 유형명
    fin_prdt_cd = models.TextField()
    intr_rate_type_nm = models.TextField(max_length=100) # 저축 금리
    intr_rate = models.FloatField(default=-1,null=True,blank=True) # 최고 우대 금리
    intr_rate2 = models.FloatField(default=-1,null=True,blank=True) # 저축 기간 (단위 : 개월)
    save_trm = models.FloatField() # 적립 유형명
    rsrv_type_nm = models.TextField()

class Subscribe_Product(models.Model):
    user_id = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='subscribe_product')
    code = models.TextField()
    inir_rate_type=models.TextField()
