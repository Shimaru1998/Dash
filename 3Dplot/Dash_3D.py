import os
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime,timedelta

fileDir = r"./"
fileExt = r".csv"
file_path = [_ for _ in os.listdir(fileDir) if _.endswith(fileExt)]
print(file_path)

def sPara(df,select):
    Para = df[select].to_list()
    if type(Para[0])==str:
        Para = list(map(float,Para))
    t = df['時間'].to_list()

    return t,Para

def mAvg(List,window_size):
    List = np.mat(List)
    i = 0
    moving_averages = []
    while i < len(List) - window_size + 1:
        this_window = List[i : i + window_size]

        window_average = (sum(this_window) / window_size).tolist()
        moving_averages.append(window_average)
        i += 1

    return moving_averages


#df = pd.read_csv(file_path[0],usecols=['時間','平均相電壓(V)'])
#Cnt,indice = Counting()
#t, para = sPara(df,'平均相電壓(V)')



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div(children=[
    html.H1(children='CPM-80', style={"text-align": "center"}),

    html.Div(children='Full Day Harmonics Printer',
             style={"text-align": "center", "color": "red"}),
    

    html.Div(children=[
        dcc.Graph(
            id='example-graph',
            figure={
                'data': [
                    #{'x': t,'y': para, 'type': 'line', 'name': '平均相電壓(V)'},
                    #{'x': [1, 2, 3], 'y': [2, 3, 5], 'type': 'line', 'name': '数据源B'},
                ],
                'layout': {
                    'title': '數據展示'
                }
            }
        )],
        style={'text-align': 'center','float':'left'}

        ),
    html.Div(children=[
        html.Div(children=[
            html.Span(children='參數選擇 :',
                    style= {'position':'relative','top':'5px','height': '60px', 'width': '100px'}),
            html.Br(),
            html.Span(children='日期 :',
                    style= {'position':'relative','top':'18px','height': '60px', 'width': '100px'}),
            ],
            style= {'height': '100px', 'width': '100px','text-align': 'center','float':'left'}
        ),
        
        
        
        
        html.Div(children=[
            dcc.Dropdown(
                id='HarmonicOf',
                options=[
                        {'label':'U1','value':'u1'},
                        {'label':'U2','value':'u2'},
                        {'label':'U3','value':'u3'},
                        {'label':'I1','value':'i1'},
                        {'label':'I2','value':'i2'},
                        {'label':'I3','value':'i3'},
                ],
                placeholder="Parameter",
                style=dict(
                        width='100%',
                        verticalAlign="middle"
                        ),
                value = 'i1',
                        clearable=False
                        #multi=True
                ),
                
            dcc.Dropdown(
                id='File_Select',
                options=[
                        {'label':'2021-1-16','value':'EMS_EXPORT_2021-1-16_2021-1-16.csv'},
                        {'label':'2021-1-17','value':'EMS_EXPORT_2021-1-17_2021-1-17.csv'}
                ],
                placeholder="Select Date",
                style=dict(
                        width='100%',
                        verticalAlign="middle"
                        ),
                value = 'EMS_EXPORT_2021-1-16_2021-1-16.csv',
                        clearable=False
                        #multi=True
                )
            ],
            style= {'height': '100px', 'width': '150px','float':'left'}
        )
                  

    ],style= {})
])

@app.callback(
    Output('example-graph', 'figure'),
    Input('HarmonicOf', 'value'),
    Input('File_Select', 'value'),
    )
def update_graph_live(select,file):
    data = []
    y = []
    col = ['時間']
    for n in range(2,64):
        col.append(select+'THDRateStart#'+str(n)+'()')
        y.append(n)
    df = pd.read_csv(file,usecols=col)
    df =df.replace('*',np.nan)
    df = df.dropna()
    x = df['時間'].to_list()
    for n in range(2,64):
        data.append(list(map(float,df[select+'THDRateStart#'+str(n)+'()'].to_list())))
    figure={
        'data': [go.Heatmap(x = x,y = y,z = data,colorscale= 'thermal'),
        ],
        'layout': {'title': select+' Individual Harmonics Distribution','height': 500, 'width': 1100,
                   'xaxis':{'title':'時間'},'yaxis':{'title':'階次'},'float':'left'},              
        }
    return figure

@app.callback(
    Output('File_Select', 'options'),
    Input('HarmonicOf', 'search_value')
    )
def update_Date_List(search_value):
    fileDir = r"./"
    fileExt = r".csv"
    file_path = [_ for _ in os.listdir(fileDir) if _.endswith(fileExt)]
    options = []
    for i in file_path :
        indices = [n for n, x in enumerate(i) if x == "_"]
        options.append({'label':i[indices[1]+1:indices[2]],'value':i})

    #print(options)
    return options


if __name__ == '__main__':
    app.run_server(host = '0.0.0.0')
