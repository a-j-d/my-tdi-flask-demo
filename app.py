import sys
import os
from flask import Flask, render_template, request, redirect
import requests
import datetime as dt
from datetime import timedelta 

app = Flask(__name__)

app.vars={}

@app.route('/')
def main():
    print 'function main() was accessed'; sys.stdout.flush();
    return redirect('/index')

@app.route('/index',methods=['GET'])
def index_get():
    if request.method == 'GET':
        print 'function index_get() was accessed'
        sys.stdout.flush()
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
        print (app.vars['checkboxes']); sys.stdout.flush();
    
    return redirect('/plot_data')


@app.route('/plot_data', methods=['GET','POST'])
def plot_data():
    if request.method == 'GET':
        print( 'nothing to do, request was get' ); sys.stdout.flush();
        # make & show plot
            # get data from quandl
        """
        today = dt.date.today().isoformat()
        from_date = today - timedelta(days=31)
        request_args = {'':'', 'start_date':from_date, 'end_date':today, 'collapse':'daily', 'api_key':'8nDck7hx1ivMZH1LpRKg'}
        d = requests.get("https://www.quandl.com/api/v3/datasets/WIKI/" + app.vars['stock_name']+".json",data=request_args)
        #d = requests.get("https://www.quandl.com/api/v3/datasets/WIKI/FB.json?column_index=4&start_date=from_date&end_date=today&collapse=daily&api_key=8nDck7hx1ivMZH1LpRKg")
        
        """
            # load data into a bokeh plot
        """
        
        from bokeh.embed import components
        from bokeh.plotting import figure
        from bokeh.resources import INLINE
        from bokeh.util.string import encode_utf8
        fig = figure(x_axis_type="datetime", width=800,height=350)
        # add the data
        for i in range(len(app.vars['checkboxes'])):
            key = app.vars['checkboxes'][i]
            fig.line(legend=key,color=colors[i])
        fig.title.text=""
        fig.legend.location="top_left"
        fig.xaxis.axis_label="Date"
        fig.yaxis.axis_label="Price"
        
        js_resources = INLINE.render_js()
        css_resources = INLINE.render_css()
        
        script,div = components(fig)
        html = render_template('', plot_script=scrip, plot_div=div, js_resources=js_resources, css_resources=css_resources, color=color, _from=_from, to=to, tckname=app.vars['stock_name'],choices=app.vars['features')
        return encode_utf8(html)
        
        """
        return render_template('plot_page.html',tckname=app.vars['stock_name'])

    elif request.method == 'POST':
        #
        print ('request was post');sys.stdout.flush();
        return redirect('/index')


if __name__ == '__main__':
    print 'hi1';sys.stdout.flush()
    # app.run(host='0.0.0.0',port=33507)
    port = int(os.environ.get("PORT", 5000))
    print 'hi1';sys.stdout.flush()
    app.run(host='0.0.0.0',port=port, debug=True)
    #app.run(port=33507)
