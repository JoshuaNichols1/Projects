# using the openfoodfacts api
# import openfoodfacts

# api = openfoodfacts.API()
# search_term = input("Please enter the name of the item you want to search for: ")
# result = api.product.text_search("Bar")
# products = result["products"]
# for num, product in enumerate(products):
#     if num == 20:
#         break
#     if product["product_name"]:
#         print(f"""{num+1}: {product["product_name"]}""")
import requests


def search_product(product_name):
    # Open Food Facts API endpoint for product search
    api_url = "https://world.openfoodfacts.org/cgi/search.pl"

    # Parameters for the search query
    params = {
        "action": "process",
        "search_terms2": product_name,
        "json": "1",
    }

    # Make the request to the API
    response = requests.get(api_url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()

        # Check if products were found
        if data["count"] > 0:
            # Get a list of product names from the search results
            product_options = []
            for product in data["products"]:
                if product["product_name"] not in product_options:
                    if (
                        (product["product_name"] == "")
                        | (product["product_name"] == None)
                        | (product["product_name"] == " ")
                    ):
                        continue
                    product_options.append(product["product_name"])
            # Display the list of options to the user
            print("Found products:")
            for i, option in enumerate(product_options, start=1):
                print(f"{i}. {option}")

            # Ask the user to select a product
            selected_option = (
                int(input("Enter the number corresponding to the desired product: ")) - 1
            )

            # Check if the selected option is within the valid range
            if 0 <= selected_option < len(product_options):
                selected_product_name = product_options[selected_option]
                selected_product = next(
                    product
                    for product in data["products"]
                    if product["product_name"] == selected_product_name
                )

                # Check if NutriScore information is available
                if "nutrition_grades_tags" in selected_product:
                    try:
                        nutri_score = selected_product["nutriscore_data"]["score"]
                        return f"The NutriScore for {selected_product_name} is: {nutri_score}/100"
                    except:
                        nutri_score = selected_product["nutriscore_grade"][0]
                        if nutri_score == "unknown":
                            return (
                                f"NutriScore information not available for {selected_product_name}"
                            )
                        return f"The NutriScore for {selected_product_name} is: {nutri_score}"
                else:
                    return f"NutriScore information not available for {selected_product_name}"
            else:
                return "Invalid selection. Please enter a valid number."
        else:
            return f"No products found for {product_name}"
    else:
        return f"Error {response.status_code}: Unable to retrieve data"


# Take user input for the product name
product_name_input = input("Enter the product name for search: ")

# Perform the product search and retrieve NutriScore
result = search_product(product_name_input)
print(result)


# # Example usage
# product_name = "your_product_name"
# result = search_product(product_name)
# print(result)


# choice = input("Please enter the number of the item you want to view: ")
# while not (choice.isdigit() & 0 < int(choice) < 20):
#     choice = input("Please enter the number of the item you want to view: ")
# product = products[int(choice) - 1]
# print(product["nutriscore_data"]["score"])
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
