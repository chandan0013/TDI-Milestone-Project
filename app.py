
# coding: utf-8

import requests
import pandas as pd
import bokeh
from bokeh.layouts import column, widgetbox
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource
from bokeh.models.widgets import Button, TextInput
from bokeh.io import curdoc
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def getData (ticker, year):
    datestart = '%d-01-01' %year
    dateend = '%d-12-31' %year
    response = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/Prices.json?ticker=%s&date.gte=%s&date.lte=%s&qopts.columns=ticker,date,open,close&api_key=oGPHaajGy6WuHobANi6p' %(ticker,datestart,dateend))
    return response

#@app.route('/graph')
def displayPlot(ticker):
    year = 2017
    r = getData(ticker, year)
    df = pd.DataFrame(r.json()['datatable']['data'])
    df.columns = pd.DataFrame(r.json()['datatable']['columns'])['name']
    df.set_index(pd.DatetimeIndex(df['date']), inplace=True)
    source = ColumnDataSource(df)
    p1 = figure(x_axis_type="datetime", title="Quandl WIKI Stock Closing Prices - %d" %year)
    p1.grid.grid_line_alpha=2.0
    p1.xaxis.axis_label = 'Date'
    p1.yaxis.axis_label = 'Price'

    p1.line('date', 'close', color='#0000FF', legend='%s: Closing Price' %ticker, source = source)
    p1.legend.location = "top_left"

    #output_file("stocks.html", title="Stock Closing Proces")
    script, div = components(p1)

    return render_template('graph.html')

@app.route('/')
def input():
	ticker_input = TextInput(placeholder="AAPL", title="Ticker:")
	submit = Button(label="Submit")
	inputs = widgetbox([ticker_input, submit], width=200)
	output_file("index.html", title="Stock Closing Proces")
	show(inputs)
	submit.on_click(displayPlot('AAPL')) #ticker_input.value.strip()
	curdoc().add_root(submit)

if __name__ == '__main__':
  app.run(port=33507)

