from django.db import models


# Create your models here.

class Ticker(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=30)
    market = models.CharField(max_length=10)
    listing = models.BooleanField(default=True)

class Price(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    open = models.IntegerField()  # 시가
    high = models.IntegerField()  # 고가
    low = models.IntegerField()   # 저가
    close = models.IntegerField()  # 종가
    volume = models.BigIntegerField()  # 거래량
    date = models.DateField() # 일자 정보를 저장하기 위한 DateField
    is_finalized = models.BooleanField(default=True)# 데이터가 finalized인지 여부를 나타내는 BooleanField

    def __str__(self):
        return f"{self.ticker} - {self.date}"

    class Meta:
        verbose_name_plural = "Price Data"
