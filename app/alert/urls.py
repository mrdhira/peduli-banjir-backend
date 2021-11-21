from django.urls import path
from .views import AlertByLatlongView, AlertByLatlongCityDistrictGroup

app_name = "alert"
urlpatterns = [
    path(
        "alert-by-latlong", view=AlertByLatlongView.as_view(), name="alert_by_latlong"
    ),
    path(
        "alert-by-latlong-city-district-group",
        view=AlertByLatlongCityDistrictGroup.as_view(),
        name="alert_by_latlong_city_district_group",
    ),
    # path("alert-by-latlong-city-district-group"),
]
