import dash
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
from dash.dependencies import Input, Output
import matplotlib.pyplot as plt
import pandas as pd
from scipy.ndimage.filters import generic_filter
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

# app = dash.Dash()

# app.layout = html.Div([
#     html.Div([

#         html.Div([
#             dcc.Dropdown(
#                 id='crossfilter-xaxis-column',
#                 options=[{'label': i, 'value': i} for i in available_indicators],
#                 value='Fertility rate, total (births per woman)'
#             ),
#             dcc.RadioItems(
#                 id='crossfilter-xaxis-type',
#                 options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
#                 value='Linear',
#                 labelStyle={'display': 'inline-block'}
#             )
#         ],
#         style={'width': '49%', 'display': 'inline-block'}),

#         html.Div([
#             dcc.Dropdown(
#                 id='crossfilter-yaxis-column',
#                 options=[{'label': i, 'value': i} for i in available_indicators],
#                 value='Life expectancy at birth, total (years)'
#             ),
#             dcc.RadioItems(
#                 id='crossfilter-yaxis-type',
#                 options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
#                 value='Linear',
#                 labelStyle={'display': 'inline-block'}
#             )
#         ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
#     ], style={
#         'borderBottom': 'thin lightgrey solid',
#         'backgroundColor': 'rgb(250, 250, 250)',
#         'padding': '10px 5px'
#     }),

#     html.Div([
#         dcc.Graph(
#             id='crossfilter-indicator-scatter',
#             hoverData={'points': [{'customdata': 'Japan'}]}
#         )
#     ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
#     html.Div([
#         dcc.Graph(id='x-time-series'),
#         dcc.Graph(id='y-time-series'),
#     ], style={'display': 'inline-block', 'width': '49%'}),

#     html.Div(dcc.Slider(
#         id='crossfilter-year--slider',
#         min=df['Year'].min(),
#         max=df['Year'].max(),
#         value=df['Year'].max(),
#         step=None,
#         marks={str(year): str(year) for year in df['Year'].unique()}
#     ), style={'width': '49%', 'padding': '0px 20px 20px 20px'})
# ])

# @app.callback(
#     dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
#     [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
#      dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
#      dash.dependencies.Input('crossfilter-xaxis-type', 'value'),
#      dash.dependencies.Input('crossfilter-yaxis-type', 'value'),
#      dash.dependencies.Input('crossfilter-year--slider', 'value')])

# def update_graph(xaxis_column_name, yaxis_column_name,
#                  xaxis_type, yaxis_type,
#                  year_value):
#     dff = df[df['Year'] == year_value]

#     return {
#         'data': [go.Scatter(
#             x=dff[dff['Indicator Name'] == xaxis_column_name]['Value'],
#             y=dff[dff['Indicator Name'] == yaxis_column_name]['Value'],
#             text=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
#             customdata=dff[dff['Indicator Name'] == yaxis_column_name]['Country Name'],
#             mode='markers',
#             marker={
#                 'size': 15,
#                 'opacity': 0.5,
#                 'line': {'width': 0.5, 'color': 'white'}
#             }
#         )],
#         'layout': go.Layout(
#             xaxis={
#                 'title': xaxis_column_name,
#                 'type': 'linear' if xaxis_type == 'Linear' else 'log'
#             },
#             yaxis={
#                 'title': yaxis_column_name,
#                 'type': 'linear' if yaxis_type == 'Linear' else 'log'
#             },
#             margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
#             height=450,
#             hovermode='closest'
#         )
#     }

# def create_time_series(dff, axis_type, title):
#     return {
#         'data': [go.Scatter(
#             x=dff['Year'],
#             y=dff['Value'],
#             mode='lines+markers'
#         )],
#         'layout': {
#             'height': 225,
#             'margin': {'l': 20, 'b': 30, 'r': 10, 't': 10},
#             'annotations': [{
#                 'x': 0, 'y': 0.85, 'xanchor': 'left', 'yanchor': 'bottom',
#                 'xref': 'paper', 'yref': 'paper', 'showarrow': False,
#                 'align': 'left', 'bgcolor': 'rgba(255, 255, 255, 0.5)',
#                 'text': title
#             }],
#             'yaxis': {'type': 'linear' if axis_type == 'Linear' else 'log'},
#             'xaxis': {'showgrid': False}
#         }
#     }

# @app.callback(
#     dash.dependencies.Output('x-time-series', 'figure'),
#     [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
#      dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
#      dash.dependencies.Input('crossfilter-xaxis-type', 'value')])
# def update_y_timeseries(hoverData, xaxis_column_name, axis_type):
#     country_name = hoverData['points'][0]['customdata']
#     dff = df[df['Country Name'] == country_name]
#     dff = dff[dff['Indicator Name'] == xaxis_column_name]
#     title = '<b>{}</b><br>{}'.format(country_name, xaxis_column_name)
#     return create_time_series(dff, axis_type, title)

# @app.callback(
#     dash.dependencies.Output('y-time-series', 'figure'),
#     [dash.dependencies.Input('crossfilter-indicator-scatter', 'hoverData'),
#      dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
#      dash.dependencies.Input('crossfilter-yaxis-type', 'value')])
# def update_x_timeseries(hoverData, yaxis_column_name, axis_type):
#     dff = df[df['Country Name'] == hoverData['points'][0]['customdata']]
#     dff = dff[dff['Indicator Name'] == yaxis_column_name]
#     return create_time_series(dff, axis_type, yaxis_column_name)

# app.css.append_css({
#     'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
# })

# if __name__ == '__main__':
#     app.run_server('0.0.0.0')


app = dash.Dash()

data_path = ('https://github.com/owid/covid-19-data/raw/'
             'master/public/data/owid-covid-data.csv')

df = pd.read_csv(data_path)

available_indicators = df['location'].unique()


app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown( id = 'dropdown',
            options = [ {'label': c, 'value': c} for c in available_indicators],
            value = 'France'),
        ],
        style={'width': '49%', 'display': 'inline-block', 'height': '10%'}),


    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    })
    ,
    html.Div([
        dcc.Graph(id='lethality'),
        dcc.Graph(id='new_cases'),
    ], style={'display': 'inline-block', 'width': '80%'}),
])

@app.callback(Output(component_id='lethality', component_property='figure'),
              [Input(component_id='dropdown', component_property='value')])
def graph_update(country):
    print(country)
    smoothing_size = 7
    death_delay = 18
    country_data = df[df['location']==country]
    cases = generic_filter(country_data.sort_values('date')['new_cases'],
                           np.nanmean, size=smoothing_size)
    death = generic_filter(country_data.sort_values('date')['new_deaths'],
                           np.nanmean, size=smoothing_size)
    if death_delay == 0:
        lethality_rate = death/cases
    else:
        lethality_rate = death[death_delay:]/cases[:-death_delay]
    lethality_rate[1<lethality_rate]=0
    all_ticks = country_data['date'][len(country_data['date'])-len(lethality_rate):]
    # fig = go.Figure([go.Scatter(x = all_ticks, y = lethality_rate,\
    #                  line = dict(color = 'firebrick', width = 4))
    #                  ])

    # fig.update_layout(title = 'Lethality Rate',
    #                   xaxis_title = 'Dates',
    #                   yaxis_title = 'Ratio death over #cases'
    #                   )

    return {
        'data': [go.Scatter(
                    x=all_ticks,
                    y=lethality_rate,
                    mode='lines'
        )],
        'layout': {
            'yaxis': {'type': 'linear'},
            'xaxis': {'showgrid': False}
        }
    }

@app.callback(Output(component_id='new_cases', component_property='figure'),
              [Input(component_id='dropdown', component_property='value')])
def graph_update(country):
    print(country)
    smoothing_size = 7
    death_delay = 18
    country_data = df[df['location']==country]
    cases = generic_filter(country_data.sort_values('date')['new_cases'],
                           np.nanmean, size=smoothing_size)

    return {
        'data': [go.Scatter(
                    x=country_data['date'],
                    y=cases,
                    mode='lines'
        )],
        'layout': {
            'yaxis': {'type': 'linear'},
            'xaxis': {'showgrid': False}
        }
    }


app.css.append_css({
    'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
})

if __name__ == '__main__':
    app.run_server('0.0.0.0')