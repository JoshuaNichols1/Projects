import scrapy
import sqlite3

link_file = open("links.txt", "r")
global temp_urls
temp_urls = [str(link) for link in link_file]


class IetfSpider(scrapy.Spider):
    name = "parsing_coles"
    start_urls = temp_urls[340:360]

    def __init__(self):
        self.results = []
        self.count = 0
        self.max = len(temp_urls[340:360]) - 1

    def parse(self, response):
        con = sqlite3.connect("foodcompare.db")
        cur = con.cursor()
        product_name = response.xpath("/html/head/title/text()").get()
        product_name = product_name[4:-8]
        description = response.xpath(
            "//div[@data-testid='section-header']/div/div/div/text()"
        ).get()
        if description is None:
            description = response.xpath("//div[@data-testid='section-header']//p").get()
            if description is not None:
                description = (
                    description.replace("<p>", "")
                    .replace("</p>", "")
                    .replace("<br>", "")
                    .replace("</br>", "")
                )
        kj = response.xpath(
            "/html/body/div[1]/div[1]/div[1]/div/div[5]/ul/li[1]/div/div/table/tbody/tr[2]/td[2]/div/text()"
        ).get()
        protein = response.xpath(
            "/html/body/div[1]/div[1]/div[1]/div/div[5]/ul/li[1]/div/div/table/tbody/tr[3]/td[2]/div/text()"
        ).get()
        total_fat = response.xpath(
            "/html/body/div[1]/div[1]/div[1]/div/div[5]/ul/li[1]/div/div/table/tbody/tr[4]/td[2]/div/text()"
        ).get()
        saturated_fat = response.xpath(
            "/html/body/div[1]/div[1]/div[1]/div/div[5]/ul/li[1]/div/div/table/tbody/tr[5]/td[2]/div/text()"
        ).get()
        carbohydrates = response.xpath(
            "/html/body/div[1]/div[1]/div[1]/div/div[5]/ul/li[1]/div/div/table/tbody/tr[6]/td[2]/div/text()"
        ).get()
        sugars = response.xpath(
            "/html/body/div[1]/div[1]/div[1]/div/div[5]/ul/li[1]/div/div/table/tbody/tr[7]/td[2]/div/text()"
        ).get()
        sodium = response.xpath(
            "/html/body/div[1]/div[1]/div[1]/div/div[5]/ul/li[1]/div/div/table/tbody/tr[8]/td[2]/div/text()"
        ).get()
        ingredients = response.xpath("//div[@id='ingredients-control']/div/div/text()").get()
        if ingredients is not None:
            ingredients = ingredients.capitalize()
        worked = self.results.append(
            (
                response.url,
                product_name,
                description,
                kj,
                protein,
                total_fat,
                saturated_fat,
                carbohydrates,
                sugars,
                sodium,
                ingredients,
            )
        )
        if worked:
            self.count += 1
        else:
            self.max -= 1
        if self.count == self.max:
            con = sqlite3.connect("foodcompare.db")
            cur = con.cursor()
            cur.executemany(
                "INSERT INTO product2 VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", self.results
            )
            con.commit()
            con.close()
        # # yield {
        # #     "product_url": response.url,
        # #     "product_name": product_name,
        # #     "description": description,
        # #     "kj": kj,
        # #     "protein": protein,
        # #     "total_fat": total_fat,
        # #     "saturated_fat": saturated_fat,
        # #     "carbohydrates": carbohydrates,
        # #     "sugars": sugars,
        # #     "sodium": sodium,
        # #     "ingredients": ingredients,
        # # }
