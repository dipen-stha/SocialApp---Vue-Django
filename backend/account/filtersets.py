from django.db.models import Count

from django_filters import rest_framework as filters

from .models import User

USER_TYPE_CHOICES = [('recommendations', 'Recommendations')]