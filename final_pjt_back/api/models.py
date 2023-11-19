from django.db import models

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
    

# Create your models here.
class DepositProducts(models.Model):
    fin_prdt_cd = models.TextField(unique=True)
    kor_co_nm = models.TextField()
    fin_prdt_nm = models.TextField()
    etc_note = models.TextField(null=True,default="없음")
    join_deny = models.IntegerField()
    join_member = models.TextField(null=True,default="없음")
    join_way = models.TextField(null=True,default="없음")
    spcl_cnd = models.TextField(null=True,default="없음")

class DepositOptions(models.Model):
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE)
    fin_prdt_cd = models.TextField()
    intr_rate_type_nm = models.CharField(max_length=100)
    intr_rate = models.FloatField(null=True,default=-1)
    intr_rate2 = models.FloatField(null=True,default=-1)
    save_trm = models.IntegerField()
