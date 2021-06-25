from django.core.management.base import BaseCommand
from dashboard.choices import CATEGORY_TYPE_CHOICES, CATEGORY_CHOICE
from dashboard.models import CategoryType, Category


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for category in CATEGORY_CHOICE:
            for type in CATEGORY_TYPE_CHOICES:
                category_type = CategoryType.objects.get(type=type[0])
                Category.objects.get_or_create(
                    name=category[0], category_type=category_type)
        print('created')
