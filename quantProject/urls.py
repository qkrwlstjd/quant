from django.contrib import admin
from django.urls import include, path

from django.urls import path, re_path
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


schema_view = get_schema_view(
   openapi.Info(
      title="Your API Title",
      default_version='v1',
      description="API description",
      # ...
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', SpectacularSwaggerView.as_view(url_name='zzzzzz'), name='swagger-ui'),
    # path('stock/', include('stock.urls')),  # 'myapp'는 앱 이름입니다.
    path('admin/', admin.site.urls),
    path('zzzzzz/', SpectacularAPIView.as_view(), name='zzzzzz'),
]
