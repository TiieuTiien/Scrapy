import scrapy
from truyenfullcrawler.items import TruyenItem


class TruyenfullSpider(scrapy.Spider):
    name = "truyenfull"
    allowed_domains = ["truyenfull.vision"]
    start_urls = ["https://truyenfull.vision/my-dung-su-xuyen-qua-lam-nong-phu-lam-giau-nuoi-con/chuong-1/"]
    counter = 0

    def parse(self, response):
        # Extract content on current page
        yield from self.parse_chapter(response)
        
        # Follow to next chapter
        next_chap = response.css('#next_chap::attr(href)').get()
        
        if next_chap is not None and self.counter < 3:
            self.counter += 1
            print(f"Following to next chapter: {next_chap}")
            print()
            yield response.follow(next_chap, callback=self.parse)

    def parse_chapter(self, response):
        """Dedicated callback for parsing chapter content"""
        truyen_item = TruyenItem()
        truyen_item['title'] = response.css('.chapter-title::attr(title)').get()
        truyen_item['content'] = response.css('.chapter-c p::text').getall()
        
        print(f"Parsing chapter: {truyen_item['title']}")
        yield truyen_item