# news/tasks.py
from celery import shared_task
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from  news_scraper.news_scraper.spiders.news_spiders import ZoomitArchiveSpider


@shared_task
def run_spider():
    # تنظیمات Scrapy را بارگیری کنید
    settings = get_project_settings()

    # تنظیمات سفارشی برای اجرا در Celery
    settings.set('LOG_ENABLED', False)  # غیرفعال کردن لاگ Scrapy (اختیاری)

    process = CrawlerProcess(settings)
    process.crawl(ZoomitArchiveSpider)
    process.start()