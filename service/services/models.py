from collections.abc import Iterable
from django.db import models
from django.core.validators import MaxValueValidator
from clients.models import Client
from services.tasks import set_comment, set_price


class Service(models.Model):
  name = models.CharField(max_length=64)
  full_price = models.PositiveIntegerField()

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.__full_price = self.full_price

  def save(self, *args, **kwargs):
    if self.full_price != self.__full_price:
      self.__full_price = self.full_price
      for subscription in self.subscriptions.all():
        set_price.delay(subscription.id)
        set_comment.delay(subscription.id)
    return super().save(*args, **kwargs)

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

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.__discount_percent = self.discount_percent

  def save(self, *args, **kwargs):
    if self.discount_percent != self.__discount_percent:
      self.__discount_percent = self.discount_percent
      for subscription in self.subscriptions.all():
        set_price.delay(subscription.id)
        set_comment.delay(subscription.id)
    return super().save(*args, **kwargs)

  def __str__(self):
    return f"{self.plan_type.upper()}: {self.discount_percent}%."


class Subscription(models.Model):
  client = models.ForeignKey(Client, on_delete=models.PROTECT, related_name='subscriptions')
  service = models.ForeignKey(Service, on_delete=models.PROTECT, related_name='subscriptions')
  plan = models.ForeignKey(Plan, on_delete=models.PROTECT, related_name='subscriptions')
  price = models.PositiveIntegerField(default=0)
  comment = models.CharField(max_length=255, default='')

  # def save(self, *args, save_model=True, **kwargs):
  #   if save_model:
  #     set_price.delay(self.id)
  #   return super().save(*args, **kwargs)

  def __str__(self):
    return f"Client: {self.client.user.username}, Service: {self.service.name}, Plan: “{self.plan}”, Finally Prise: {(self.service.full_price * self.plan.discount_percent / 100)}"
