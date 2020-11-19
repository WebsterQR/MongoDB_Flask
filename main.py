from flask import Flask, render_template, request, redirect, url_for
from pymongo import *
app = Flask(__name__)
client = MongoClient('localhost', 27017)
db = client['testDB']
collection = db["series"]


@app.route('/')
def start():
    return render_template("hello.html")

@app.route('/filterdata',  methods=["GET", "POST"])
def filter():
    data = []
    if request.method == "POST":
        ID = request.form["id_search"]
        Name =request.form["name_search"]
        Description = request.form["description_search"]
        if ID != "":
            for post in db.collection.find():
                if post["id"] == ID:
                    data.append(post)
        elif Name != "":
            for post in db.collection.find():
                if post["Name"] == Name:
                    data.append(post)
        elif Description != "":
            for post in db.collection.find():
                if post["Description"] == Description:
                    data.append(post)
        return render_template("filter_id.html", data=data, length = len(data))
    else:
        return  render_template("filterdata.html")

@app.route('/getdata')
def getdata():
    print(db.collection_names())
    data = [ list(db[coll].find({})) for coll in db.collection_names() ]
    return render_template("getdata.html", data = data[0], total_records=len(data[0]), length = db.collection.find().count())

@app.route('/newdata', methods=["GET", "POST"])
def newdata():
    if request.method == "POST":
        ID = request.form["ID"]
        name = request.form["name"]
        description = request.form["description"]
        post = {
            "id": ID,
            "Name": name,
            "Description": description
        }
        db.collection.insert_one(post)
        print(db.collection.find().count())
        return redirect(url_for('getdata'))
    else:
        return render_template("newdata.html")

if __name__ == "__main__":
    app.run()