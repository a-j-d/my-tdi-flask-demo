import os
from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

app.vars={}

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index',methods=['GET'])
def index_get():
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/index',methods=['POST'])
def index_post():
    """
    If submission made then
     - collect stock ticker name (global var)
     - collect categories of data to retrieve for ticker (global vars)
     redirect to page which displays sthis data
    """
    # check below that method is POST (i.e. user input submitted)
    if request.method == 'POST':
        # collect ticker and checkbox data
        app.vars['stock_name'] = request.form('ticker')
        #app.vars['stock_name'] = 'dummy_ticker_name'
        app.vars['checkboxes'] = request.form('features')
        print (app.vars['checkboxes'])
    
    return redirect('/plot_data')


@app.route('/plot_data', methods=['GET','POST'])
def plot_data():
    if request.method == 'GET':
        print( 'nothing to do, request was get' )
        # return render_template('plot_page.html',tckname=app.vars['stock_name'])
    elif request.method == 'POST':
        #
        print ('request was post')
        
        return render_template('plot_page.html',tckname=app.vars['stock_name'])


if __name__ == '__main__':
    # app.run(host='0.0.0.0',port=33507)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0',port=33057, debug=True)