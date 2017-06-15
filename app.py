import sys
import os
from flask import Flask, render_template, request, redirect

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
    # check below that method is POST (i.e. user input submitted)
    print 'index_post() was accessed';sys.stdout.flush(); 
    if request.method == 'POST':
        # collect ticker and checkbox data
        app.vars['stock_name'] = request.form('ticker')
        #app.vars['stock_name'] = 'dummy_ticker_name'
        app.vars['checkboxes'] = request.form('features')
        np.savetxt('fname.txt',app.vars['checkboxes'])
    
    return redirect('/plot_data')


@app.route('/plot_data', methods=['GET','POST'])
def plot_data():
    if request.method == 'GET':
        print( 'nothing to do, plot_data request was get' ); sys.stdout.flush();
        
        return render_template('plot_page.html',tckname=app.vars['stock_name'])

    elif request.method == 'POST':
        #
        print ('request was post');sys.stdout.flush();
        return redirect('/index')
    else: 
        print ' nothing to do ';sys.stdout.flush();


if __name__ == '__main__':
    print 'hi1, i.e. in main if stmt';sys.stdout.flush()
    # app.run(host='0.0.0.0',port=33507)
    port = int(os.environ.get("PORT", 5000))
    print 'hi1, i.e. port assigned';sys.stdout.flush()
    app.run(host='0.0.0.0',port=port, debug=True)
    #app.run(port=33507)
