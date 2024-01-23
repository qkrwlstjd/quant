from django.urls import path, include
from analytics.view import PriceListView  # PriceListView가 있는 위치에 따라 import 경로를 조절해야 합니다.

urlpatterns = [
    # 다른 URL 패턴들 ...
    path('price/', PriceListView.as_view(), name='price-list'),
]
