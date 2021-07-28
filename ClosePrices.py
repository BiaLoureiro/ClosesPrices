# -*- coding: utf-8 -*-
"""
Created on Tue Jul 27 17:07:00 2021

@author: beatr
"""
import requests
import json
import pandas as pd
import plotly.express as px
from plotly.offline import plot
import plotly.graph_objs as go
from datetime import datetime, timedelta

class RequestBitmex:
    @staticmethod
    def retrieve_candles(symbol, bin_size, reverse, start_timestamp=None, end_timestamp=None):
        params = {
            'symbol': symbol,
            'binSize': bin_size,
            'reverse': reverse
        }

        if start_timestamp is not None:
            params['startTime'] = start_timestamp

        if end_timestamp is not None:
            params['endTime'] = end_timestamp

        r = requests.get(f'https://www.bitmex.com/api/v1/trade/bucketed', params=params)

        if r.status_code == 200:
            if len(r.json()) == 0:
                print('Error: {}'.format(r.text))
            else:
                return r.json()
        else:
            print('Error: {}'.format(r.text))


symbol1 = 'XBTUSD'
symbol2 = 'AAVEUSDT'
symbol3 = 'BNBUSDT'
bin_size = '1d'
reverse = 'false'
start_timestamp = datetime(2021, 7, 15)
end_timestamp = datetime(2021, 7, 27)

t1 = RequestBitmex.retrieve_candles(symbol1, bin_size, reverse, start_timestamp, end_timestamp)
t2 = RequestBitmex.retrieve_candles(symbol2, bin_size, reverse, start_timestamp, end_timestamp)
t3 = RequestBitmex.retrieve_candles(symbol3, bin_size, reverse, start_timestamp, end_timestamp)

df1 = pd.DataFrame(t1)
df2 = pd.DataFrame(t2)
df3 = pd.DataFrame(t3)
df2_novo = df2.rename(columns={'close': 'close2', 'symbol': 'symbol2'})
df3_novo = df3.rename(columns={'close': 'close3', 'symbol': 'symbol3'})

df = pd.concat([df1, df2_novo, df3_novo])
#print(df)
df["timestamp"] = pd.to_datetime(df['timestamp'])
#fig1 = px.line(df1, x=df1["timestamp"], y=df1.close, title=('XBT'))
#plot(fig1)

trace1 = {
    'x': df.timestamp,
    'y': df.close,
    'type': 'scatter',
    'mode': 'lines',
    'line': {
        'width': 1,
        'color': 'red'
    },
    'name': 'XBT'
}


trace2 = {
    'x': df.timestamp,
    'y': df.close2,
    'type': 'scatter',
    'mode': 'lines',
    'line': {
        'width': 1,
        'color': 'blue'
    },
    'name': 'AAVE'
}

trace3 = {
    'x': df.timestamp,
    'y': df.close3,
    'type': 'scatter',
    'mode': 'lines',
    'line': {
        'width': 1,
        'color': 'green'
    },
    'name': 'BNB'
}

data = [trace1, trace2, trace3]

layout = go.Layout({
    'title': {
        'text': 'gráfico de preços',
        'font': {
            'size': 20
        }
    }
})

fig = go.Figure(data=data, layout=layout)
plot(fig)

