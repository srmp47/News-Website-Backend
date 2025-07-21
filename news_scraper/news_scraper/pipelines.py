# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from news.models import News,Tag
class NewsScraperPipeline:
    def process_item(self, item, spider):
        if News.objects.filter(title=item['title']).exists():
            return item

        news_item = News.objects.create(
            title=item['title'],
            content=item['content'],
            source=item['source']
        )

        for tag_name in item['tags']:
            tag, created = Tag.objects.get_or_create(tag_string=tag_name)
            news_item.tags.add(tag)

        return item
