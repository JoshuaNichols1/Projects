import scrapy


class IetfSpider(scrapy.Spider):
    name = "ietf"
    allowed_domains = ["pythonscraping.com"]
    start_urls = [
        "https://www.woolworths.com.au/shop/productdetails/172235/in-a-biskit-drumstix-crackers",
        "https://www.woolworths.com.au/shop/productdetails/112725/dj-a-veggie-crisps-original",
    ]

    def parse(self, response):
        def format_parse(xpath):
            result = response.xpath(f"{xpath}").get()
            result = result.replace("\n                    ", "")
            result = result.replace("\n                ", "")
            return result.strip()

        food_name = response.xpath("//div/h1/text()").get()
        ingredients = response.xpath(
            """/html/body/ar-partial/ar-product-detail-container/section/div[2]/section[1]/ar-view-more/div/div/div/div/text()"""
        ).get()
        serving_size = response.xpath(
            """/html/body/ar-partial/ar-product-detail-container/section/div[2]/ar-product-details-nutrition-table/section/div[2]/text()"""
        ).get()
        kj = format_parse(
            "/html/body/ar-partial/ar-product-detail-container/section/div[2]/ar-product-details-nutrition-table/section/div[3]/ul[2]/li[2]/text()"
        )
        protein = format_parse(
            """/html/body/ar-partial/ar-product-detail-container/section/div[2]/ar-product-details-nutrition-table/section/div[3]/ul[3]/li[2]/text()"""
        )
        fat_total = format_parse(
            """/html/body/ar-partial/ar-product-detail-container/section/div[2]/ar-product-details-nutrition-table/section/div[3]/ul[4]/li[2]/text()"""
        )
        fat_saturated = format_parse(
            """/html/body/ar-partial/ar-product-detail-container/section/div[2]/ar-product-details-nutrition-table/section/div[3]/ul[5]/li[2]/text()"""
        )
        carbs = format_parse(
            """/html/body/ar-partial/ar-product-detail-container/section/div[2]/ar-product-details-nutrition-table/section/div[3]/ul[6]/li[2]/text()"""
        )
        sugars = format_parse(
            """/html/body/ar-partial/ar-product-detail-container/section/div[2]/ar-product-details-nutrition-table/section/div[3]/ul[7]/li[2]/text()"""
        )
        dietary_fibre = format_parse(
            """/html/body/ar-partial/ar-product-detail-container/section/div[2]/ar-product-details-nutrition-table/section/div[3]/ul[8]/li[2]/text()"""
        )
        sodium = format_parse(
            """/html/body/ar-partial/ar-product-detail-container/section/div[2]/ar-product-details-nutrition-table/section/div[3]/ul[9]/li[2]/text()"""
        )
        return {
            "food_name": food_name,
            "ingredients": ingredients,
            "serving_size": serving_size,
            "kj": kj,
            "fat_total": fat_total,
            "fat_saturated": fat_saturated,
            "carbs": carbs,
            "sugars": sugars,
            "dietary_fibre": dietary_fibre,
            "sodium": sodium,
        }
