import dash
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
from dash.dependencies import Input, Output


app = dash.Dash()

data_path = 'https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv'
data = pd.read_csv(data_path)

app.layout = html.Div(id = 'parent', children = [
    html.H1(id = 'H1', children = 'Covid-data',
            style = {'textAlign':'center',
                     'marginTop':40,'marginBottom':40}),

        dcc.Dropdown( id = 'dropdown',
        options = [
            {'label':'France', 'value':'France' },
            {'label': 'United Kingdom', 'value':'United Kingdom'},
            {'label': 'India', 'value':'India'},
            ],
        value = 'France'),
        dcc.Graph(id = 'bar_plot')
    ])
    
    
@app.callback(Output(component_id='bar_plot', component_property= 'figure'),
              [Input(component_id='dropdown', component_property= 'value')])


def graph_update(dropdown_value):
    print(dropdown_value)
    sub_data = df[df==dropdown_value]
    fig = go.Figure([go.Scatter(x = df['date'], y = df['new_cases'],\
                     line = dict(color = 'firebrick', width = 4))
                     ])
    
    fig.update_layout(title = 'Number of new cases',
                      xaxis_title = 'Dates',
                      yaxis_title = 'Prices'
                      )
    return fig  



if __name__ == '__main__': 
    app.run_server('0.0.0.0')