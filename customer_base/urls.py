from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from rest_framework import routers
from rest_framework.authtoken import views #for obtain_auth_token setup

from core.views import (
    CustomerViewSet,
    ProfessionViewSet,
    DataSheetViewSet,
    DocumentViewSet
)#getting the views here


router = routers.DefaultRouter()

router.register(r'customers',CustomerViewSet,basename = "customers")
router.register(r'professions',ProfessionViewSet)
router.register(r'data-sheet',DataSheetViewSet)
router.register(r'documents',DocumentViewSet)
#this is for Urls register the ViewSet


urlpatterns = [
    path('api/', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth', include('rest_framework.urls')),
    path('api-token-auth/',  views.obtain_auth_token) #for obtain_auth_token setup


]
