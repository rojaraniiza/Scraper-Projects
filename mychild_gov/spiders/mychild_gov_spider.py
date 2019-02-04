# -*- coding: utf-8 -*-
import scrapy
import requests
from scrapy.crawler import CrawlerProcess
from selenium import webdriver
from selenium.webdriver import ActionChains
from lxml import html
import string
class MychildGovSpiderSpider(scrapy.Spider):
	name = 'mychild_gov_spider'
	allowed_domains = ['ifp.mychild.gov.au']
	start_urls = []
	basic = 'http://ifp.mychild.gov.au/Search/AZSearch.aspx?Location='
	alphabets = string.ascii_uppercase
	for i in alphabets:
		start_urls.append(basic+i)
	def parse(self, response):
		urls = response.xpath("//ul[@id='AZsuburbList']/li/a/@href").extract()
		print('url is ---', response.url)
		domain = 'http://ifp.mychild.gov.au'
		with open('emails_from_mychild_gov.csv', mode='a+', encoding='utf-8') as outfile:
			for url in urls:
				absolute_url = domain+url
				r = requests.get(absolute_url)
				doc = html.fromstring(r.content)
				emails = doc.xpath('//div[@class="resultItemDetail"]/a[@class="resultItemPadded"][contains(text(), "Email")]/@href')
				for email in emails:
					outfile.write(email[7:])
					outfile.write('\n')
