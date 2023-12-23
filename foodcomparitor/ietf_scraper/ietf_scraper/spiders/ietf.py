import scrapy


class IetfSpider(scrapy.Spider):
    name = "ietf"
    allowed_domains = ["pythonscraping.com"]
    start_urls = [
        "https://www.woolworths.com.au/shop/search/products?searchTerm=a&pageNumber=1&sortBy=TraderRelevance&filter=Category(1_39FD49C%2C1_9E92C35%2C1_5AF3A0A%2C1_717445A%2C1_D5A2236%2C1-E5BEE36E%2C1_6E4F4E4)%3BSoldBy(Woolworths)",
    ]

    def parse(self, response):
        link_file = open("links.txt", "w")
        for i in range(1, 36):
            link = response.xpath(
                f"""//wow-product-search-container/shared-grid/div/div[{i}]/shared-product-tile/shared-web-component-wrapper/wc-product-tile//section/div[4]/div[1]/a/@href"""
            ).get()
            link_name = f"link{i}"
            yield {link_name: link}
            # link_file.write(link + "\n")
            # link_file.write("hello")
