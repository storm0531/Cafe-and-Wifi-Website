from flask import Flask, render_template, redirect, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_sqlalchemy import SQLAlchemy
import csv

# setting up flask application and it's configs
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cafes.db"
app.config['SECRET_KEY'] = 'xfTZeHAsMP6hM@&!X9V$xM2hJ*AW9'

# bounding app with databade and falsk bootstrap
db = SQLAlchemy(app)
Bootstrap(app)


# creating cafe database table using SQLALCHEMY
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cafe = db.Column(db.String, unique=True, nullable=False)
    location = db.Column(db.String, unique=True, nullable=False)
    rating = db.Column(db.String, nullable=False)
    wifi = db.Column(db.String, nullable=False)
    plugs = db.Column(db.String, nullable=False)


# creating cafe database #
with app.app_context():
    db.create_all()


# flask form for adding a cafe to database #
class AddForm(FlaskForm):
    cafe = StringField("NAME", validators=[DataRequired()])
    location = StringField("Cafe Location", validators=[DataRequired(), URL()])
    rating = SelectField("Coffee Ratings", choices=["☕️", "☕☕", "☕☕☕", "☕☕☕☕", "☕☕☕☕☕"], validators=[DataRequired()])
    wifi = SelectField("WIFI strength", choices=["✘", "💪", "💪💪", "💪💪💪", "💪💪💪💪", "💪💪💪💪💪"], validators=[DataRequired()])
    plugs = SelectField("Power Plugs", choices=["✘", "🔌", "🔌🔌", "🔌🔌🔌", "🔌🔌🔌🔌", "🔌🔌🔌🔌🔌"], validators=[DataRequired()])
    submit = SubmitField("ADD")


# rendering home page #
@app.route("/")
def home():
    return render_template("index.html")


# rendering cafes list page by getting data from database #
@app.route("/cafes")
def cafes():
    ### using csv file as storage #
    # with open("data.csv", encoding="UTF-8") as data_file:
    #     cafe_data = csv.reader(data_file)
    #     cafe_row_list = []
    #     for row in cafe_data:
    #         cafe_row_list.append(row)

    cafe_data = db.session.query(Cafe).all()
    return render_template("cafes.html", cafes=cafe_data)


# rendering a add cafe page with flask form to add to database #
@app.route("/add_cafe", methods=["GET", "POST"])
def add():
    form = AddForm()

    ### if a POST request has been send #
    if form.validate_on_submit():
        ### using csv file as data storage #
        # with open("data.csv", "a", encoding="UTF-8") as data_file:
        #     data_file.write(f"\n{form.cafe.data},"
        #                     f"{form.location.data},"
        #                     f"{form.rating.data},"
        #                     f"{form.wifi.data},"
        #                     f"{form.plugs.data}")

        ### adding to SQLITE data base #
        cafe = Cafe(cafe=form.cafe.data,
                    location=form.location.data,
                    rating=form.rating.data,
                    wifi=form.wifi.data,
                    plugs=form.plugs.data, )
        db.session.add(cafe)
        db.session.commit()

        # redirecting to cafes list page #
        return redirect("cafes")
    return render_template("add.html", form=form)


# deleting cafe from database #
@app.route("/delete")
def delete_cafe():
    cafe_id = request.args.get("id")
    cafe_to_delete = Cafe.query.get(cafe_id)
    db.session.delete(cafe_to_delete)
    db.session.commit()

    return redirect("cafes")


# running website using flask #
if __name__ == "__main__":
    app.run(debug=True)
