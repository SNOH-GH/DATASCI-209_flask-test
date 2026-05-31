
from flask import Flask, render_template
import pandas as pd
import os
app = Flask(__name__)

APP_FOLDER = os.path.dirname(os.path.realpath(__file__))

@app.route('/')
def w209():
    file = 'about9.jpg'
    return render_template('w209.html', file=file)

# Route to serve the D3 example page
@app.route('/temp')
def temp():
    return render_template('temp.html')


# # Dynamic data endpoint for D3
# @app.route("/getData/<int:year>")
# def getData(year):
#     revenue = pd.read_csv(os.path.join(APP_FOLDER, "static/data/1_Revenues.csv"))
#     if year < 1942 or year > 2008:
#         return "Error in the year range"
#     filteredRevenue = revenue[revenue['Year4'] == year][["Name", "Year4", "Total Revenue", "Population (000)"]]
#     return filteredRevenue.to_json(orient='records')

if __name__ == '__main__':
    app.run()
