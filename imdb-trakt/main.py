from __future__ import absolute_import, division, print_function
from trakt import Trakt

import json
import os
import six
import requests
import random
from flask import Flask, request, redirect, url_for, render_template


# def authenticate():
#     authorization = os.environ.get("AUTHORIZATION")

#     if authorization:
#         return json.loads(authorization)

#     print(
#         "Navigate to: %s"
#         % Trakt["oauth"].authorize_url("urn:ietf:wg:oauth:2.0:oob")
#     )

#     code = six.moves.input("Authorization code:")
#     if not code:
#         exit(1)

#     authorization = Trakt["oauth"].token_exchange(
#         code, "urn:ietf:wg:oauth:2.0:oob"
#     )
#     if not authorization:
#         exit(1)

#     # print("Authorization: %r" % authorization)
#     return authorization


# films_file = open("films.txt", "w")

# Trakt.configuration.defaults.client(
#     id="f75b525803f409d605e43e7bb1fa303d557409ae61c549d4f5e6b48b41131fec",
#     secret="ba99ea4104262ec2a0202a209da504e734c9ca36f24c46d17e7aa3ae4079cf26",
# )

# Trakt.configuration.defaults.http(retry=True)

# # Authenticate
# Trakt.configuration.defaults.oauth.from_response(authenticate())

# # Fetch movie library (watched, collection, ratings)
# movies = {}

# Trakt["sync/watched"].movies(movies, exceptions=True)
# # # Trakt["sync/collection"].movies(movies, exceptions=True)

# to_write = []

# for movie in movies.values():
#     if list(movie.keys[1])[1].isdigit():
#         to_write.append(list(movie.keys[1])[1])

# films_file.write("\n".join(to_write))
# films_file.close()

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    film_ids = open("films.txt", "r").read().split("\n")

    films = []
    film_with_id = {}
    film_desc = {}
    film_year = {}
    film_rating = {}

    for i in range(5):
        res = requests.get(
            f"https://api.themoviedb.org/3/discover/movie?sort_by=vote_average.desc&api_key=9327f569858bf5836301107af965d5bb&page={i+1}&vote_count.gte=500"
        ).json()
        for result in res["results"]:
            if str(result["id"]) not in film_ids:
                if result["vote_average"] > 7.5:
                    films.append(result["title"])
                    film_with_id[result["title"]] = result["id"]
                    film_desc[result["title"]] = result["overview"]
                    film_year[result["title"]] = result["release_date"].split(
                        "-"
                    )[0]
                    film_rating[result["title"]] = result["vote_average"]

    choice = random.choice(films)
    videos = requests.get(
        f"https://api.themoviedb.org/3/movie/{film_with_id[choice]}/videos?api_key=9327f569858bf5836301107af965d5bb&language=en-US"
    ).json()
    videos = videos["results"]
    # trailers = [
    #     "https://www.youtube.com/watch?v=" + video["key"]
    #     for video in videos
    #     if video["type"] == "Trailer"
    # ]
    trailers = [
        "https://www.youtube.com/embed/" + video["key"]
        for video in videos
        if video["type"] == "Trailer"
    ]
    return render_template(
        "main.html",
        film_name=choice,
        film_year=film_year[choice],
        film_description=film_desc[choice],
        trailers=trailers,
        tmdb_link=f"https://www.themoviedb.org/movie/{film_with_id[choice]}",
        rating=film_rating[choice],
        int_rating=int(film_rating[choice]),
    )
    # return f"""<p>{choice} ({film_year[choice]})\n\n{film_desc[choice]}\n\nTrailers:\n{trailers}\n\nhttps://www.themoviedb.org/movie/{film_with_id[choice]}</p>"""


if __name__ == "__main__":
    app.run(debug=True)
