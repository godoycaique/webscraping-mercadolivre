import scrapy


class MercadolivreLustresSpider(scrapy.Spider):
    name = "mercadolivre-lustres"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/lustre-mdf-pendente"]

    def parse(self, response):
        products = response.css('div.ui-search-result__content')
        
        for product in products:
            
           yield {
               'title': product.css('h2.ui-search-item__title::text').get() 
           } 