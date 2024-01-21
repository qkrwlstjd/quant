from stock.serializers import PriceSerializer


def save_price_data(data, ticker,is_finalized=True):
    price_serializer = PriceSerializer(data=data, many=True, context={'ticker': ticker, 'is_finalized': is_finalized})
    if price_serializer.is_valid():
        price_serializer.save()
    else:
        print(price_serializer.errors)