import requests
import pandas as pd
import bokeh
from bokeh.layouts import column, widgetbox
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from bokeh.models.widgets import Button, TextInput
from bokeh.io import curdoc
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def getData (ticker, year, price):
	datestart = '%d-01-01' %year
	dateend = '%d-12-31' %year
	response = requests.get('https://www.quandl.com/api/v3/datatables/WIKI/Prices.json?ticker=%s&date.gte=%s&date.lte=%s&qopts.columns=ticker,date,%s&api_key=oGPHaajGy6WuHobANi6p' %(ticker,datestart,dateend,price))
	return response

def processData (ticker, year, price):
	r = getData(ticker, year, price)
	df = pd.DataFrame(r.json()['datatable']['data'])
	df.columns = pd.DataFrame(r.json()['datatable']['columns'])['name']
	df.set_index(pd.DatetimeIndex(df['date']), inplace=True)
	return df

def makePlot (df, ticker, year, price):
	p = figure(x_axis_type="datetime", title="Quandl WIKI Stock Data - %d" %year)
	p.grid.grid_line_alpha=2.0
	p.xaxis.axis_label = 'Date'
	p.yaxis.axis_label = 'Price (USD)'
	p.line(df.index,df[price], color='#0000FF', legend='%s: %s' %(ticker,price))
	p.legend.location = "top_left"
	script, div = components(p)
	return script, div

@app.route('/', methods=['GET','POST'])
def index():
	return render_template('index.html')

@app.route('/graph', methods=['POST'])
def graph():
	ticker, year, price = request.form['tickerInput'].upper(), int(request.form['yearInput']), request.form['priceInput']
	df = processData(ticker, year, price)

	if df.empty:
		err = 'Uhoh! Something went wrong...'
		return render_template('index.html', err=err)#redirect(url_for('index.html', err=err))

	else:
		#script, div = makePlot(df, app.vars['ticker'], app.vars['year'])
		script, div = makePlot(df, ticker, year, price)
		return render_template('graph.html', div = div, script = script)

if __name__ == '__main__':
	app.run(port=33507)

