import requests
import geocoder
import torch as pt

weather_key = "11f6f2a5f0a745b4bc323611231912"


def get_weather(location=None):
    g = geocoder.ip("me")
    longlat = ",".join(str(i) for i in g.latlng)
    url = f"""http://api.weatherapi.com/v1/current.json?key={key}&q={longlat if location is None else location}&aqi=no"""
    response = requests.get(url)
    weather_data = response.json()["current"]
    weather_condition = weather_data["condition"]["text"]
    temp = weather_data["temp_c"]


chatbot_name = "NotBot"

training_data = [
    [
        "Hi",
        "Welcome, I'm your chatbot",
    ],
    [
        "Are you a plant?",
        "No, I'm the pot below the plant!",
    ],
    [
        "What's your name?",
        f"My name is {chatbot_name}, what's yours?",
    ],
    [
        "What are you?",
        f"I'm a chatbot, my name is {chatbot_name}",
    ],
    [
        "My name is Josh",
        "Hello there, Josh",
    ],
    [
        "My name is [name]",
        "Hello there, [name]",
    ],
    ["Hello", "Hi there!"],
    ["Good morning", "Good morning!"],
    ["Good evening", "Good evening!"],
    [
        "What's up?",
        "Not much, just chilling out. What about you?",
    ],
    ["How are you?", "I'm doing well, thanks for asking! How are you today?"],
    ["Who are you?", f"I'm {chatbot_name}, your friendly chatbot companion!"],
    [
        "What can you do?",
        "I can try to answer any question you can throw at me, go head and try one out!",
    ],
    ["What are you made of?", "I'm made of code and lots of data!"],
    ["What's the weather like?", f"The weather is currently {get_weather()}"],
    ["What's the weather like in london?", f"""The weather is currently {get_weather("London")}"""],
    ["What's the news today?", "Here are some headlines..."],
    [
        "Tell me a joke",
        "Sure, here's one: Why did the scarecrow win an award? Because he was outstanding in his field! ",
    ],
    [
        "What's your favorite color?",
        "I don't have preferences like that, but I appreciate a beautiful sunset! ",
    ],
    [
        "What do you think about [topic]?",
        "That's an interesting topic! I've learned that...",
    ],
]

exit_conditions = (":q", "quit", "exit", "quit()")
while True:
    query = input("> ")
    if query in exit_conditions:
        break
    elif query != "":
        print(f"{query}")  # replace with ai's response to query
