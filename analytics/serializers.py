from rest_framework import serializers
from .models import Indicators

class MyModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicators
        fields = '__all__'  # 모든 필드를 포함시키거나, 필요한 필드만 명시할 수 있습니다.


