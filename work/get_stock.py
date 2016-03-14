import requests
import numpy as np
import pandas as pd
import datetime
import datetime
from bokeh.plotting import figure
from bokeh.embed import components
from jinja2 import Template
from dateutil.relativedelta import relativedelta

template = Template("""
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>{{ title }}</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/css/bootstrap-theme.min.css">
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.5/js/bootstrap.min.js"></script>
    <link
    href="http://cdn.pydata.org/bokeh/release/bokeh-0.10.0.min.css"
    rel="stylesheet" type="text/css">
    <script src="http://cdn.pydata.org/bokeh/release/bokeh-0.10.0.min.js"></script>
    {{ script }}
  </head>
  <body>
    <div>
        <h2><a href='index'>Return to index</a></h2>
    </div>
    {{ div }}
  </body>
</html>
""")

def get_and_plot(stock_symbol, folder):
  global template
  try:
    r = requests.get('https://www.quandl.com/api/v3/datasets/WIKI/'+stock_symbol+'.json')
    if r.status_code != 200:
      return True
    df = pd.DataFrame(data = np.array(r.json()['dataset']['data']), 
                      columns = r.json()['dataset']['column_names'])
    one_month_ago = datetime.date.today()-relativedelta(months=1)
    to_use = pd.to_datetime(df.Date)>one_month_ago
    
    p = figure(x_axis_type='datetime', x_axis_label = 'Date', y_axis_label = 'Price',
               plot_width = 600, plot_height = 550)
    p.title = stock_symbol
    p.line(pd.to_datetime(df.Date[to_use]), df.High[to_use])
    script, div = components(p)
    
    output_file = folder+'graph.html'
    with open(output_file, 'w') as f:
      f.write(template.render(script = script, div = div, title = stock_symbol))
  except:
    return True

if __name__ == '__main__':
  if get_and_plot('MSFT', ''):
    print 'MSFT failed'
  if get_and_plot('Not a ticker symbol', ''):
    print 'Failure successful'