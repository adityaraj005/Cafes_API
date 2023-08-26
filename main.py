from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy
import random

app = Flask(__name__)

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

    def to_dict(self):
        # self.__table__.columns => this will give all the column names in the table which is stored inside our database
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

    def to_list(self):
        rows = self.query.all()
        # Get all the column names of the table in order to iterate through
        column_keys = self.__table__.columns.keys()
        # Temporary dictionary to keep the return value from table
        rows_dic_temp = {}
        rows_dic = []
        # Iterate through the returned output data set
        for row in rows:
            for col in column_keys:
                rows_dic_temp[col] = getattr(row, col)
            rows_dic.append(rows_dic_temp)
            rows_dic_temp = {}
        return rows_dic


@app.route("/")
def home():
    return render_template("index.html")


## HTTP GET - Read Record
@app.route("/random", methods=['GET'])
def get_random_cafe():

    cafes = db.session.query(Cafe).all()
    random_cafe = random.choice(cafes)
    return jsonify(cafe=random_cafe.to_dict())


@app.route("/all")
def get_all_cafe():
    all_cafes = db.session.query(Cafe).all()

    return jsonify(cafes=[cafe.to_dict() for cafe in all_cafes])


@app.route("/search")
def search_cafe():
    query_location = request.args.get("loc")
    find_cafe = Cafe.query.filter_by(location=query_location).all()
    if find_cafe:
        return jsonify(cafe=[cafe.to_dict() for cafe in find_cafe])
    else:
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})


## HTTP POST - Create Record


@app.route("/add", methods=["POST"])
def post_new_cafe():
    new_cafe = Cafe(
        name=request.form.get("name"),
        map_url=request.form.get("map_url"),
        img_url=request.form.get("img_url"),
        location=request.form.get("loc"),
        has_sockets=bool(request.form.get("sockets")),
        has_toilet=bool(request.form.get("toilet")),
        has_wifi=bool(request.form.get("wifi")),
        can_take_calls=bool(request.form.get("calls")),
        seats=request.form.get("seats"),
        coffee_price=request.form.get("coffee_price"),
    )
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success": "Successfully added the new cafe."})


## HTTP PUT/PATCH - Update Record


@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    cafe = Cafe.query.get(cafe_id)
    print(cafe.coffee_price)
    updated_price = request.args.get("new_price")

    if cafe:
        cafe.coffee_price = updated_price
        print(cafe.coffee_price)
        db.session.commit()
        return jsonify(response={"success": "Successfully updated the price."})

    else:
        return jsonify(error={"Not Found": "Sorry, a cafe with that id was not found in the database."})


## HTTP DELETE - Delete Record

@app.route("/report-closed/<cafe_id>")
def delete_cafe(cafe_id):
    api_key = request.args.get("api_key")

    if api_key == "TopSecretApiKey":
        cafe = Cafe.query.get(cafe_id)

        if cafe:
            db.session.delete(cafe)
            db.session.commit()
            return jsonify(response={"success": "Successfully deleted the cafe from the database."}), 200

        else:
            return jsonify(error={"Not Found": "Sorry a cafe with that id was not found in the database."}), 404

    else:
        return jsonify(error={"Forbidden": "Sorry, that's not allowed. Make sure you have the correct api_key."}), 403


if __name__ == '__main__':
    app.run(debug=True)
