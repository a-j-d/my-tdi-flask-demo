import sys
import os
from flask import Flask, render_template, request, redirect
import datetime as dt
import requests
import simplejson as json
import pandas as pd
import collections
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from bokeh.models.formatters import DatetimeTickFormatter

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
    print 'hi: ',request.method;sys.stdout.flush();

    if request.method == 'POST':
        # collect ticker and checkbox data
        app.vars['stock_name'] = request.form['ticker']
        print 'features: ', request.form.getlist('features'); sys.stdout.flush();
        print 'ticker: ', request.form['ticker']
        app.vars['checkboxes'] = request.form.getlist('features')
        
    return redirect('/plot_data')


@app.route('/plot_data', methods=['GET','POST'])
def plot_data():
    
    print '/plot data was accessed' ; sys.stdout.flush();

    if request.method == 'GET':
        print 'plot data method was GET' ; sys.stdout.flush();
        
        # prepare api request url
        today = dt.date.today().isoformat()
        from_date = (dt.date.today() - dt.timedelta(days=31)).isoformat()
        print 'dates are: ', today, from_date; sys.stdout.flush();
        
        ###
        #request_args = {'column_index':'4', 'exclude_column_names':'true', 'start_date':from_date, 'end_date':today, 'frequency':'daily', 'api_key':'8nDck7hx1ivMZH1LpRKg'}
        ###
        request_args = {'start_date':from_date, 'end_date':today, 'frequency':'daily', 'api_key':'8nDck7hx1ivMZH1LpRKg'}
        
        print 'request_args is: ', request_args; sys.stdout.flush();
        
        req = requests.get("https://www.quandl.com/api/v3/datasets/WIKI/" + app.vars['stock_name']+".json",data=request_args)    
        
        print 'Was request successful? ', req.status_code == requests.codes.ok
        
        if req.status_code == requests.codes.ok:
            
            # ind1 = open, ind4 = close, ind8 = ajd. open, ind11 = adj. close
            
            print( 'displaying plot..., plot_data request was get' ); sys.stdout.flush();
            
            ###
            df = pd.DataFrame(req.json())
            ###
            print "df ", df; sys.stdout.flush(); 
            
            ###
            dat = df['dataset']['data']
            
            ###
            print 'dat' , dat; sys.stdout.flush();
            print 'dat_col_names' , df['dataset']['column_names']; sys.stdout.flush();
            
            ###
            dat_col_ind = [df['dataset']['column_names'].index(elem) for elem in app.vars['checkboxes']]
            print 'dat_col_ind ', dat_col_ind ; sys.stdout.flush();

            ###
            print "dat info", type(dat), dat; sys.stdout.flush();
            
            ###
            indtoplot = []
            ###
            dattoplot = []
            
            ###
            print "dat[0] ", dat[0]
            ###
            print "dat[4] ", dat[4]
            ###
            print "dat[1] ", dat[1]
            ###
            print "dat[8] ", dat[8]
            

            ###
            for index in dat_col_ind:
                #    indtoplot.append(list(pd.to_datetime(dat[0]).values))
                ###
                indtoplot.append(list(range(len(dat[1].values))))
                ###
                dattoplot.append(list(dat[index].values))
            
            ###
            print "indtoplot ", indtoplot; sys.stdout.flush();
            ###
            print "dattoplot ", dattoplot; sys.stdout.flush();
            
            ###
            #df = pd.DataFrame(req.json())
            ###
            #print "df: ", df; sys.stdout.flush();
            
            datdic = dict(req.json()['dataset']['data'])
            ###
            #print "datdic: ", datdic; sys.stdout.flush();
            
            ordatdic = collections.OrderedDict(sorted(datdic.items()))
            ###
            #print "ordatdic: ", ordatdic ; sys.stdout.flush();
            
            ###
            #df2 = pd.DataFrame(data=ordatdic.values(), index=pd.DatetimeIndex(ordatdic.keys()), columns= ['Close'])
            ###
            #print "df2 data is: ", df2['Close']; sys.stdout.flush();
            ###
            #print "df2 index is: ", df2.index
            
            fig = figure(width=500, height=300)#, x_axis_type="datetime") 
            ###
            fig.multi_line(indtoplot, dattoplot)
            #fig.line(df2.index,df2['Close'])#,color="#2222aa",line_width=5)
            #fig.line(df2.index,df2['Close'])#,color="#2222aa",line_width=5)
            ###
            #fig.xaxis.formatter = DatetimeTickFormatter(days=["%d-%m-%y"], months=["%d-%m-%y"], years=["%d-%m-%y"])
            fig.title.text="Quandl WIKI data for '"+app.vars['stock_name']+"'"
            fig.legend.location="top_left"
            fig.xaxis.axis_label="Date"
            fig.yaxis.axis_label="Price"
            
            js_resources = INLINE.render_js()
            css_resources = INLINE.render_css()
            
            script, div = components(fig)
            
            #html = render_template('embed.html', plot_script=script, plot_div=div, js_resources=js_resources, css_resources=css_resources, color=color, _from=from_date, to=today)#, tckname=app.vars['stock_name'],pricestring=", ".join(app.vars['checkboxes']))
            html = render_template('plot_page.html', plot_script=script, plot_div=div, js_resources=js_resources, css_resources=css_resources)#, tckname=app.vars['stock_name'],pricestring=", ".join(app.vars['checkboxes']))
            return encode_utf8(html)
            #return render_template('plot_page.html')
            
            # display error below otherwise
        else:
            return render_template('key_error.html')
            
    elif request.method == 'POST':
        #
        print ('plot data request was post');sys.stdout.flush();
        return redirect('/index')
    else: 
        print ' /plot_data request was neither GET nor POST ';sys.stdout.flush();


if __name__ == '__main__':
    print 'hi1, i.e. in main if stmt';sys.stdout.flush()

    port = int(os.environ.get("PORT", 5000))
    
    print 'hi1, i.e. port assigned';sys.stdout.flush()
    
    app.run(host='0.0.0.0',port=port, debug=True)