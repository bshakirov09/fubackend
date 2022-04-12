from django.db import models

from fitness.core.models import BaseModel, SingletonModel


class Terms(SingletonModel, BaseModel):
    description = models.TextField()


class Guidelines(SingletonModel, BaseModel):
    description = models.TextField()


class PrivacyPolicy(SingletonModel, BaseModel):
    description = models.TextField()


class FAQ(SingletonModel, BaseModel):
    description = models.TextField()


class ContactUs(SingletonModel, BaseModel):
    description = models.TextField()
