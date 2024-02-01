from stock.models import AtrResult
from django.db.models import Sum, Max, Min, Avg, Count


def get_buy_info():
    queryset = AtrResult.objects.filter(comment=5,ticker__market="KOSDAQ").values('price_buy__date').annotate(
        total_count=Count('price_buy__date'),
        profit_sum=Sum('profit'),
        max_profit=Max('profit'),
        min_profit=Min('profit'),
        avg_profit=Avg('profit')
    ).order_by('price_buy__date')

    a=1
    for item in queryset:
        a= a*(100+item['avg_profit']-0.1)/100
    print(a)
