from django.contrib.sites import requests
from quizapp.models import Category
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'My scheduled job'

    def handle(self, *args, **options):
        try:
            Category.objects.create(name='cron')
            token = '6798739793:AAGZ8hFVcg-z4S5avYDFwo5doSRe0zqBNX8'
            url = f"https://api.telegram.org/bot{token}/sendMessage"
            data = {
                'chat_id': 6050173548,
                'text': "It is working"
            }
            requests.post(url, params=data)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error deleting user: {e}'))


