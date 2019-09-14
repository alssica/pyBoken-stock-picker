from flask import Flask, render_template, request, redirect
import requests
import json
import logging

app = Flask(__name__)


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
        with open(ticker.upper()+".json", 'w') as output:
            json.dump(response.json(), output)
        message = "some info about ticker {}".format(ticker)
    elif response.status_code == 403:
        message = "invalid ticker! please try another one"
    return render_template('index.html', msg=message)


if __name__ == '__main__':
    app.run(debug=True)
