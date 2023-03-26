#!/usr/bin/python3


from flask import Flask, render_template

import random
import requests

app = Flask(__name__, template_folder="templates")

# API credentials
app_id = 
app_key = 

# Get random recipes from the API
@app.route("/")
def home():
    url = f'https://api.edamam.com/search?q=random&app_id={app_id}&app_key={app_key}&from=0&to=9'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()['hits']
    recipes = []
    for item in data:
        recipe = item['recipe']
        recipes.append(recipe)

    # Select a random subset of the results
    num_results = min(len(recipes), 10)
    random_data = random.sample(recipes, k=num_results)

    # Render the template with the random results
    return render_template("index.html", recipes=random_data)

if __name__ == "__main__":
    app.run(debug=True)
