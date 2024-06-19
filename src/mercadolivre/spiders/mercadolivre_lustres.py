import scrapy


class MercadolivreLustresSpider(scrapy.Spider):
    name = "mercadolivre-lustres"
    allowed_domains = ["lista.mercadolivre.com.br"]
    start_urls = ["https://lista.mercadolivre.com.br/lustre-mdf-pendente"]
    page_count = 1
    max_pages = 2

    def parse(self, response):
        products = response.css('div.ui-search-result__content')
        
        for product in products:

           prices = product.css('span.andes-money-amount__fraction::text').getall()
           cents = product.css('span.andes-money-amount__cents::text').getall()

           yield {
               'title': product.css('h2.ui-search-item__title::text').get(),
               'rating': product.css('span.ui-search-reviews__rating-number::text').get(),
               'old_price': prices[0] if len(prices) > 0 else None,
               'old_cents': cents[0] if len(cents) > 0 else None,
               'new_price': prices[1] if len(prices) > 1 else None,
               'new_cents': cents[1] if len(cents) > 1 else None,
               'is_free_ship': product.css('span.ui-pb-highlight::text').get(),
               'is_full': product.css('span.ui-pb-label::text').get(),
               'is_ads': product.css('label.ui-search-styled-label.ui-search-item__pub-label::text').get(),
               'page': self.page_count 
           } 
        
        if self.page_count < self.max_pages:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get()
            if next_page:
                self.page_count += 1
                yield scrapy.Request(url=next_page, callback=self.parse)