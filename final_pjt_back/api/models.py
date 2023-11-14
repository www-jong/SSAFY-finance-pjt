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