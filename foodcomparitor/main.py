import openfoodfacts
import scrapy
import sqlite3
from flask import Flask, render_template, request, redirect, url_for

api = openfoodfacts.API()

app = Flask(__name__)
app.config["SECRET_KEY"] = "your secret key"


@app.route("/productsearch", methods=("GET", "POST"))
@app.route("/", methods=("GET", "POST"))
@app.route("/home", methods=("GET", "POST"))
@app.route("/index", methods=("GET", "POST"))
def productsearch():
    return render_template(
        "index.html",
    )


@app.route("/productsearch", methods=("GET", "POST"))
def productsearchresults():
    if request.method == "POST":
        search_term = request.form["search"]
        if not search_term:
            search_term = request.form.get("search")
            if not search_term:
                flash("Please enter a search term")
                return redirect(url_for("productsearch"))
        con = sqlite3.connect(
            "E:\Coding\Projects\\foodcomparitor\ietf_scraper\spiders\\foodcompare.db"
        )
        cur = con.cursor()
        result = cur.execute(
            "SELECT * FROM product WHERE product_name LIKE ?", (f"%{search_term}%",)
        )
        result = result.fetchall()
        if result:
            products = []
            for num, row in enumerate(result):
                products.append(f"{num+1}: {row[1]}")
            return redirect(url_for("productsearch", products=products))
        else:
            flash("No results found")
            return redirect(url_for("productsearch"))
    else:
        return redirect(url_for("productsearch"))


@app.route("/product/<product_id>")
def product_detail(product_id):
    # Fetch product details from the database using product_id
    cur.execute("SELECT * FROM products WHERE id=?", (product_id,))
    result = cur.fetchone()
    if result:
        return render_template(
            "product_details.html",
            product_name=result[1] if result[1] else "No product name available",
            product_description=result[2] if result[2] else "No product description available",
            product_energy=result[3] if result[3] else "No energy details available",
            product_protein=result[4] if result[4] else "No protein details available",
            product_total_fat=result[5] if result[5] else "No total fat details available",
            product_saturated_fat=result[6] if result[6] else "No saturated fat details available",
            product_carbohydrates=result[7] if result[7] else "No carbohydrate details available",
            product_sugar=result[8] if result[8] else "No sugar details available",
            product_sodium=result[9] if result[9] else "No sodium details available",
            product_ingredients=result[10] if result[10] else "No ingredients available",
        )
    else:
        flash("No product found")
        return redirect(url_for("productsearch"))


# @app.route("/productdetails", methods=["POST"])
# def productdetails():
#     def format_result(text):
#         return " ".join(text[3:].split("_"))

#     if request.method == "POST":
#         search_term = request.form.get("search")
#         con = sqlite3.connect(
#             "E:\Coding\Projects\\foodcomparitor\ietf_scraper\spiders\\foodcompare.db"
#         )
#         cur = con.cursor()
#         result = cur.execute(
#             "SELECT * FROM product WHERE product_name LIKE ?", (f"%{search_term}%",)
#         )
#         result = result.fetchall()
#         if result:
#             for num, row in enumerate(result):
#                 print(f"{num+1}: {row[1]}")
#             choice = input("Please enter the number of the item you want to view: ")
#             while not (choice.isdigit() & 0 < int(choice) <= len(result)):
#                 choice = input("Please enter the number of the item you want to view: ")
#             product = result[int(choice) - 1]
#             return render_template(
#                 "comparitor.html",
#                 product_name=product[1],
#                 product_description=product[2],
#                 product_energy=product[3],
#                 product_protein=product[4],
#                 product_total_fat=product[5],
#                 product_saturated_fat=product[6],
#                 product_carbohydrates=product[7],
#                 product_sugar=product[8],
#                 product_sodium=product[9],
#                 product_ingredients=product[10],
#             )
#         else:
#             return redirect(url_for("productsearch"))
#     else:
#         return redirect(url_for("productsearch"))


if __name__ == "__main__":
    app.run(debug=True)

# using the openfoodfacts api

# result = api.product.text_search(search_term)
# products = result["products"]
# for num, product in enumerate(products):
#     if num == 20:
#         break
#     if product["product_name"]:
#         print(f"""{num+1}: {product["product_name"]}""")

# choice = input("Please enter the number of the item you want to view: ")
# while not (choice.isdigit() & 0 < int(choice) < 20):
#     choice = input("Please enter the number of the item you want to view: ")
# product = products[int(choice) - 1]
# print("Product details:")
# print(f"""Name: {product["product_name"]}""")
# print(f"Alergens:")
# for alergen in product["allergens_hierarchy"]:
#     print(f"""- {format_result(alergen)}""")
# print("Catagories:")
# for category in product["categories_tags"]:
#     print(f"""- {format_result(category)}""")
# if product["ecoscore_data"]["adjustments"]["threatened_species"]:
#     print(
#         f"""Ingredient Warnings: {format_result(product["ecoscore_data"]["adjustments"]["threatened_species"]["ingredient"])}"""
#     )
# print("Ingredients:")
# for ingredient in product["ecoscore_extended_data"]["impact"]["likeliest_recipe"]:
#     if format_result(ingredient).isalpha():
#         print(f"- {ingredient[3:]}")
