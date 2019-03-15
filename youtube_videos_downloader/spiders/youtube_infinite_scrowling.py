#usage scrapy runspider youtube_infinite_scrowling.py
#Scraping Infinite Scrolling Pages 
from __future__ import unicode_literals
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.item import Item, Field
import time
from time import sleep
from lxml import html
from selenium import webdriver
import scrapy
from itertools import count
import scrapy
import requests
import scrapy
import youtube_dl

class ItatSpider(scrapy.Spider):
    chrome_options = webdriver.ChromeOptions()
    name = "youtube"  # Name of the Spider, required value
    allowed_domains = ['www.youtube.com']
    start_urls = ["https://www.youtube.com/results?search_query=data+science"]
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path=r'/home/nebulae-ws1/Downloads/Software/chromedriver',chrome_options=self.chrome_options)
        self.driver.implicitly_wait(30)
        self.session_requests = requests.session()

    def parse(self, response):
        self.driver.get("https://www.youtube.com/results?search_query=data+science")
        Y = 1000
        scrowling_down_count = 20
        for _ in range(scrowling_down_count):
          self.driver.execute_script("window.scrollTo(0, "+str(Y)+");")
          sleep(3)
          Y += 1000
        for element in self.driver.find_elements_by_id("video-title"):
          url = element.get_attribute("href")
          print("url is \n", url)
          if url:
            ydl_opts = {}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
              result = ydl.extract_info(url,download=False)
              duration = result.get('duration')
              print("duration of",url,"url is",duration)
              if duration and (duration < 1600):
                print("downloading video num -",count)
                ydl.download([url])
              else:
                print("video duration is more than 10 minutes")
