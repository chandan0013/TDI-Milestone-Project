Welcome to my milestone project for the TDI 12-day course! This code grabs stock data from the [Quandl WIKI](https://www.quandl.com/databases/WIKIP) dataset and puts it into a pandas dataframe to be plotted via Bokeh embedding. Flask is used to tie the code to html and the app is deployed via Heroku. You can view my completed Heroku app [here](https://hasan-khan-datainc-project.herokuapp.com/). The app takes ticker, year, and various price metrics as inputs and outputs a time-series plot.

## app.py

Main python file that grabs stock data from Quandl API, plots it, and embeds to html with the help of Bokeh and Flask.

## Procfile, requirements.txt, conda-requirements.txt, and runtime.txt

Config files that mainly tell Heroku what packages to include.

## templates
Contains html files for the index (index.html) and plot (graph.html) pages.
