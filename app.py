from flask import Flask, render_template, request, redirect
import requests
import json
import pandas as pd

from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, RangeTool, HoverTool, CrosshairTool
from bokeh.layouts import column
from bokeh.io import show
from bokeh.embed import components
from bokeh.resources import CDN

app = Flask(__name__)
# api_key = U1XTGOBRHDKLZ1G4


def bokeh_plot(df):
    dates = df['Date']
    source = ColumnDataSource(data={
        'date': dates,
        'close': df['Adj_Close'],
        'high': df['High'],
        'low': df['Low'],
        'volume': df['Adj_Volume']
    })

    p = figure(title="Drag to change range", plot_height=300, plot_width=700, tools="xpan", toolbar_location=None,
               x_axis_type="datetime", x_axis_location="below", sizing_mode="scale_width",
               background_fill_color="#f5f5f5", x_range=(dates[len(dates)-300], dates[len(dates)-1]))

    hover_tool = HoverTool(
        tooltips=[
            ('Date',   '@date{%F}'),  # use @{ } for field names with spaces
            ('Close',  '$@close{%0.2f}'),
            ('High',   '$@high{%0.2f}'),
            ('Low',    '$@low{%0.2f}'),
            ('Volume', '@volume{0.00 a}'),
        ],

        formatters={
            'date': 'datetime',  # use 'datetime' formatter for 'date' field
            'close': 'printf',   # use 'printf' formatter for 'adj close' field
            'high': 'printf',
            'low': 'printf'
            # use default 'numeral' formatter for other fields
        },

        # display a tooltip whenever the cursor is vertically in line with a glyph
        mode='vline'
    )
    # cross_tool = CrosshairTool()

    p.add_tools(hover_tool)

    p.line('date', 'close', source=source)
    p.yaxis.axis_label = 'Price'

    select = figure(title="Drag to change the range",
                    plot_height=130, plot_width=930, y_range=p.y_range,
                    x_axis_type="datetime", y_axis_type=None, sizing_mode="scale_width",
                    tools="", toolbar_location=None, background_fill_color="#f5f5f5")

    range_tool = RangeTool(x_range=p.x_range)
    range_tool.overlay.fill_color = "navy"
    range_tool.overlay.fill_alpha = 0.2

    select.line('date', 'close', source=source)
    select.ygrid.grid_line_color = "white"
    select.add_tools(range_tool)
    select.toolbar.active_multi = range_tool

    c = column(p, select)
    script, div = components(p)

    return script, div


@app.route('/', methods=['GET'])
def index():
    # if request.method == 'GET':
    #     ticker = defualt_ticker
    # else:
    #     ticker = request.form['ticker']
    #     app.logger.info("ticker is {}".format(ticker))
    return render_template('index.html')


@app.route('/graph', methods=['POST'])
def graph():
    ticker = request.form['ticker']
    url = "https://www.quandl.com/api/v3/datasets/EOD/{}.json?api_key=zrKPeqnLPwRc8HSyEjhG".format(
        str(ticker).upper())
    response = requests.get(url)

    if response.status_code == 200:
        # with open(ticker.upper()+".json", 'w') as output:
        #     json.dump(response.json(), output)
        # message = "some info about ticker {}".format(ticker)
        data = response.json()['dataset']
        df = pd.DataFrame(data['data'], columns=data['column_names'])
        df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
        df = df.sort_values(by=['Date'], ascending=True).reset_index(drop=True)

        script, div = bokeh_plot(df)
        # return json.dumps(json_item(plot, "plot"))

        message = ticker.upper()
        app.logger.info(div)
        return render_template('index.html', msg=message, script=script, div=div)

    elif response.status_code == 403:
        message = "Sorry, this ticker is not yet supported. Please try another one."
        return render_template('index.html', msg=message)

    else:
        message = "Invalid ticker! Please try another one."
        return render_template('index.html', msg=message)


if __name__ == '__main__':
    app.run(debug=True)
