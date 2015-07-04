from django.conf.urls import include, url
from django.contrib import admin
from rest_framework import routers

from airspace import views as airspace_views

router = routers.DefaultRouter()
router.register(r'centers', airspace_views.CenterViewset)
router.register(r'navaids', airspace_views.NavaidViewset)
router.register(r'towers', airspace_views.TowerViewset)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
]
