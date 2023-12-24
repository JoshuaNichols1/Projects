import openfoodfacts
import scrapy
import sqlite3
from flask import Flask, flash, render_template, request, redirect, url_for

api = openfoodfacts.API()

app = Flask(__name__)
app.config["SECRET_KEY"] = "your secret key"

global products
products = []
global product_nums
product_nums = []
global original_results
original_results = []
global opened_file
opened_file = open("E:\Coding\Projects\\foodcomparitor\\text.txt", "a")
global comp_products
comp_products = []
global comp_product_nums
comp_product_nums = []
global comp_products2
comp_products2 = []
global com_original_results
com_original_results = []
global com_original_results2
com_original_results2 = []


@app.route("/productsearch", methods=("GET", "POST"))
@app.route("/", methods=("GET", "POST"))
@app.route("/home", methods=("GET", "POST"))
@app.route("/index", methods=("GET", "POST"))
def productsearch():
    if request.args.get("show_results") == "Yes":
        return render_template(
            "index.html",
            products=products,
            product_nums=product_nums,
        )
    return render_template("index.html", show_results="No")


@app.route("/productsearchresults", methods=("GET", "POST"))
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
        result2 = cur.execute(
            "SELECT * FROM product2 WHERE product_name LIKE ?", (f"%{search_term}%",)
        )
        result2 = result2.fetchall()
        result += result2
        global original_results
        original_results = list(result)
        if result:
            products.clear()
            product_nums.clear()
            for num, row in enumerate(result):
                products.append(row[1])
                product_nums.append(num + 1)
            return redirect(url_for("productsearch", show_results="Yes"))
        else:
            flash("No results found")
            return redirect(url_for("productsearch"))
    else:
        return redirect(url_for("productsearch"))


@app.route("/product/<product_id>", methods=("GET", "POST"))
def product_detail(product_id):
    if request.method == "POST":
        product_id = original_results[int(product_id)][0]
        con = sqlite3.connect(
            "E:\Coding\Projects\\foodcomparitor\ietf_scraper\spiders\\foodcompare.db"
        )
        cur = con.cursor()
        cur.execute("SELECT * FROM product WHERE product_url=?", (product_id,))
        result = cur.fetchone()
        if result:

            def format_result(result_var, text):
                if (result_var == None) | (result_var == "None") | (result_var == ""):
                    return text
                return result_var

            return render_template(
                "product_details.html",
                product_name=format_result(result[1], "No product name available"),
                product_description=format_result(result[2], "No product description available"),
                product_energy=format_result(result[3], "No energy details available"),
                product_protein=format_result(result[4], "No protein details available"),
                product_total_fat=format_result(result[5], "No total fat details available"),
                product_saturated_fat=format_result(
                    result[6], "No saturated fat details available"
                ),
                product_carbohydrates=format_result(result[7], "No carbohydrate details available"),
                product_sugar=format_result(result[8], "No sugar details available"),
                product_sodium=format_result(result[9], "No sodium details available"),
                product_ingredients=format_result(result[10], "No ingredients available"),
            )
        else:
            flash("No product found")
            return redirect(url_for("productsearch"))
    else:
        return redirect(url_for("productsearch"))


@app.route("/compsearch", methods=("GET", "POST"))
def comparison_search():
    if request.args.get("show_results") == "Yes":
        return render_template(
            "compare_search.html",
            products=comp_products,
            product_nums=comp_product_nums,
            products2=comp_products2,
        )
    return render_template("compare_search.html")


@app.route("/compsearchresults", methods=("GET", "POST"))
def compsearchresults():
    if request.method == "POST":

        def get_results(search_term):
            con = sqlite3.connect(
                "E:\Coding\Projects\\foodcomparitor\ietf_scraper\spiders\\foodcompare.db"
            )
            cur = con.cursor()
            result = cur.execute(
                "SELECT * FROM product WHERE product_name LIKE ?", (f"%{search_term}%",)
            )
            result = result.fetchall()
            result2 = cur.execute(
                "SELECT * FROM product2 WHERE product_name LIKE ?", (f"%{search_term}%",)
            )
            result2 = result2.fetchall()
            result += result2
            return result

        search_term = request.form["search"]
        search_term2 = request.form["search2"]
        if not (search_term and search_term2):
            search_term = request.form.get("search")
            search_term2 = request.form.get("search2")
            if not search_term & search_term2:
                flash("Please enter both search terms")
                return redirect(url_for("comparison_search"))
        result = get_results(search_term)
        result2 = get_results(search_term2)
        global com_original_results
        com_original_results = list(result)
        global com_original_results2
        com_original_results2 = list(result2)
        if result and result2:
            comp_products.clear()
            comp_product_nums.clear()
            comp_products2.clear()
            for num, row in enumerate(result):
                comp_products.append(row[1])
                comp_product_nums.append(num + 1)
                comp_products2.append(result2[num][1])
            return redirect(url_for("comparison_search", show_results="Yes"))
        else:
            flash("No results found")
            return redirect(url_for("comparison_search"))
    else:
        return redirect(url_for("comparison_search"))


@app.route("/productcomp", methods=("GET", "POST"))
def product_comparison():
    if request.method == "POST":
        product_id = com_original_results[int(request.form["product1_id"])][0]
        product_id2 = com_original_results2[int(request.form["product2_id"])][0]
        con = sqlite3.connect(
            "E:\Coding\Projects\\foodcomparitor\ietf_scraper\spiders\\foodcompare.db"
        )
        cur = con.cursor()
        cur.execute("SELECT * FROM product WHERE product_url=?", (product_id,))
        result1 = cur.fetchone()
        if not result1:
            cur.execute("SELECT * FROM product2 WHERE product_url=?", (product_id,))
            result1 = cur.fetchone()
        cur.execute("SELECT * FROM product WHERE product_url=?", (product_id2,))
        result2 = cur.fetchone()
        if not result2:
            cur.execute("SELECT * FROM product2 WHERE product_url=?", (product_id2,))
            result2 = cur.fetchone()
        if result1 & result2:

            def format_result(result_var, text):
                if (result_var == None) | (result_var == "None") | (result_var == ""):
                    return text
                return result_var

            return render_template(
                "product_comparison.html",
                product_name=format_result(result1[1], "No product name available"),
                product_description=format_result(result1[2], "No product description available"),
                product_energy=format_result(result1[3], "No energy details available"),
                product_protein=format_result(result1[4], "No protein details available"),
                product_total_fat=format_result(result1[5], "No total fat details available"),
                product_saturated_fat=format_result(
                    result1[6], "No saturated fat details available"
                ),
                product_carbohydrates=format_result(
                    result1[7], "No carbohydrate details available"
                ),
                product_sugar=format_result(result1[8], "No sugar details available"),
                product_sodium=format_result(result1[9], "No sodium details available"),
                product_ingredients=format_result(result1[10], "No ingredients available"),
                product2_name=format_result(result2[1], "No product name available"),
                product2_description=format_result(result2[2], "No product description available"),
                product2_energy=format_result(result2[3], "No energy details available"),
                product2_protein=format_result(result2[4], "No protein details available"),
                product2_total_fat=format_result(result2[5], "No total fat details available"),
                product2_saturated_fat=format_result(
                    result2[6], "No saturated fat details available"
                ),
                product2_carbohydrates=format_result(
                    result2[7], "No carbohydrate details available"
                ),
                product2_sugar=format_result(result2[8], "No sugar details available"),
                product2_sodium=format_result(result2[9], "No sodium details available"),
                product2_ingredients=format_result(result2[10], "No ingredients available"),
            )
        else:
            flash("No product found")
            return redirect(url_for("productsearch"))
    else:
        return redirect(url_for("comparison_search"))


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
