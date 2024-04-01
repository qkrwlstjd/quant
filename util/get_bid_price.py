def get_below_bid_price(current_price):
    # 호가 단위에 따른 현재가 범위 설정
    if 1000 <= current_price <= 2000:
        bid_unit = 1
    elif 2000 < current_price <= 5000:
        bid_unit = 5
    elif 5000 < current_price <= 10000:
        bid_unit = 10
    elif 10000 < current_price <= 20000:
        bid_unit = 10
    elif 20000 < current_price <= 50000:
        bid_unit = 50
    elif 50000 < current_price <= 100000:
        bid_unit = 100
    elif 100000 < current_price <= 200000:
        bid_unit = 100
    elif 200000 < current_price <= 500000:
        bid_unit = 500
    else:  # 500000원 이상
        bid_unit = 1000

    # 현재가가 호가 단위의 배수인 경우를 고려하여 바로 아래 호가 계산
    if current_price % bid_unit == 0:
        below_bid_price = current_price - bid_unit
    else:
        below_bid_price = (current_price // bid_unit) * bid_unit - bid_unit

    return below_bid_price


def get_next_bid_price(current_price):
    # 호가 단위에 따른 현재가 범위 설정
    if 1000 <= current_price < 2000:
        bid_unit = 1
    elif 2000 <= current_price < 5000:
        bid_unit = 5
    elif 5000 <= current_price < 10000:
        bid_unit = 10
    elif 10000 <= current_price < 20000:
        bid_unit = 10
    elif 20000 <= current_price < 50000:
        bid_unit = 50
    elif 50000 <= current_price < 100000:
        bid_unit = 100
    elif 100000 <= current_price < 200000:
        bid_unit = 100
    elif 200000 <= current_price < 500000:
        bid_unit = 500
    else:  # 500000원 이상
        bid_unit = 1000

    # 현재가에 호가 단위를 더해서 다음 호가를 계산
    next_bid_price = current_price + bid_unit
    return next_bid_price
