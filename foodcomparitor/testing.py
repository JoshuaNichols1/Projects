# using the openfoodfacts api
import openfoodfacts

api = openfoodfacts.API(user_agent="testing/1.0")
# search_term = input("Please enter the name of the item you want to search for: ")
result = api.product.text_search("Bar")
products = result["products"]
for num, product in enumerate(products):
    if num == 20:
        break
    if product["product_name"]:
        print(f"""{num+1}: {product["product_name"]}""")

choice = input("Please enter the number of the item you want to view: ")
while not (choice.isdigit() & 0 < int(choice) < 20):
    choice = input("Please enter the number of the item you want to view: ")
product = products[int(choice) - 1]
print(product["nutriscore_data"])
print("Product details:")
print(f"""Name: {product["product_name"]}""")
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
