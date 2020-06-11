# coding: utf8
import scrapy
import logging

class ParsWine(scrapy.Spider):
    logging.getLogger('scrapy').setLevel(logging.WARNING)
    logging.getLogger('scrapy').propagate = False

    name = "pars_wine"
    allowed_domains = ["eurocave.ru"]
    start_urls = [
            'http://eurocave.ru/products/'
        ]
    custom_settings = {
        'FEED_URI': 'result.json',
        'FEED_FORMAT': 'json'
    }
    def parse(self, response):
        product_item = response.css('article div.product-item')
        try:
            if not product_item:
                for category in response.css('article div.category-item'):
                    next_page = category.css('div.wrapper div.category-capt-txt a').attrib['href']
                    yield response.follow(next_page, callback=self.parse)
            else:
                for item in product_item:
                    product_temp = item.css('div.wrapper div.product-link')[0]
                    product_text = product_temp.css('a::text').get(default='').strip()
                    if 'шкаф' in product_text.split(' ') or 'шкаф,' in product_text.split(' '):
                        yield response.follow(product_temp.css('a::attr(href)').get(default=''), callback=self.take_color)
                    else:
                        yield {
                            'name': product_text,
                            'cost': item.css('span.product-price-data::attr(data-cost)').get(default=''),
                            'status': item.css('div.quantity-products::text').get(default='').strip(),
                            'url': response.url,
                            'color': 'не шкаф'
                        }
        except Exception as err:
            print(err)
    
    def take_color(self, response):
        try:
            if True: 
                position = response.css('div.product-content div.row-fluid div.span8 div.user-inner')
                f = len(position.css('p')) 
                if (f > 3) and (16 > f):
                    position = position.css('p')
                else:
                    position = position.css('table')
                    for item in position:
                        temp = item.css('tbody tr')
                        if len(temp) == 1:
                            temp = temp.css('td')
                            if len(temp) == 2:
                                position = temp[-1].css('p')
                # print(len(position))     
                if position:
                    flag = False
                    for item in position:
                        try:
                            line = item.css('span')[0].css('::text').get(default='').strip(' ').split('\xa0')
                            color = line[0].split(' ')
                            if 'Цвет' in color:
                                if 'черный' in color or 'черный' in line:
                                    flag = True
                        except IndexError as err:
                            const = ['http://eurocave.ru/products/15737787', 'http://eurocave.ru/products/15332736']
                            if response.url in const:
                                yield self.simple_return(response=response, color='черный')
                            else:
                                print(err)
                                print(response.url)
                            # if 'черный\xa0' in color or 'черный\xa0' in line:
                            #     flag = True
                    if flag:
                        yield self.simple_return(response=response, color='черный')
                    else:
                        yield self.simple_return(response=response, color='не черный')
                else:
                    yield self.simple_return(response=response, color='шкаф без описания')
        except Exception as err:
            print(err)
            print(response.url)
            print(self.simple_return(response=response, color='error'))

    def simple_return( 
        self,
        response = None,
        name = 'div.span8 h1::text', 
        cost = 'span.product-price-data::text', 
        status = 'div.quantity-products div.-f-big::text', 
        url = None, 
        color = None):
        return {
            'name': response.css(name).get(default=''),
            'cost': response.css(cost).get(default=''),
            'status': response.css(status).get(default=''),
            'url': response.url,
            'color': color
        }
