from __future__ import unicode_literals
import scrapy
import requests
from scrapy.http import Request
import requests
import scrapy
from scrapy.crawler import CrawlerProcess
from pytube import YouTube
import youtube_dl
class YoutubeVideosSpider(scrapy.Spider):
  name = "youtube_videos_spider"
  start_urls = []
  keywords = ["data science", "python tutorials", "djongo"]
  for keyword in keywords:
    keys = keyword.split(' ')
    start_urls.append("https://www.youtube.com/results?search_query="+'+'.join(keys))
     
  def parse(self,response):
    videos_urls = [i for i in response.xpath('//@href').extract() if "watch?" in i]
    count = 0
    for url in videos_urls:
      print("\n url is ", "https://www.youtube.com"+url)
      if len(url) < 30:
        url = "https://www.youtube.com"+url
        ydl_opts = {}
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(
                url,
                download=False # We just want to extract the info
            )
        duration = result.get('duration')
        print("duration of",url,"url is",duration)
        if duration and (duration < 600):
          count += 1
          print("downloading video num -",count)
          ydl.download([url])
        print("video duration is more than 10 minutes")
# if __name__ == "__main__":
    # keywords2 = ["Natarajan", "Ravichandran", "MARUTI SUZUKI"]
    # process = CrawlerProcess()
    # # for keyword in keywords2:
    # #     process.crawl(YoutubeVideosSpider, keyword)
    # #     pass
    # process.start()