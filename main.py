from flask import Flask, render_template, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,SubmitField
from wtforms.validators import DataRequired,URL
from flask_sqlalchemy import SQLAlchemy
import csv


app = Flask(__name__)
app.config['SECRET_KEY'] = 'xfTZeHAsMP6hM@&!X9V$xM2hJ*AW9'
Bootstrap(app)

class AddForm(FlaskForm):
    cafe = StringField("NAME",validators=[DataRequired()])
    location = StringField("Cafe Location",validators=[DataRequired(),URL()])
    rating = SelectField("Coffee Ratings",choices=["☕️","☕☕","☕☕☕","☕☕☕☕","☕☕☕☕☕"],validators=[DataRequired()])
    wifi = SelectField("WIFI strength",choices=["✘","💪","💪💪","💪💪💪","💪💪💪💪","💪💪💪💪💪"],validators=[DataRequired()])
    plugs = SelectField("Power Plugs",choices=["✘","🔌","🔌🔌","🔌🔌🔌","🔌🔌🔌🔌","🔌🔌🔌🔌🔌"],validators=[DataRequired()])
    submit = SubmitField("ADD")
# columns = ["#Number", "Cofe Name", "WiFi power", "Power Plugs"]
# values = ["1", "maxine_coffees", "💪💪💪💪", "🔌🔌🔌🔌"]
# # with open("data.csv", "a", encoding='UTF8',newline="") as data:
# #     writer = csv.writer(data)
# #     writer.writerow(values)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/cafes")
def cafes():
    with open("data.csv",encoding="UTF-8") as data_file:
        cafe_data = csv.reader(data_file)
        cafe_row_list = []
        for row in cafe_data:
            cafe_row_list.append(row)
    return render_template("cafes.html",cafes=cafe_row_list)

@app.route("/add_cofe",methods=["GET","POST"])
def add():
    form = AddForm()
    if form.validate_on_submit():
        with open("data.csv","a",encoding="UTF-8") as data_file:
            data_file.write(f"\n{form.cafe.data},"
                            f"{form.location.data},"
                            f"{form.rating.data},"
                            f"{form.wifi.data},"
                            f"{form.plugs.data}")
        return redirect("cafes")
    return render_template("add.html",form=form)


if __name__ == "__main__":
    app.run(debug=True)