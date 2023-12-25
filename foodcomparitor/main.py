import openfoodfacts
import scrapy
import sqlite3
from flask import Flask, flash, render_template, request, redirect, url_for

api = openfoodfacts.API()

app = Flask(__name__)
app.config["SECRET_KEY"] = "your secret key"

global products
products = []
global product_ids
product_ids = []
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


def health_score(record):
    def normalize(data):
        rdis = {
            "energy": 2000,  # Recommended daily intake for energy (kcal)
            "protein": 50,  # Recommended daily intake for protein (g)
            "total_fat": 70,  # Recommended daily intake for total fat (g)
            "saturated_fat": 20,  # Recommended daily intake for saturated fat (g)
            "carbohydrates": 275,  # Recommended daily intake for carbohydrates (g)
            "sugar": 90,  # Recommended daily intake for sugar (g)
            "sodium": 2400,  # Recommended daily intake for sodium (mg)
        }

        normalized_data = {}
        for nutrient, value in data.items():
            normalized_data[nutrient] = int(value) / rdis[nutrient]

        return normalized_data

    def remove_end(string):
        try:
            return int(record[3])
        except:
            return int(record[3][0:-2])

    data = {
        "energy": remove_end(record[3]),
        "protein": remove_end(record[4]),
        "total_fat": remove_end(record[5]),
        "saturated_fat": remove_end(record[6]),
        "carbohydrates": remove_end(record[7]),
        "sugar": remove_end(record[8]),
        "sodium": remove_end(record[9]),
    }
    weights = {
        "energy": -0.001,
        "protein": 0.002,
        "total_fat": 0.001,
        "saturated_fat": 0.003,
        "carbohydrates": 0.001,
        "sugar": 0.003,
        "sodium": 0.0001,
    }

    normalized_data = normalize(data.copy())  # Assuming a normalize function is defined
    score = 0
    for nutrient, value in normalized_data.items():
        score += weights[nutrient] * value

    # Scale the score to a range of 0 to 100
    health_score = score * 100

    return f"{health_score:.2f}"


def unhealthy_amount(record):
    nutrients = {
        "energy": 800.0,
        "protein": 5.0,
        "total_fat": 20.0,
        "saturated_fat": 5.0,
        "carbohydrates": 10.0,
        "sugar": 10.0,
        "sodium": 600.0,
    }
    warnings = {
        "energy": "High energy content",
        "protein": "Low protein content",
        "total_fat": "High fat content",
        "saturated_fat": "High saturated fat content",
        "carbohydrates": "Low carbohydrate content",
        "sugar": "High sugar content",
        "sodium": "High sodium content",
    }
    warnings_list = []
    for num, nutrient_amount in enumerate(record[3:-1]):
        if nutrient_amount == None:
            continue
        try:
            nutrient_amount = float(nutrient_amount)
        except:
            nutrient_amount = float(nutrient_amount[0:-2])
        if num == 1:
            if nutrient_amount < nutrients["protein"]:
                warnings_list.append(warnings["protein"])
        elif num == 4:
            continue
        else:
            if nutrient_amount > nutrients[list(nutrients.keys())[num]]:
                warnings_list.append(warnings[list(warnings.keys())[num]])
    if "palm oil" in record[10].lower():
        warnings_list.append("Contains palm oil")
    return warnings_list


@app.route("/productsearch", methods=("GET", "POST"))
@app.route("/", methods=("GET", "POST"))
@app.route("/home", methods=("GET", "POST"))
@app.route("/index", methods=("GET", "POST"))
def productsearch():
    if request.args.get("show_results") == "Yes":
        return render_template(
            "index.html",
            products=products,
            product_ids=product_ids,
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
            product_ids.clear()
            for num, row in enumerate(result):
                products.append(row[1])
                product_ids.append(row[0])
            return redirect(url_for("productsearch", show_results="Yes"))
        else:
            flash("No results found")
            return redirect(url_for("productsearch"))
    else:
        return redirect(url_for("productsearch"))


@app.route("/product", methods=("GET", "POST"))
def product_detail():
    if request.method == "POST":
        product_id = request.form["product_id"]
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

            # try:
            #     health_score=health_score(result)
            # except:
            #     health_score="No health score available"
            try:
                warning_list = unhealthy_amount(result)
            except:
                warning_list = ["No warnings avaliable"]
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
                warning_list=warning_list,
                health_score=health_score(result),
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
            for row in result2:
                comp_products2.append(row[1])
            return redirect(url_for("comparison_search", show_results="Yes"))
        else:
            flash("No results found")
            return redirect(url_for("comparison_search"))
    else:
        return redirect(url_for("comparison_search"))


@app.route("/productcomp", methods=("GET", "POST"))
def product_comparison():
    if request.method == "POST":

        def compare_results(product1_result, product2_result):
            product1_best = []
            product2_best = []
            nutrients = {
                "kj": "Less",
                "protein": "More",
                "total fat": "Less",
                "saturated fat": "Less",
                "carbohydrates": "Less",
                "sugar": "Less",
                "sodium": "Less",
            }
            for num, nutrient in enumerate(product1_result[3:-1]):
                match nutrient:
                    case _ if nutrient > product2_result[num + 3]:
                        product2_best.append(
                            f"{list(nutrients.values())[num]} {list(nutrients.keys())[num]} per 100g than {product1_result[1]}"
                        )
                    case _ if nutrient < product2_result[num + 3]:
                        product1_best.append(
                            f"{list(nutrients.values())[num]} {list(nutrients.keys())[num]} per 100g than {product2_result[1]}"
                        )
            return product1_best, product2_best

        product_id = com_original_results[int(request.form["product1_id"])][0]
        opened_file.write(f"""{int(request.form["product1_id"])}\n""")
        product_id2 = com_original_results2[int(request.form["product2_id"])][0]
        opened_file.write(f"""{int(request.form["product2_id"])}\n""")
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
        if result1 and result2:

            def format_result(result_var, text):
                if (result_var == None) | (result_var == "None") | (result_var == ""):
                    return text
                return result_var

            product_positive_list, product2_positive_list = compare_results(result1, result2)
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
                warning_list=unhealthy_amount(result1),
                product_positive_list=product_positive_list,
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
                warning_list2=unhealthy_amount(result2),
                product2_positive_list=product2_positive_list,
            )
        else:
            flash("No product found")
            return redirect(url_for("productsearch"))
    else:
        return redirect(url_for("comparison_search"))


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
