import openfoodfacts
import scrapy
import sqlite3

con = sqlite3.connect("foodcompare.db")
cur = con.cursor()

api = openfoodfacts.API()


def format_result(text):
    return " ".join(text[3:].split("_"))


search_term = input("Enter a product name: ")
while not search_term:
    search_term = input("Enter a product name: ")
result = cur.execute("SELECT * FROM product WHERE product_name LIKE ?", (f"%{search_term}%",))
result = result.fetchall()
if result:
    for num, row in enumerate(result):
        print(f"{num+1}: {row[1]}")
    choice = input("Please enter the number of the item you want to view: ")
    while not (choice.isdigit() & 0 < int(choice) <= len(result)):
        choice = input("Please enter the number of the item you want to view: ")
    product = result[int(choice) - 1]
    print("\nProduct details:")
    print(f"""\nName: {product[1]}""")
    print(f"""\nDescription: {product[2]}""")
    print(f"""\nEnergy (KJ): {product[3]}""")
    print(f"""\nProtein: {product[4]}""")
    print(f"""\nTotal Fat: {product[5]}""")
    print(f"""  - Saturated Fats: {product[6]}""")
    print(f"""\nCarbohydrates: {product[7]}""")
    print(f"""  - Sugar: {product[8]}""")
    print(f"""\nSodium: {product[9]}""")
    print(f"""\nIngredients: {product[10]}""")
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
