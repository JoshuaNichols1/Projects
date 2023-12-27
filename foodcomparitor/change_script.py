import sqlite3
import re
import requests

with open(
    "E:\Coding\Projects\\foodcomparitor\ietf_scraper\spiders\\health_scores.txt", "w"
) as opened_file:

    def update_product_urls(test_mode=False):
        # Connect to the SQLite database
        con = sqlite3.connect(
            "E:\Coding\Projects\\foodcomparitor\ietf_scraper\spiders\\foodcompare.db"
        )
        cursor = con.cursor()

        # Fetch all product URLs
        cursor.execute("SELECT product_url FROM product2")
        products = cursor.fetchall()

        # Compile the regex pattern outside of the loop
        pattern = re.compile(r"(\d+)$")

        # Update each product URL
        for product in products:
            url = product[0]
            match = pattern.search(url)
            if match:
                new_url = match.group(1)
                print(f"Updating product: {url} -> {new_url}")
                cursor.execute(
                    "UPDATE product2 SET product_url = ? WHERE product_url = ?", (new_url, url)
                )

        # Commit changes if not in test mode
        if not test_mode:
            con.commit()

        # Close the connection
        con.close()

    def health_score_alg(product_name):
        print(f"Searching for product: {product_name}")
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
                option = input("Enter the number corresponding to the desired product: ")
                if option == "n":
                    return "Stop"
                selected_product_name = product_options[int(option) - 1]
                selected_product = next(
                    product
                    for product in data["products"]
                    if product["product_name"] == selected_product_name
                )
                # Check if NutriScore information is available
                if "nutrition_grades_tags" in selected_product:
                    try:
                        nutri_score = selected_product["nutriscore_data"]["score"]
                        return f"{nutri_score:.2f}/100"
                    except:
                        try:
                            nutri_score = selected_product["nutriscore_grade"][0]
                            if nutri_score == "unknown":
                                return f"No health score available"
                            return f"{nutri_score.upper()}"
                        except:
                            return "No health score available"
                else:
                    return "No health score available"
            else:
                return "No health score available"
        else:
            return "No health score available"

    def remove_end(string):
        if string is None:
            return None
        numbers = re.findall(r"\d+\.\d+|\d+", string)
        if not numbers:
            return None
        return float("".join(numbers))

    def remove_useless_parts(product_name):
        useless_parts = [
            "Boxed",
            # "Gift Box 24 Pack",
            "Tin",
            "Gift Box",
            "Assorted Cornet",
            r"\d+ Piece Pack",
            # "Gift Box 30 Pack",
            "Share Pack",
            # "5 Pack",
            r"\d+ Pack",
            # "Gift Box 5 Pack",
            r"Gift Box \d+ Pack",
        ]
        for part in useless_parts:
            product_name = product_name.replace(part, "")
        return product_name.strip()

    con = sqlite3.connect("E:\Coding\Projects\\foodcomparitor\ietf_scraper\spiders\\foodcompare.db")
    cursor = con.cursor()
    # Fetch all product URLs
    cursor.execute("SELECT product_name, health_score FROM product")
    products = cursor.fetchall()
    for product in products:
        if product[1] == "No health score available":
            product_name = remove_useless_parts(product[0])
            if type(remove_end(" ".join(product_name.split()[-1]))) == float:
                product_name = " ".join(product_name.split()[:-1])
            health_score = health_score_alg(product_name)
            if health_score == "Stop":
                health_score = "No health score available"
            else:
                if health_score == "No health score available":
                    product_name_copy = product_name
                    while (
                        health_score == "No health score available"
                        and len(product_name_copy.split()) > 1
                    ):
                        product_name_copy = " ".join(product_name_copy.split()[1:])
                        health_score = health_score_alg(product_name_copy)
                        if health_score == "Stop":
                            health_score = "No health score available"
                            break
                if health_score == "No health score available":
                    product_name_copy = product_name
                    while (
                        health_score == "No health score available"
                        and len(product_name_copy.split()) > 1
                    ):
                        product_name_copy = " ".join(product_name_copy.split()[:-1])
                        health_score = health_score_alg(product_name_copy)
                        if health_score == "Stop":
                            health_score = "No health score available"
                            break
            opened_file.write(f"{product_name} - {health_score}\n")
            # print(f"{product_name}: {health_score}")
            # update_q = input("Update health score with choice? (y/n): ")
            # if update_q == "y":
            #     con = sqlite3.connect(
            #         "E:\Coding\Projects\\foodcomparitor\ietf_scraper\spiders\\foodcompare.db"
            #     )
            #     cursor = con.cursor()
            #     cursor.execute(
            #         "UPDATE product SET health_score = ? WHERE product_name = ?",
            #         (health_score, product_name),
            #     )

    # Call the function in test mode
    # update_product_urls(test_mode=True)
