from flask import Flask, render_template, request, redirect
from work import get_stock
import os.path

app = Flask(__name__)
app.stock = ''
folder = 'templates/'

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET', 'POST'])
def index():
  if request.method == 'GET':
    return render_template('index.html')
  else:
    app.stock = request.form['stock']
    failed = get_stock.get_and_plot(app.stock, folder)

    if failed:
      return redirect('/error')
    else:
      return redirect('/graph')

@app.route('/graph')
def graph():
 return render_template('graph.html')

@app.route('/error')
def error():
  return render_template('error.html', stock=app.stock)
  #page with a link to 

if __name__ == '__main__':
  app.run(port=33507, debug=True)
