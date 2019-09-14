from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

api_key = "zrKPeqnLPwRc8HSyEjhG"
end_pt = "https://www.quandl.com/api/v3/datasets/EOD/"
# https://www.quandl.com/api/v3/datasets/EOD/AAPL.csv?api_key=zrKPeqnLPwRc8HSyEjhG
response = requests.get("https://www.quandl.com/api/v3/datasets/EOD/AAPL.csv?api_key=zrKPeqnLPwRc8HSyEjhG")
print(response)

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(debug=True)
