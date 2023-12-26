import sqlite3
import re


def update_product_urls(test_mode=False):
    # Connect to the SQLite database
    con = sqlite3.connect("E:\Coding\Projects\\foodcomparitor\ietf_scraper\spiders\\foodcompare.db")
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


# Call the function in test mode
update_product_urls(test_mode=False)
