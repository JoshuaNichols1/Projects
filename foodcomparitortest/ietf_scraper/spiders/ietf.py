import scrapy


class IetfSpider(scrapy.Spider):
    name = "ietf"
    start_urls = [f"https://www.coles.com.au/browse/pantry?page={i}" for i in range(1, 20)]

    def __init__(self):
        self.failed = []
        self.links = []

    def parse(self, response):
        link_file = open("links.txt", "a")
        for i in range(1, 60):
            try:
                link = response.xpath(
                    f"""//*[@id="coles-targeting-product-tiles"]/section[{i}]/div[2]/header/div[2]/a/@href"""
                ).get()
                if link is not None:
                    link_file.write(f"https://www.coles.com.au{link}\n")
                    self.links.append(f"https://www.coles.com.au{link}")
            except:
                self.failed.append(i)
                if i > 50:
                    if i - 1 in failed & i - 2 in failed & i - 3 in failed:
                        break
                pass
        yield {""}
