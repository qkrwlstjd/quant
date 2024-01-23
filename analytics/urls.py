from django.urls import path, include
from rest_framework.routers import DefaultRouter
from analytics.view import IndicatorsViewSet

router = DefaultRouter()
router.register(r'indicator', IndicatorsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
