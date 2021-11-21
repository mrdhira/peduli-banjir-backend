from rest_framework import permissions
from rest_framework.views import APIView
from app.utils.http import generic_get
from .models import Alert
from .serializers import AlertSerializer, AlertByLatlongSerializer

# Create your views here.
class AlertByLatlongView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return generic_get(
            request=request,
            model_method=Alert.objects.get_alert_by_latlong,
            request_serializer=AlertByLatlongSerializer,
            response_serializer=AlertSerializer,
            protected=True,
        )


class AlertByLatlongCityDistrictGroup(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        return generic_get(
            request=request,
            model_method=Alert.objects.get_alert_by_latlong_city_district_group,
            request_serializer=AlertByLatlongSerializer,
            response_serializer=AlertSerializer,
            many=True,
            protected=True,
        )
