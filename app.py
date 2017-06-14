import os
from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)

app.vars={}

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index')
def index_get():
    if request.method == 'GET':
        return render_template('index.html')

@app.route('/index')
def index_post():
    if request.method == 'POST':
        #app.vars['stock_name'] = request.form('ticker')
        app.vars['stock_name'] = 'dummy_ticker_name'
        
    return render_template('plot_page.html',tckname=app.vars['stock_name'])

if __name__ == '__main__':
    # app.run(host='0.0.0.0',port=33507)
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0',port=33057)