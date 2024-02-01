from django.db import models


# Create your models here.

class Ticker(models.Model):
    code = models.CharField(primary_key=True, max_length=10)
    name = models.CharField(max_length=30)
    market = models.CharField(max_length=10)
    listing = models.BooleanField(default=True)
    shares = models.FloatField(default=0)


class Price(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    open = models.IntegerField()  # 시가
    high = models.IntegerField()  # 고가
    low = models.IntegerField()  # 저가
    close = models.IntegerField()  # 종가
    volume = models.BigIntegerField()  # 거래량
    date = models.DateField()  # 일자 정보를 저장하기 위한 DateField
    is_finalized = models.BooleanField(default=True)  # 데이터가 finalized인지 여부를 나타내는 BooleanField

    def __str__(self):
        return f"{self.ticker} - {self.date}"

    class Meta:
        verbose_name_plural = "Price Data"

class AtrResult(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    price_buy = models.ForeignKey(Price, on_delete=models.CASCADE, related_name='atr_results_buy')
    price_sell = models.ForeignKey(Price, on_delete=models.CASCADE, related_name='atr_results_sell')
    buy_line = models.FloatField(default=0)
    comment = models.CharField(max_length=20,default='')
    profit = models.FloatField()


class Indicators(models.Model):
    name = models.CharField(max_length=30)


class IndicatorsValues(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    price = models.ForeignKey(Price, on_delete=models.CASCADE)  # 언제 데이터인지 (계산된 마지막 캔들)
    indicator = models.ForeignKey(Indicators, on_delete=models.CASCADE)
    score = models.FloatField()  # 수정된 데이터(점수로 치환된)
    value = models.FloatField()  # 원본 데이터


class IndicatorsRuleTable(models.Model):
    rule_name = models.CharField(max_length=30)
    goal_score = models.FloatField()


class IndicatorsRule(models.Model):
    indicator = models.ForeignKey(Indicators, on_delete=models.CASCADE)
    rule_table = models.ForeignKey(IndicatorsRuleTable, on_delete=models.CASCADE)
    score = models.FloatField()


class Result(models.Model):
    ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    price_indicator = models.ForeignKey(Price, on_delete=models.CASCADE, related_name='buy_indicator')
    price_buy = models.ForeignKey(Price, on_delete=models.CASCADE, related_name='buy_price')
    price_sell = models.ForeignKey(Price, on_delete=models.CASCADE, related_name='sell_price')
    indicator_rule_table = models.ForeignKey(IndicatorsRuleTable, on_delete=models.CASCADE)
    profit = models.FloatField()
