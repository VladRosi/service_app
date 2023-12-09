from django.db import models
from django.core.validators import MaxValueValidator
from clients.models import Client


class Service(models.Model):
  name = models.CharField(max_length=64)
  full_price = models.PositiveIntegerField()

  def __str__(self):
    return f"{self.name}: {self.full_price}."


class Plan(models.Model):
  PLAN_TYPES = (
    ('full', 'FULL'),
    ('student', 'STUDENT'),
    ('discount', 'DISCOUNT'),
    ('family', 'FAMILY'),
  )
  plan_type = models.CharField(choices=PLAN_TYPES, max_length=15)
  discount_percent = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])

  def __str__(self):
    return f"{self.plan_type.upper()}: {self.discount_percent}%."


class Subscription(models.Model):
  client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='subscriptions')
  service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='subscriptions')
  plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')

  def __str__(self):
    return f"Client: {self.client.user.username}, Service: {self.service.name}, Plan: “{self.plan}”, Finally Prise: {(self.service.full_price * self.plan.discount_percent / 100)}"
