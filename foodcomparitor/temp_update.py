import sqlite3

con = sqlite3.connect("foodcompare.db")
cur = con.cursor()
cur.execute(
    "UPDATE product SET product_name=?, description=?, kj=?, protein=?, total_fat=?, saturated_fat=?, carbohydrates=?, sugar=?, sodium=?, ingredients=? WHERE product_url = ?",
    (
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
        response.url,
    ),
)
con.commit()
con.close()
