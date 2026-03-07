# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RealEstateScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    url = scrapy.Field()
    listing_type = scrapy.Field()  # 'rent' or 'sale'
    Bedrooms = scrapy.Field()
    Bathrooms = scrapy.Field()
    Area_sqm = scrapy.Field()
    price_monthly = scrapy.Field()
    price_annualy = scrapy.Field()
    sale_price = scrapy.Field()
    area = scrapy.Field()
    furnished = scrapy.Field()
    pool = scrapy.Field()
    floor = scrapy.Field()
    floor_type = scrapy.Field()
    location = scrapy.Field()
    description = scrapy.Field()
    specialities = scrapy.Field()

