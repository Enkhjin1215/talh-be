from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from myapp.views import LotteryViewSet


router = routers.DefaultRouter()
router.register(r'lotteries', LotteryViewSet, basename='lottery')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),

]
