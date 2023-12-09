from rest_framework import serializers
from services.models import Plan, Subscription


class PlanSerializer(serializers.ModelSerializer):
  class Meta:
    model = Plan
    fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
  plan = PlanSerializer()

  client_name = serializers.CharField(source='client.company_name')
  email = serializers.CharField(source='client.user.email')
  price = serializers.SerializerMethodField()

  # whole_price = serializers.CharField(source='service.full_price')

  # whole_price = serializers.SerializerMethodField()

  # def get_price(self, instance):
  #   return instance.service.full_price - \
  #     instance.service.full_price * (instance.plan.discount_percent / 100)
  
  def get_price(self, instance):
    return instance.price

  # def get_whole_price(self, instance):
  #   return instance

  class Meta:
    model = Subscription
    fields = ['id', 'plan_id', 'client_name', 'email', 'plan', 'price']  # 'whole_price']
