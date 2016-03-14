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
    return redirect('/graph')

@app.route('/graph')
def graph():
  plot_components = get_stock.get_and_plot(app.stock)
  if plot_components == 'failed':
    return redirect('/error')
  else:
    return render_template('graph.html', title = app.stock, script = plot_components[0], 
                           div = plot_components[1])

@app.route('/error')
def error():
  return render_template('error.html', stock=app.stock)
  #page with a link to 

if __name__ == '__main__':
  app.run(port=33507)
