
from flask import Flask, jsonify, render_template
import pandas as pd
import os

from flask import jsonify
import altair as alt
from altair import datum


app = Flask(__name__)

APP_FOLDER = os.path.dirname(os.path.realpath(__file__))

@app.route('/')
def w209():
    file = 'about9.jpg'
    return render_template('w209.html', file=file)

# Route to serve the D3 example page
@app.route('/map')
def map():
    return render_template('map.html')


# Dynamic data endpoint for D3
@app.route("/getData/<int:year>")
def getData(year):
    revenue = pd.read_csv(os.path.join(APP_FOLDER, "static/data/1_Revenues.csv"))
    if year < 1942 or year > 2008:
        return "Error in the year range"
    filteredRevenue = revenue[revenue['Year4'] == year][["Name", "Year4", "Total Revenue", "Population (000)"]]
    return filteredRevenue.to_json(orient='records')




@app.route("/altair-chart")
def altair_chart():

    df_global = pd.read_csv(os.path.join(APP_FOLDER, "static/data/players_20.csv"))
    df = df_global

    output = df.groupby("nationality")\
        .agg(num_players=("nationality", "count"),
             avr_age=("age", "mean"))\
        .reset_index()

    min_age = output["avr_age"].min()
    max_age = output["avr_age"].max()

    top5 = (
        output.sort_values("num_players", ascending=False)
        .head(5)["nationality"]
        .tolist()
    )

    output['isTop5'] = output['nationality'].isin(top5)

    color_scale = alt.Scale(
        domain=list(output["nationality"].unique()),
        scheme="tableau10"
    )

    # MAIN CHART
    main = alt.Chart(output).mark_circle().encode(
        x=alt.X('avr_age:Q',
                title='Average Age',
                scale=alt.Scale(domain=[min_age - 2, max_age + 2])),

        y=alt.Y('num_players:Q', title='Number of Players'),

        size=alt.Size('num_players:Q',
                      scale=alt.Scale(range=[20, 300])),

        color=alt.Color(
            'nationality:N',
            scale=color_scale,
            legend=None
        ),

        stroke=alt.condition(
            alt.datum.isTop5,
            alt.value('black'),
            alt.value(None)
        ),

        strokeWidth=alt.condition(
            alt.datum.isTop5,
            alt.value(1.5),
            alt.value(0)
        ),

        tooltip=["nationality", "num_players", "avr_age"]
    ).properties(width=400, height=400)

    # LEGEND
    legend_order = top5

    legend = alt.Chart(output).transform_filter(
        alt.datum.isTop5
    ).mark_point(size=120, filled=True, stroke='black').encode(
        y=alt.Y('nationality:N',
                sort=legend_order,
                axis=alt.Axis(title="Top 5 Countries")),
        color=alt.Color('nationality:N',
                        scale=color_scale,
                        legend=None)
    )

    final_chart = alt.hconcat(main, legend).configure_view(stroke=None)

    return jsonify(final_chart.to_dict())



@app.route('/altair')
def altair_page():
    return render_template('altair.html')

@app.route('/api')
def api():
    #retun a json respones with the key 'x' and integer value 
    return {"x": 20}#jsonify({"x": 15})


if __name__ == '__main__':
    app.run()
