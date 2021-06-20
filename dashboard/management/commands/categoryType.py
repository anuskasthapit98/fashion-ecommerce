from django.core.management.base import BaseCommand
from dashboard.choices import CATEGORY_TYPE_CHOICES
from dashboard.models import CategoryType


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for type in CATEGORY_TYPE_CHOICES:
            CategoryType.objects.create(type=type[0])
        print('created')
