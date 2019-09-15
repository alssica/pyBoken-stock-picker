# Stock Lookup [Flask x Bokeh]

This is a simple stock lookup tool that displays the historic daily closing price of your ticker of choice.
Deployed on Heroku [here][https://pyboken-stock-picker.herokuapp.com/] if you want to play with it.

This repo contains the code that can reproduce this app ready for Heroku deployment.

### The virtual environment
- This repo uses `pipenv` to manage its virtual environment. All dependencies are stored in the `Pipfile` and `Pipfile.lock`. 
They can be used by Heroku directly, but if you prefer the good old requirement.txt file, you can generate it by using the `pipenv lock -r` command.
- The `Procfile` contains settings to be used by Heroku.
- There is some boilerplate HTML in `templates/`

### The data
- Data for the stock information are pulled from Quandl's [End of Day US Stock Prices][https://www.quandl.com/data/EOD-End-of-Day-US-Stock-Prices]. 
The free tier account can only access a small sample of the entire database, so not all tickers are available.
- The app will parse the json file obtained from Quandl's api and turn the json file into pandas dataframe for further analysis.

### The app
- The app is built with Bokeh, a python library that provides interactive plots and graphs. It enables many abilities such as hover-over tool tips, drag and zoom, and etc. without having to write javascript.

### Next steps / TODO
- 1. Explore other free libraries that have a larger inclusion of stocks
- 2. Autocomplete
- 3. Zoom ability on different time frame (1D, 1M, 1Y, 5Y, Max)

