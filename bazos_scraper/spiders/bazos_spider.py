from scrapy.spiders import SitemapSpider


class BazosSitemapSpider(SitemapSpider):
    name = 'bazos'
    with open('urls.txt') as f:
        start_urls = [url.strip() for url in f.readlines()]
    sitemap_urls = [f'{url}sitemap.php' for url in start_urls]

    sitemap_rules = [
        ('/inzerat/', 'parse'),
    ]
    

    def parse(self, response):
        bazosurl = response.url
        category = response.xpath('//div[@class="drobky"]/a[2]/text()').extract_first()
        subcategory = response.xpath('//div[@class="drobky"]/a[3]/text()').extract_first()
        subsubcategory = response.xpath('//div[@class="drobky"]/a[4]/text()').extract_first()
        advertid = response.xpath('//div[@class="drobky"]/b/text()').extract_first()
        advertid = advertid.replace('Inzerát č.', '').replace(' ', '') if advertid else None
        title = response.xpath('//h1[@class="nadpisdetail"]/text()').extract_first()
        topped = response.xpath('//span[@class="ztop"]/text()').extract_first()
        
        date = response.xpath('//span[@class="velikost10"]/text()')
        if len(date) > 1:
            try:
                date = date[1].extract().split(' - ')[1]
            except:
                date = None
        else:
            date = None
            
        name = response.xpath('//span[@class="paction"]/text()')
        if len(name) > 1:
            name = name[1].extract()
        else:
            name = None
            
        gmapsurl = response.xpath('//td/a/@href').extract_first()
        zipnumber = response.xpath('//td[3]/a/text()').extract_first()
        cityloc = response.xpath('//td[3]/a/text()')
        if len(cityloc) > 1:
            cityloc = cityloc[1].extract()
        else:
            cityloc = None
            
        price = response.xpath('//tr/td/b/text()').extract_first()
        price = price.replace(' ', '').replace('€', '') if price else None
        views = response.xpath('//td/text()').extract()
        if len(views) > 6:
            try:
                views = views[6].replace('ľudí', '').replace(' ', '')
            except:
                views = None
        else:
            views = None
        description = response.xpath('//div[@class="popisdetail"]/text()').extract()
        
        yield {
            'bazosurl':bazosurl,
            'category': category,
            'subcategory': subcategory,
            'subsubcategory': subsubcategory,
            'advertid': advertid,
            'title': title,
            'topped': topped,
            'date': date,
            'name': name,
            'gmapsurl': gmapsurl,
            'zipnumber': zipnumber,
            'cityloc': cityloc,
            'price': price,
            'views': views,
            'description': description
        }