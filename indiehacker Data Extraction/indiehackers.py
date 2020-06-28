#Usage: python indiehackers.py
import requests
import time
from time import sleep
import scrapy
import urllib.request
from scrapy.http import Request
import re
from scrapy.crawler import CrawlerProcess
import jsonlines
import logging
from twisted.internet.defer import inlineCallbacks, returnValue, DeferredList
from scrapy.settings import Settings
from csv import DictWriter
import json

class IndieSpider(scrapy.Spider):
    name='indiehackers'

    def __init__(self,raw_data_file=None, **kwargs):
        if not raw_data_file:
            raise Exception('Missing Spider Props: {}'.format(self.name))

        self.raw_data_file = raw_data_file

    def start_requests(self):
        url="https://www.indiehackers.com"
        yield Request(url, self.get_product_details)

    @inlineCallbacks
    def get_product_details(self, response):
        for i in range(1000): #can be vary depending on the pages
            try:
                request = scrapy.Request("https://n86t1r3owz-3.algolianet.com/1/indexes/*/queries?x-algolia-agent=Algolia%20for%20JavaScript%20(3.35.1)%3B%20Browser%20(lite)%3B%20JS%20Helper%202.21.1&x-algolia-application-id=N86T1R3OWZ&x-algolia-api-key=5140dac5e87f47346abbda1a34ee70c3", method='post', body = "{\"requests\":[{\"indexName\":\"products\",\"params\":\"query=&hitsPerPage=16&page="+str(i)+"&restrictSearchableAttributes=&facets=%5B%5D&tagFilters=\"}]}", headers =  {
                    "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0",
                    "Accept": "application/json",
                    "Accept-Language": "en-US,en;q=0.5",
                    "content-type": "application/x-www-form-urlencoded",
                    "Referer" : "https://www.indiehackers.com/products?sorting=recently-updated"})
                response = yield self.crawler.engine.download(request, self)
                json_data = json.loads(response.text)
                results = json_data["results"]
                hits = results[0]["hits"]
                if not hits:
                    break
                keys = ["name","tagline","revenue","revenue_type", "numFollowers", "websiteUrl","description", "city", "country", "twitterHandle"]
                for product in hits:
                    if ('stripe-verified-revenue' in product["_tags"]):
                        product["revenue_type"] = 'stripe-verified revenue'
                    else:
                        product["revenue_type"] = 'self-reported revenue'
                with open(self.raw_data_file,'a') as outfile:
                    writer = DictWriter(outfile, keys, extrasaction='ignore')
                    writer.writeheader()
                    writer.writerows(hits)
            except Exception as e:
                print("exception is", e)


if __name__ == "__main__":
    scrapy_settings = Settings()
    process = CrawlerProcess(scrapy_settings)
    process.crawl(IndieSpider, raw_data_file = "indiehacker_results.csv")

    process.start()