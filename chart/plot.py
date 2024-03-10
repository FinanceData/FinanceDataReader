#-*- coding: utf-8 -*-
#
# FinaceDataReader chart.py
# (c)2018-2023 FinaceData.KR

import numpy as np

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
except ModuleNotFoundError as e:
    plotly_install_msg = f'''{'-' * 80}
    FinanceDataReade.chart.plot() dependen on plotly
    plotly not installed please install as follows

    pip install plotly

    FinanceDataReade.chart.plot()는 plotly에 의존성이 있습니다.
    명령창에서 다음과 같이 plotly를 설치하세요

    pip install plotly
    '''
    raise ModuleNotFoundError(plotly_install_msg)

import plotly.io as pio
# ['ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white', 'plotly_dark', 'presentation', 'xgridoff', 'ygridoff', 'gridon', 'none']
pio.templates.default = "plotly_white" 

def plot(df, kind='line', x=None, y=None, secondary_y=None, title=None, layout=None):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    traces = [] # [{'kind': 'line', 'x': x, 'y': y, '2nd_y': False}]
    
    if y == None:
        y = df.select_dtypes(include=np.number).columns.tolist()

    if type(y) == str:
        traces = [{'kind':kind, 'x':x, 'y':df[y], 'name':y, 'ry':False}]
    elif type(y) == list:
        cols = y
        ys = [df[col] for col in cols]
        kinds = [kind] * len(cols) if type(kind) == str else kind
        if x == None:
            xs = [df.index] * len(cols)
        elif type(x) == str:
            xs = [df[x]] * len(cols)
        elif type(x) == list:
            xs = [df[col] for col in x]
        names = cols
        if secondary_y==None:
            rys = [False] * len(cols)
        elif type(secondary_y) == str:
            rys = [col == secondary_y for col in cols]
        elif type(secondary_y) == list:
            rys = [col in secondary_y for col in cols]
        for kind, x, y, col, name, secondary_y in zip(kinds, xs, ys, cols, names, rys):
            traces.append({'kind':kind, 'x':x, 'y':y, 'name':name, 'ry':secondary_y})
    # print(traces)
    for trace in traces:
        if trace['kind'].lower() == 'line':
            fig.add_trace(go.Scatter(x=trace['x'], y=trace['y'], mode='lines', name=trace['name'], opacity=0.7), secondary_y=trace['ry'])
        elif trace['kind'].lower() == 'bar':
            fig.add_trace(go.Bar(x=trace['x'], y=trace['y'], name=trace['name'], opacity=0.7), secondary_y=trace['ry'])

    ## update_layout
    layout_defaults = {
    }
    new_layout = {}
    if title:
        new_layout.update({'title':title})
    new_layout.update(layout_defaults) 
    if layout:
        new_layout.update(layout)
    fig.update_layout(new_layout)
    return fig