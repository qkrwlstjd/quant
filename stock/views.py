from rest_framework import views
from drf_spectacular.utils import extend_schema, OpenApiParameter
from stock.cron.finalized_price_cron_job import PriceFinalizationCronJob
from stock.cron.unfinalized_price_cron_job import PriceUnfinalizationCronJob
from rest_framework.response import Response


class CronPriceView(views.APIView):
    authentication_classes = []
    permission_classes = []

    @extend_schema(
        parameters=[
            OpenApiParameter(name='isfinalized', type=bool, location=OpenApiParameter.QUERY, description='isfinalized'),

        ],
    )
    def get(self, request, *args, **kwargs):
        isfinalized = self.request.query_params.get('isfinalized')
        if isfinalized=='true':
            PriceFinalizationCronJob().do()
        else:
            PriceUnfinalizationCronJob().do()
        return Response({"status": "success", "message": "Prices have been finalized."})
