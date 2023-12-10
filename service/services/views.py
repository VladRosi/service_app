from django.conf import settings
from django.db.models import F, Prefetch, Sum
from django.shortcuts import render
from rest_framework.viewsets import ReadOnlyModelViewSet
from clients.models import Client
from services.models import Service, Subscription
from services.serializers import SubscriptionSerializer
from django.core.cache import cache


class SubscriptionView(ReadOnlyModelViewSet):
  # queryset = Subscription.objects.all().prefetch_related('client').prefetch_related('client__user')
  queryset = Subscription.objects.all().prefetch_related(
    'plan',
    Prefetch('client', queryset=Client.objects.all().select_related('user').only('company_name', 'user__email')),
    # Prefetch('service', queryset=Service.objects.all().only('full_price'))
  )  #.annotate(price=F('service__full_price') - \
  #(F('service__full_price') * (F('plan__discount_percent') / 100.00)))

  serializer_class = SubscriptionSerializer

  def list(self, request, *args, **kwargs):
    queryset = self.filter_queryset(self.get_queryset())
    response = super().list(self, request, *args, **kwargs)

    
    price_cache = cache.get(settings.PRICE_CACHE_NAME)

    if price_cache: 
      total_price = price_cache
    else:
      total_price = queryset.aggregate(total=Sum('price')).get('total')
      cache.set(settings.PRICE_CACHE_NAME, total_price, 3600)

    response_data = {'result': response.data}
    response_data['total_amount'] = total_price
    response.data = response_data
    return response
