#!/usr/bin/python

import sqlite3
import plotly
plotly.tools.set_credentials_file(username='ati', api_key='y19eta4pkn')
import plotly.plotly as py
from plotly.graph_objs import *

DB="/home/pi/weather.sqlite3"
conn = sqlite3.connect(DB)
conn.row_factory = sqlite3.Row

sql = conn.cursor()
res = sql.execute("select avg(temperature) as temperature, avg(humidity) as humidity, avg(pressure)/1.3332239 as pressure, created_at from oregons where created_at > DATETIME('now', '-3 days') group by date(created_at), strftime('%H', created_at) order by created_at;").fetchall()

ts = [ row['created_at'] for row in res ]
datas = []
ranges = {'temperature': [-30,30], 'humidity': [0,100], 'pressure': [950, 1050]}

for i, field in enumerate(['temperature', 'humidity', 'pressure']):
  datas.append(Scatter(x=ts, y=[ float("{0:.1f}".format(row[field])) for row in res ], name=field, yaxis='y' + str(i+1)))

layout = Layout(
    yaxis=YAxis(
        domain=[0, 0.33]
    ),
    legend=Legend(
        traceorder='reversed'
    ),
    yaxis2=YAxis(
        domain=[0.33, 0.66]
    ),
    yaxis3=YAxis(
        domain=[0.66, 1]
    )
)
fig = Figure(data=Data(datas), layout=layout)
plot_url = py.plot(fig, filename='weather')
print plot_url
