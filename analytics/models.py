from stock.models import Ticker, Price
from django.db import models


class Indicators(models.Model):
    name = models.CharField(max_length=30)


class IndicatorsValues(models.Model):
    stock_ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    stock_price = models.ForeignKey(Price, on_delete=models.CASCADE)  # 언제 데이터인지 (계산된 마지막 캔들)
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
    stock_ticker = models.ForeignKey(Ticker, on_delete=models.CASCADE)
    stock_price_indicator = models.ForeignKey(Price, on_delete=models.CASCADE, related_name='buy_indicator')
    stock_price_buy = models.ForeignKey(Price, on_delete=models.CASCADE, related_name='buy_price')
    stock_price_sell = models.ForeignKey(Price, on_delete=models.CASCADE, related_name='sell_price')
    indicator_rule_table = models.ForeignKey(IndicatorsRuleTable, on_delete=models.CASCADE)
    profit = models.FloatField()
