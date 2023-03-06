import dash
from dash import html, callback, Output, Input, State, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import requests

dash.register_page(__name__, path_template="/")

def main_layout():
    return dbc.Container([
        html.H1('Main app'),
        dbc.Row(id='alert-row'),
        dbc.Col([dbc.Label("nx", ),
                    dbc.Input(type="text", n_submit=0, id="nx",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ),  

        dbc.Col([dbc.Label("ny", ),
                    dbc.Input(type="text", n_submit=0, id="ny",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ), 
        
        dbc.Col([dbc.Label("T", ),
                    dbc.Input(type="text", n_submit=0, id="T",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ),         

        dbc.Col([dbc.Label("Nx1", ),
                    dbc.Input(type="text", n_submit=0, id="nx1",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ), 

        dbc.Col([dbc.Label("Nx2", ),
                    dbc.Input(type="text", n_submit=0, id="nx2",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ), 
        
        dbc.Col([dbc.Label("Ny1", ),
                    dbc.Input(type="text", n_submit=0, id="ny1",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ), 
        
        dbc.Col([dbc.Label("ny2", ),
                    dbc.Input(type="text", n_submit=0, id="ny2",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ), 
        
        dbc.Col([dbc.Label("ny3", ),
                    dbc.Input(type="text", n_submit=0, id="ny3",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ), 
        
        dbc.Col([dbc.Label("ах", ),
                    dbc.Input(type="text", n_submit=0, id="ax",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ), 
        dbc.Col([dbc.Label("bx", ),
                    dbc.Input(type="text", n_submit=0, id="bx",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ), 
                
        dbc.Col([dbc.Label("ay", ),
                    dbc.Input(type="text", n_submit=0, id="ay",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ),
        
        dbc.Col([dbc.Label("by", ),
                    dbc.Input(type="text", n_submit=0, id="by",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ),          
        
        dbc.Col([dbc.Label("eps", ),
                    dbc.Input(type="text", n_submit=0, id="eps",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ), 
        
        dbc.Col([dbc.Label("ro1"),
                    dbc.Input(type="text", n_submit=0, id="ro1",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ), 
        dbc.Col([dbc.Label("ro2"),
                    dbc.Input(type="text", n_submit=0, id="ro2",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ),         
        
        dbc.Col([dbc.Label("mu1", ),
                    dbc.Input(type="text", n_submit=0, id="mu1",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ),    

        dbc.Col([dbc.Label("mu2", ),
                    dbc.Input(type="text", n_submit=0, id="mu2",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ),
        
        dbc.Col([dbc.Label("tau", ),
                    dbc.Input(type="text", n_submit=0, id="tau",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ),
        
        dbc.Col([dbc.Label("D", ),
                    dbc.Input(type="text", n_submit=0, id="D",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ),
        
        dbc.Col([dbc.Label("Sq", ),
                    dbc.Input(type="text", n_submit=0, id="sq",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ),          
        
        dbc.Col(dbc.Button(children=["Начать рассчет"], n_clicks=0, type='submit',
                                    id='calculate-button', style={'marginTop': '20px'}),
                            width={'size': 4, 'offset': 4}),                                                                          
                ], id='main-container')



layout = dbc.Container([
    dcc.Location(id='app-app', refresh=True), html.Div([], id='app-layout')])


@callback(Output('app-app', 'pathname'),
          Output('app-layout', 'children'),
          Input('user-name', 'modified_timestamp'),
          State('user-name', 'data'),
          State('url', 'pathname'),
)
def set_layout(ts_user_name, user_name, url):
    
    if user_name is None:
        return '/login', dash.no_update

    return dash.no_update, main_layout()


@callback(Output('alert-row', 'children'),
          [Input('nx', 'value'),
          Input('ny', 'value'),
          Input('T', 'value'),
          Input('nx1', 'value'),
          Input('nx2', 'value'),
          Input('ny1', 'value'),
          Input('ny2', 'value'),
          Input('ny3', 'value'),
          Input('ax', 'value'),
          Input('bx', 'value'),
          Input('ay', 'value'),
          Input('by', 'value'),
          Input('eps', 'value'),
          Input('ro1', 'value'),
          Input('ro2', 'value'),
          Input('mu1', 'value'),
          Input('mu2', 'value'),
          Input('tau', 'value'),
          Input('D', 'value'),
          Input('sq', 'value'),
          Input('calculate-button', 'n_clicks')],
          prevent_initial_call=True)
def start_calculations(nx, ny, T, nx1, nx2, 
                       ny1, ny2,ny3, ax, bx, 
                       ay, by, eps, ro1, ro2, 
                       mu1, mu2, tau, D, Sq,
                       n_clicks):
    ctx = dash.callback_context
    if ctx.triggered_id is not None and ctx.triggered_id == 'calculate-button': 
                   
        json = {'nx': nx, 'ny': ny, 'T': T, 'nx1': nx1, 'nx2': nx2,
                'ny1': ny1, 'ny2': ny2, 'ny3': ny3, 'ax': ax,
                'bx': bx, 'ay': ay, 'by': by,
                'eps': eps, 'ro1':ro1, 'ro2': ro2, 'mu1': mu1, 
                'mu2': mu2, 'tau': tau,
                'D': D, 'Sq': Sq}
        # print(json)
        requests.post(url='http://127.0.0.1:8051/calc', json=json)
        return dbc.Alert("ЗАПУСТИЛОСЬ", color="success", duration=5000)
    else:
        return dash.no_update