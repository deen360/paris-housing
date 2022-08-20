# we import flask

from flask import Flask, jsonify, redirect, render_template, request, session
import pickle
import pymongo
from pymongo import MongoClient


cluster = MongoClient(
    "mongodb+srv://deen360:1_Jackson5@cluster0.zyfi4dh.mongodb.net/?retryWrites=true&w=majority")

# name of database
db = cluster["flask"]

# name of collection
collection = db["parisprediction"]


app = Flask(__name__)


with open('model-lin.b', 'rb') as f_in:
    (dv, model) = pickle.load(f_in)


# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/predict/", methods=["GET", "POST"])
def predict():
    if request.method == "POST":

        #: takes the user entry
        if not request.form.get("squaremeter"):
            return render_template("index.html")

        else:
            size = request.form.get("squaremeter")
            size = int(size)
            house = {"squareMeters": size}
            features = {}
            features['squareMeters'] = house['squareMeters']
            X = dv.transform(features)
            preds = model.predict(X)
            result = {'House price': preds}
            price = "{:,}".format(round(result['House price'][0]))
            sizes = house["squareMeters"]
            data = {"squareMeters": size, 'House price': price}
            database = collection.insert_one(data)
            return render_template("index.html", prices=price, sizes=sizes)

    else:

        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
