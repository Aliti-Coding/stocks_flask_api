from flask import Flask, render_template, request, jsonify
from news_api import NewsAPI
from alphavantage_api import StockAPI
from collections import OrderedDict

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/news")
def news():
    ticker = request.args.get("ticker").lower()
    print(ticker)

    apicall = NewsAPI(ticker)
    get_data = apicall.api_call()
    print(len(get_data))
    if len(get_data) > 0:
            
    
        
        # in order to maintain the order of dictionary we use the code under
        # ordered_result = OrderedDict(get_data)

        status_dict = {200: "ok"}
        result_dict = {"result": get_data}
    

        response_dict = {"response": status_dict}
        response_dict.update(result_dict)


        return jsonify(response_dict)
    else: 
        return jsonify(Error={404: "Could not find news for that tickersymbol"})

@app.route("/stock")    
def stocks():
    ticker = request.args.get("ticker").lower()
    print(ticker)

    apicall = StockAPI(ticker)
    get_data = apicall.get_data()

    return jsonify(get_data)

if __name__ == "__main__":
    app.run(debug=True)