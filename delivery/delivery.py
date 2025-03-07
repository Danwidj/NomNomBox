from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv, dotenv_values
import psycopg2

app = Flask(__name__)

CORS(app)
load_dotenv(".env")
print(os.getenv("DATABASE_HOST"))

app.config["SQLALCHEMY_DATABASE_URI"] = (
     os.getenv("DATABASE_HOST")
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {'pool_recycle': 299}

db = SQLAlchemy(app)




class Delivery(db.Model):
    __tablename__ = "delivery"


    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, nullable=False)
    start_time = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    end_time = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    location = db.Column(db.Text, nullable=False)



    def __init__(self, id, order_id, start_time, end_time, location):
        self.id = id
        self.order_id = order_id
        self.start_time = start_time
        self.end_time = end_time
        self.location = location


    def json(self):
        return {
            "id": self.id,
            "order_id": self.order_id,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "location": self.location,
        }


@app.route("/delivery")
def get_all():
    delivery_list = db.session.scalars(db.select(Delivery)).all()

    if len(delivery_list):
        return jsonify(
            {
                "code": 200,
                "data": {"deliveries": [delivery.json() for delivery in delivery_list]},
            }
        )
    return jsonify({"code": 404, "message": "There are no deliveries."}), 404


# @app.route("/book/<string:isbn13>")
# def find_by_isbn13(isbn13):
#     book = db.session.scalar(db.select(Book).filter_by(isbn13=isbn13))

#     if book:
#         return jsonify({"code": 200, "data": book.json()})
#     return jsonify({"code": 404, "message": "Book not found."}), 404


# @app.route("/book/<string:isbn13>", methods=["POST"])
# def create_book(isbn13):
#     if db.session.scalar(db.select(Book).filter_by(isbn13=isbn13)):
#         return (
#             jsonify(
#                 {
#                     "code": 400,
#                     "data": {"isbn13": isbn13},
#                     "message": "Book already exists.",
#                 }
#             ),
#             400,
#         )

#     data = request.get_json()
#     book = Book(isbn13, **data)

#     try:
#         db.session.add(book)
#         db.session.commit()
#     except Exception as e:
#         print("Exception:{}".format(str(e)))
#         return (
#             jsonify(
#                 {
#                     "code": 500,
#                     "data": {"isbn13": isbn13},
#                     "message": "An error occurred creating the book.",
#                 }
#             ),
#             500,
#         )

#     return jsonify({"code": 201, "data": book.json()}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
