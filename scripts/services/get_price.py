from stock.models import Price


def get_price(code):
    price_list = Price.objects.filter(ticker__code=code, is_finalized=True).order_by('date').values()

    # 결과 반환
    return price_list


def get_price_list(code,recent=False,date=None):
    if date:
        return list((Price.objects.filter(ticker__code=code, is_finalized=True,date__lte=date)
                     .order_by('-date'))[:61].values())[::-1]
    if recent:
        return list((Price.objects.filter(ticker__code=code, is_finalized=True)
                     .order_by('-date'))[:61].values())[::-1]
    else:
        return list(Price.objects.filter(ticker__code=code, is_finalized=True).order_by('date').values())