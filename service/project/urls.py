from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from services.models import Subscription
from services.views import SubscriptionView

router = routers.DefaultRouter()
router.register(r'api/subscriptions', viewset=SubscriptionView, basename='subs')

urlpatterns = [
  path('admin/', admin.site.urls),
  path('', include(router.urls)),
  path('api-auth', include('rest_framework.urls')),
]
