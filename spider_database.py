import scrapy

class Spider1(scrapy.spiders.Spider):
    name = "fuji1"
    start_urls = ["https://www.fotokoch.de/Fujifilm-X100V-schwarz_64109.html"]

    
    def parse(self, response):
        yield{
            'status': response.css("div.shipping-state::text").get(),
            'url':response.url
        }

class Spider2(scrapy.spiders.Spider):
    name = "fuj2"
    start_urls = ["https://www.fotomeyer.de/fujifilm-x100v-schwarz-79707.html"]

  
    def parse(self, response):
        yield{
            'status': response.css('p.availability span::text').get().replace("\t","").replace("\n",""),
            'url':response.url
        }

class Spider3(scrapy.spiders.Spider):
    name = "fuj3"
    start_urls = ["https://www.calumetphoto.de/product/Fujifilm-X100V-Kompaktkamera-schwarz/FUJX100VBL"]

  
    def parse(self, response):
        yield{
            'status': response.css("span.info-availability::text").get(),
            'url':response.url
        }

class Spider4(scrapy.spiders.Spider):
    name = "fuj4"
    start_urls = ["https://www.fujifilm-shop.de/fujifilm-x100v-schwarz.html"]

  
    def parse(self, response):
        yield{
            'status': response.css("div.product-info-stock-sku span::text").get(),
            'url':response.url
        }

class Spider5(scrapy.spiders.Spider):
    name = "fuj5"
    start_urls = ["https://www.foto-leistenschneider.de/Fujifilm-X100V-Schwarz/060350150817"]

  
    def parse(self, response):
        yield{
            'status': response.css("div.store-status span").get(),
            'url':response.url
        }

class Spider6(scrapy.spiders.Spider):
    name = "fuj6"
    start_urls = ["https://www.foto-erhardt.de/kameras/systemkameras/fuji-systemkameras/fujifilm-x100v-schwarz.html"]

  
    def parse(self, response):
        yield{
            'status': response.css("button#addtocart-primary::text").get(),
            'url':response.url
        }

class Spider7(scrapy.spiders.Spider):
    name = "fuj7"
    start_urls = ["https://www.fuji-store.de/p/vorbestellung-fujifilm-x-100v-schwarz"]

  
    def parse(self, response):
        yield{
            'status': response.css("span.product-availability-info::text").get(),
            'url':response.url
        }

#fotogregor krieg ich nciht hin 

#fotoprofi auch kacke
def get_all_spiders():
    return [Spider1,Spider2,Spider3,Spider4,Spider5,Spider6,Spider7]