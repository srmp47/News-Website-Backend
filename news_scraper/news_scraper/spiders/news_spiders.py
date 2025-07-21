import scrapy
import json
from urllib.parse import urlencode
from scrapy_playwright.page import PageMethod


class ZoomitArchiveSpider(scrapy.Spider):
    name = 'zoomit_archive'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
        'DOWNLOAD_DELAY': 0.5,
        'CONCURRENT_REQUESTS_PER_DOMAIN': 4,
        'CONCURRENT_REQUESTS': 4,
        'FEEDS': {
            'zoomit_archive.json': {
                'format': 'json',
                'encoding': 'utf-8',
                'overwrite': True,
                'indent': 4
            }
        },
        'RETRY_TIMES': 3,
        'RETRY_HTTP_CODES': [500, 502, 503, 504, 400, 403, 404, 429],
        'HTTPCACHE_ENABLED': False,
        'HTTPCACHE_EXPIRATION_SECS': 86400,
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 1,
        'AUTOTHROTTLE_MAX_DELAY': 3,
        'DOWNLOAD_HANDLERS': {
            'http': 'scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler',
            'https': 'scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler',
        },
        'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor',
        'PLAYWRIGHT_BROWSER_TYPE': 'chromium',
        'PLAYWRIGHT_LAUNCH_OPTIONS': {'headless': True, 'timeout': 30000},
        'PLAYWRIGHT_CONTEXTS': {'default': {'java_script_enabled': True, 'ignore_https_errors': False, 'viewport': {'width': 1920, 'height': 1080}}}
    }

    API_URL = 'https://api2.zoomit.ir/editorial/api/articles/browse'
    WEB_URL = 'https://www.zoomit.ir/archive/?sort=Newest&publishDate=All&readingTime=All&pageNumber=1'
    ARTICLE_BASE_URL = 'https://www.zoomit.ir/'
    MAX_PAGES = 10
    MAX_ARTICLES = 50
    article_count = 0

    def start_requests(self):
        yield scrapy.Request(
            url=self.WEB_URL,
            callback=self.parse_web,
            meta={'playwright': True, 'playwright_include_page': True, 'playwright_page_methods': [PageMethod('wait_for_selector', 'div.scroll-m-16', timeout=30000)]},
        )
        params = {'sort': 'Newest', 'publishDate': 'All', 'readingTime': 'All', 'pageNumber': 1, 'PageSize': 20}
        yield scrapy.Request(url=f"{self.API_URL}?{urlencode(params)}", callback=self.parse_api, meta={'page': 1})

    async def parse_web(self, response):
        page = response.meta['playwright_page']
        try:
            articles = await page.evaluate('''() => {
                const items = [];
                document.querySelectorAll('div.scroll-m-16').forEach(el => {
                    const a = el.querySelector('h3 a');
                    if (a) items.push(a.href);
                });
                return items;
            }''')
            for url in articles:
                if self.article_count >= self.MAX_ARTICLES: break
                yield response.follow(url, callback=self.parse_article)
        finally:
            await page.close()

    def parse_api(self, response):
        data = json.loads(response.text)
        for art in data.get('source', [])[:self.MAX_ARTICLES - self.article_count]:
            if art.get('slug'):
                yield response.follow(f"{self.ARTICLE_BASE_URL}{art['slug']}/", callback=self.parse_article)

    def parse_article(self, response):
        if self.article_count >= self.MAX_ARTICLES:
            return
        self.article_count += 1

        title = response.css('h1::text').get(default='').strip()
        paragraphs = response.css('div[itemprop="articleBody"] p::text, div.article-body p::text, div.post-content p::text').getall()
        if not paragraphs:
            paragraphs = response.css('p.sc-9996cfc-0.gAFslo.sc-b2ef6c17-0.joXpaW::text').getall()
        content = "\n".join(p.strip() for p in paragraphs if p.strip())

        source = response.css('div.sc-8efc4a6a-4 a::text, div.source::text, span.source-name::text').get(default='زومیت').strip()

        tags = response.css('span.sc-9996cfc-0.NawFH::text').getall()
        tags = [t.strip() for t in tags if t.strip()]

        yield {
            'title': title,
            'content': content,
            'source': source,
            'tags': tags
        }

    async def errback(self, failure):
        page = failure.request.meta.get('playwright_page')
        if page: await page.close()
