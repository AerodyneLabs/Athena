from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers
from rest_framework_swagger.views import get_swagger_view

from airspace import views as airspace_views

router = routers.DefaultRouter()
router.register(r'airspaces', airspace_views.AirspaceViewset)
router.register(r'airspaceBoundaries', airspace_views.AirspaceVolumeViewset)
router.register(r'centers', airspace_views.CenterViewset)
router.register(r'navaids', airspace_views.NavaidViewset)
router.register(r'towers', airspace_views.TowerViewset)

schema_view = get_swagger_view(title='Athena API')

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^docs/', schema_view),
]
