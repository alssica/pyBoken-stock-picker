import requests
import json

api_key = "zrKPeqnLPwRc8HSyEjhG"
end_pt = "https://www.quandl.com/api/v3/datasets/EOD/"
# https://www.quandl.com/api/v3/datasets/EOD/AAPL.csv?api_key=zrKPeqnLPwRc8HSyEjhG

response = requests.get("https://www.quandl.com/api/v3/datasets/EOD/AAPL.json?api_key=zrKPeqnLPwRc8HSyEjhG")
# print(response.headers.get('Content-Type'))
with open("aapl.json", 'w') as output:
    json.dump(response.json(), output)
