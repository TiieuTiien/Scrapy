import scrapy


class TruyenfullSpider(scrapy.Spider):
    name = "truyenfull"
    allowed_domains = ["truyenfull.vision"]
    start_urls = ["https://truyenfull.vision/my-dung-su-xuyen-qua-lam-nong-phu-lam-giau-nuoi-con/chuong-1/"]
    counter = 0

    def parse(self, response):
        truyen = response.css('.col-xs-12')

        yield {
            'title': truyen.css('.chapter-title::attr(title)').get(),
            'content': truyen.css('.chapter-c p::text').getall(),
        }
        
        next_chap = response.css('#next_chap::attr(href)').get()

        if next_chap is not None and self.counter < 5:
            self.counter += 1
            print(f"Following to next chapter: {next_chap}")
            yield response.follow(next_chap, callback=self.parse)
