import dash
import dash_html_components as html
import plotly.graph_objects as go
import dash_core_components as dcc
from dash.dependencies import Input, Output
import matplotlib.pyplot as plt
import pandas as pd
from scipy.ndimage.filters import generic_filter
import numpy as np


data_path = 'https://github.com/owid/covid-19-data/raw/master/public/data/owid-covid-data.csv'
data = pd.read_csv(data_path)

app = dash.Dash()

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
    smoothing_size = 7
    death_delay = 18
    country_data = data[data['location']==dropdown_value]
    cases = generic_filter(country_data.sort_values('date')['new_cases'],
                           np.nanmean, size=smoothing_size)
    death = generic_filter(country_data.sort_values('date')['new_deaths'],
                           np.nanmean, size=smoothing_size)
    if death_delay == 0:
        lethality_rate = death/cases
    else:
        lethality_rate = death[death_delay:]/cases[:-death_delay]
    lethality_rate[1<lethality_rate]=0
    lethality_rate = lethality_rate[to_keep[death_delay:]]
    all_ticks = country_data['date'][len(country_data['date'])-len(lethality_rate):]
    # ax.plot(all_ticks, lethality_rate, '-', label='Lethality ratio')
    # ax.set_ylabel('Ratio death over #cases')
    # ax.set_ylim(ylim)
    # ax.legend()
    # ax.set_title(country)
    # if 1 < nb_plots:
    #     for ax, val in zip(axes[1:], additional_plots):
    #         Y = generic_filter(country_data.sort_values('date')[val],
    #                            np.nanmean, size=smoothing_size)[to_keep]
    #         ax.plot(Y, '-', label=val)
    #         ax.set_ylabel(f'#{val}')
    #         if 'per_hundred' in val:
    #             ax.set_ylim(0, 100)
    #         ax.legend()
    # step_ticks = max(1, len(ticks)//6)
    # ax.set_xticks(ticks[::step_ticks])
    # ax.set_xticklabels(tick_labels[::step_ticks])
    # ax.set_xlim(0, max(all_ticks))
    # fig.tight_layout()

    fig = go.Figure([go.Scatter(x = all_ticks, y = lethality_rate,\
                     line = dict(color = 'firebrick', width = 4))
                     ])
    
    fig.update_layout(title = 'Number of new cases',
                      xaxis_title = 'Dates',
                      yaxis_title = 'Prices'
                      )
    return fig  



if __name__ == '__main__': 
    app.run_server('0.0.0.0')