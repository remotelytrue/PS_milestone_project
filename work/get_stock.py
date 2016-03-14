import requests
import numpy as np
import pandas as pd
import datetime
from bokeh.plotting import figure
from bokeh.embed import components
from jinja2 import Template
from dateutil.relativedelta import relativedelta

def get_and_plot(stock_symbol):
  try:
    url = 'https://www.quandl.com/api/v3/datasets/WIKI/%s.json'%stock_symbol
    session = requests.Session()
    session.mount('http://', requests.adapters.HTTPAdapter(max_retries=3))
    r = session.get(url)
    if r.status_code != 200:
      return 'failed'
    df = pd.DataFrame(data = np.array(r.json()['dataset']['data']), 
                      columns = r.json()['dataset']['column_names'])
    one_month_ago = datetime.date.today()-relativedelta(months=1)
    to_use = pd.to_datetime(df.Date)>one_month_ago
    
    p = figure(x_axis_type='datetime', x_axis_label = 'Date', y_axis_label = 'Price',
               plot_width = 600, plot_height = 550)
    p.title = stock_symbol
    p.line(pd.to_datetime(df.Date[to_use]), df.High[to_use])
    script, div = components(p)
    
    return (script, div)
  except:
    return 'failed'

if __name__ == '__main__':
  if get_and_plot('MSFT', ''):
    print 'MSFT failed'
  if get_and_plot('Not a ticker symbol', ''):
    print 'Failure successful'