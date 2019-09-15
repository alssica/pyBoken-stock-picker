from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, RangeTool, HoverTool, CrosshairTool
from bokeh.layouts import column
from bokeh.io import show
from bokeh.embed import components
import requests
import json
import pandas as pd

api_key = "zrKPeqnLPwRc8HSyEjhG"
end_pt = "https://www.quandl.com/api/v3/datasets/EOD/"
# https://www.quandl.com/api/v3/datasets/EOD/AAPL.csv?api_key=zrKPeqnLPwRc8HSyEjhG

response = requests.get(
    "https://www.quandl.com/api/v3/datasets/EOD/AAPL.json?api_key=zrKPeqnLPwRc8HSyEjhG")
# print(response.headers.get('Content-Type'))
# with open("aapl.json", 'w') as output:
#     json.dump(response.json(), output)
data = response.json()['dataset']
df = pd.DataFrame(data['data'], columns=data['column_names'])
df['Date'] = pd.to_datetime(df['Date'], format='%Y-%m-%d')
df = df.sort_values(by=['Date'], ascending=True).reset_index(drop=True)
# print(df)
# df = df.set_index('Date')


# dates = np.array(AAPL['date'], dtype=np.datetime64)
# source = ColumnDataSource(data=dict(date=dates, close=AAPL['adj_close']))

dates = df['Date']
# source = ColumnDataSource(data=dict(date=dates, close=df['Adj_Close']))

source = ColumnDataSource(data={
    'date': dates,
    'close': df['Adj_Close'],
    'high': df['High'],
    'low': df['Low'],
    'volume': df['Adj_Volume']
})

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

p = figure(plot_height=500, plot_width=800, tools="xpan", toolbar_location=None, x_axis_type="datetime", x_axis_location="below",
           sizing_mode="scale_width", background_fill_color="#efefef", x_range=(dates[800], dates[1000]))

p.add_tools(hover_tool)

p.line('date', 'close', source=source)
p.yaxis.axis_label = 'Price'

select = figure(title="Drag the middle and edges of the selection box to change the range above",
                plot_height=130, plot_width=800, y_range=p.y_range,
                x_axis_type="datetime", y_axis_type=None,
                tools="", toolbar_location=None, background_fill_color="#efefef")

range_tool = RangeTool(x_range=p.x_range)
range_tool.overlay.fill_color = "navy"
range_tool.overlay.fill_alpha = 0.2

select.line('date', 'close', source=source)
select.ygrid.grid_line_color = "white"
select.add_tools(range_tool)
select.toolbar.active_multi = range_tool

script, div = components(p)
ids = div.split("\"")
div_id = ids[3]
data_root_id = ids[5]
print(id[5])
# show(column(p, select))
