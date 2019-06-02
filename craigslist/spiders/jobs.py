import scrapy
from scrapy import Request

class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["craigslist.org"]
    start_urls = ["https://newyork.craigslist.org/search/egr"]

    def parse(self, response):
        jobs = response.xpath('//p[@class="result-info"]')
        for job in jobs:
            url = job.xpath("a/@href").extract_first()
            title = job.xpath('a/text()').extract_first()
            address = job.xpath('span[@class="result-meta"]/span[@class="result-hood"]/text()').extract_first()
            
            yield Request(url, callback=self.parse_page, meta={'URL':url, 'TITLE':title, 'ADDRESS':address})
        next_page_url = response.xpath('//a[@class="button next"]/@href').extract_first()
        absolute_next_page_url = 'https://newyork.craigslist.org' + next_page_url
        yield Request(absolute_next_page_url, callback=self.parse)

    def parse_page(self, response):
        url = response.meta.get('URL')
        title = response.meta.get('TITLE')
        address = response.meta.get('ADDRESS')
        description = "".join(line for line in response.xpath('//*[@id="postingbody"]/text()').extract())
        compensation = response.xpath('//p[@class="attrgroup"]/span[1]/b/text()').extract_first()
        employment_type = response.xpath('//p[@class="attrgroup"]/span[2]/b/text()').extract_first()

        yield {'URL':url, 'TITLE': title, 'ADDRESS': address, 'DESCRIPTION': description, 'COMPENSATION': compensation, 'EMPLOYMENT_TYPE': employment_type}

