import random

import requests
from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

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
        # Method 1.
        # dictionary = {}
        # Loop through each column in the data record
        # for column in self.__table__.columns:
        #     # Create a new dictionary entry;
        #     # where the key is the name of the column
        #     # and the value is the value of the column
        #     dictionary[column.name] = getattr(self, column.name)
        # return dictionary

        # Method 2. Altenatively use Dictionary Comprehension to do the same thing.
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


@app.route("/")
def home():
    return render_template("index.html")

""" in this route is for: If the user want to choose a random cafe from the db """
@app.route("/random", methods=['GET'])
def get_random_cafe():
    """call the db for all the cafes in the db"""
    cafes =db.session.query(Cafe).all()
    '''With random.choice to lest the system to choose randomly the cafe from the db  '''
    random_cafe = random.choice(cafes)
    return jsonify(cafe=random_cafe.to_dict())
    # return jsonify(cafe={
    #     "id": random_cafe.id,
    #     "name": random_cafe.name,
    #     "map_url": random_cafe.map_url,
    #     "img_url": random_cafe.img_url,
    #     "location": random_cafe.location,
    #     "seats": random_cafe.seats,
    #     "has_toilet": random_cafe.has_toilet,
    #     "has_wifi": random_cafe.has_wifi,
    #     "has_sockets": random_cafe.has_sockets,
    #     "can_take_calls": random_cafe.can_take_calls,
    #     "coffee_price": random_cafe.coffee_price,
    # })
## HTTP GET - Read Record
"""This one is a HTTP GET All the cafes from the db. There is not need to do 'methods=['GET'] because is intrinsic a GET
request"""
@app.route('/all')
def all_cafe():
    cafes = db.session.query(Cafe).all()
    """return all the information in the database through a list Comprehension  """
    return jsonify(cafes=[cafe.to_dict() for cafe in cafes])

"""Search cafe by location in the db"""
@app.route("/search")
def get_cafe_at_location():
    """this variable stock the entry requested in the http 'search?loc=<locationname> """
    query_location = request.args.get("loc")
    """cafe = query in the db and fiter by location(name of the column) the name of the location searched. .first() will
    output the first cafe in the db of the location requested """
    cafe = db.session.query(Cafe).filter_by(location=query_location).first()
    if cafe:
        """if the location requested is in the db the output will be in json format as a dict"""
        return jsonify(cafe=cafe.to_dict())
    else:
        """if the location requested is not in the db the output will be the error message"""
        return jsonify(error={"Not Found": "Sorry, we don't have a cafe at that location."})
## HTTP POST - Create Record
@app.route('/add', methods=['POST'])
def post_new_cafe():
    new_cafe= Cafe(
        name = request.form.get('name'),
        map_url = request.form.get('map_url'),
        img_url = request.form.get('img_url'),
        location = request.form.get('location'),
        seats = request.form.get('seats'),
        has_toilet = bool(request.form.get('toilet')),
        has_wifi = bool(request.form.get('wifi')),
        has_sockets = bool(request.form.get('sockets')),
        can_take_calls = bool(request.form.get('calls')),
        coffee_price = request.form.get('coffee_price'))
    db.session.add(new_cafe)
    db.session.commit()
    return jsonify(response={"success":"Successfully added the new cafe."})

## HTTP PUT/PATCH - Update Record
"""Update coffee price using PATCH """
@app.route('/update-price/<int:cafe_id>', methods=['PATCH'])
def update_coffee_price(cafe_id):
    """<cafe_id> is a GET from the user. That id will be searched in the db and once it is located. it will go to
     where is the 'coffee_price' column of that cafe and modify the value (the price) the Key and Value are donne in
      Postman. URL e.g: http://127.0.0.1:5000/update-price/22?new_price=$4"""
    # Patch the Value
    new_price = request.args.get("new_price")
    #get the id
    cafe = db.session.query(Cafe).get(cafe_id)
    # if cafe id exist in the db.
    if cafe:
        #in the db cafe_id.the column coffee_price of that cafe = the new_price
        cafe.coffee_price = new_price
        #sent modification to the db
        db.session.commit()
        return jsonify(response={"success":"Successfully updated the price."})
    else:
        return jsonify(error={"NOT FOUND":"Sorry a cafe with that id was not found in the database."})

## HTTP DELETE - Delete Record
"""Delete cafe by add a security feature by requiring an api-key . If the api-key "TopSecretAPIKey" then 
allowed to make the delete request, otherwise, tell  no authorized to make that request. A 403 in HTTP ."""
@app.route('/report-closed/<int:cafe_id>', methods=['DELETE'])
def delete_cafe(cafe_id):
    #DELETE request
    api_key = request.args.get('api_key')
    #Cheching the value of api_key
    if api_key== 'TopSecretToken':
        # fetch cafe via the cafe_id
        cafe_to_delete = db.session.query(Cafe).get(cafe_id)
        # if id exist in the db, proceed to delete the cafe from the db.
        if cafe_to_delete:
            db.session.delete(cafe_to_delete)
            db.session.commit()
            return jsonify(response={'Success 200':'Cafe  deleted!'})
        else:
            return jsonify(error={'Error 404 ': "Sorry, the coffe_id does'nt exist"})
    else:
        return jsonify(error={'Error 403 ':"Sorry, that's not allowed. Make sure you have the correct API_KEY" })


if __name__ == '__main__':
    app.run(debug=True)
