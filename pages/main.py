import dash
from dash import html, callback, Output, Input, State, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
import requests
from utils.work_with_api import UserFinctionality

dash.register_page(__name__, path_template="/app")

def main_layout():
    return dbc.Container([
        html.H1('Запустить расчет'),
        dcc.Link("История запусков", href='/history'),
        dbc.Row(id='alert-row'),
        dbc.Col([dbc.Label("Количество узлов по x", ),
                    dbc.Input(type="text", n_submit=0, id="nx",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ),  

        dbc.Col([dbc.Label("Количество узлов по y", ),
                    dbc.Input(type="text", n_submit=0, id="ny",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ), 
        
        dbc.Col([dbc.Label("Количество шагов по времени", ),
                    dbc.Input(type="text", n_submit=0, id="T",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ),         

        dbc.Col([dbc.Label("Координата перегородки x1", ),
                    dbc.Input(type="text", n_submit=0, id="nx1",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ), 

        dbc.Col([dbc.Label("Координата перегородки x2", ),
                    dbc.Input(type="text", n_submit=0, id="nx2",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ), 
        
        dbc.Col([dbc.Label("Координата перегородки y1", ),
                    dbc.Input(type="text", n_submit=0, id="ny1",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ), 
        
        dbc.Col([dbc.Label("Координата уровня воды в волнопродукторе", ),
                    dbc.Input(type="text", n_submit=0, id="ny2",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ), 
        
        dbc.Col([dbc.Label("Координата уровня воды в лотке", ),
                    dbc.Input(type="text", n_submit=0, id="ny3",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ), 
        
        dbc.Col([dbc.Label("X координата левой нижней точки области", ),
                    dbc.Input(type="text", n_submit=0, id="ax",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ), 
        dbc.Col([dbc.Label("X координата правой верхнней точки области", ),
                    dbc.Input(type="text", n_submit=0, id="bx",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ), 
                
        dbc.Col([dbc.Label("Y координата левой нижней точки области", ),
                    dbc.Input(type="text", n_submit=0, id="ay",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ),
        
        dbc.Col([dbc.Label("Y координата правой верхнней точки области", ),
                    dbc.Input(type="text", n_submit=0, id="by",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ),          
        
        dbc.Col([dbc.Label("eps", ),
                    dbc.Input(type="text", n_submit=0, id="eps",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ), 
        
        dbc.Col([dbc.Label("Плотность воздуха"),
                    dbc.Input(type="text", n_submit=0, id="ro1",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ), 
        dbc.Col([dbc.Label("Плотность воды"),
                    dbc.Input(type="text", n_submit=0, id="ro2",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ),         
        
        dbc.Col([dbc.Label("Вязкость воздуха", ),
                    dbc.Input(type="text", n_submit=0, id="mu1",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ),    

        dbc.Col([dbc.Label("Вязкость воды", ),
                    dbc.Input(type="text", n_submit=0, id="mu2",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ),
        
        dbc.Col([dbc.Label("Шаг по времени", ),
                    dbc.Input(type="text", n_submit=0, id="tau",
                            placeholder=['Введите значение']),
                    ], width={'size': 4, 'offset': 4}
                ),
        
        dbc.Col([dbc.Label("Коэффициент диффузии", ),
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
          Input('calculate-button', 'n_clicks'),
          State('user-name', 'data')],
          prevent_initial_call=True)
def start_calculations(nx, ny, T, nx1, nx2, 
                       ny1, ny2,ny3, ax, bx, 
                       ay, by, eps, ro1, ro2, 
                       mu1, mu2, tau, D, Sq,
                       n_clicks, username):
    ctx = dash.callback_context
    if ctx.triggered_id is not None and ctx.triggered_id == 'calculate-button': 
        user = UserFinctionality()
        json = {'nx': nx, 'ny': ny, 'T': T, 'nx1': nx1, 'nx2': nx2,
                'ny1': ny1, 'ny2': ny2, 'ny3': ny3, 'ax': ax,
                'bx': bx, 'ay': ay, 'by': by,
                'eps': eps, 'ro1':ro1, 'ro2': ro2, 'mu1': mu1, 
                'mu2': mu2, 'tau': tau,
                'D': D, 'Sq': Sq, 'username': username}
        response = user.send_calculate(json=json)
        if response.status_code == 200:
            return dbc.Alert(response.content.decode('utf-8'), color="success", duration=4000)
        else:
            return dbc.Alert(response.content.decode('utf-8'), color="danger", duration=4000)
    else:
        return dash.no_update