import os
import django
from news.tasks import run_spider

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsWebsiteBackend.settings')
django.setup()

if __name__ == '__main__':
    print("Starting spider task...")
    result = run_spider.delay()
    print(f"Task started! ID: {result.id}")