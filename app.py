import os
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index')
def index():
  #return render_template('index.html')
  return render_template('home_page.html')

if __name__ == '__main__':
  # app.run(host='0.0.0.0',port=33507)
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0',port=port)
