import dash
from dash import html, callback, Output, Input, State, dcc, ctx, ALL
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import json
import requests
import ast
from utils.work_with_api import UserFinctionality
dash.register_page(__name__, path_template="/history")



def prepare_calculations_table(username):
    user = UserFinctionality()
    calculations = user.send_history(username).content.decode('utf-8')
    calculations = json.loads(calculations)[0]['calculatingHistory']
    divs = []
    for i, value in enumerate(calculations):
        fields = {}
        fields['Дата'] = value['datetime']
        fields['Id процесса'] = value['calc_id']
        fields['Статус'] = value['status']
        fields['Количество узлов по x'] = value['parameters']['nx']
        fields['Количество узлов по y'] = value['parameters']['ny']
        fields['Количество шагов по времени'] = value['parameters']['T']
        fields['Координата перегородки x1'] = value['parameters']['nx1']
        fields['Координата перегородки x2'] = value['parameters']['nx2']
        fields['Координата перегородки y1'] = value['parameters']['ny1']
        fields['Координата уровня воды в волнопродукторе'] = value['parameters']['ny2']
        fields['Координата уровня воды в лотке'] = value['parameters']['ny3']
        fields['X координата левой нижней точки области'] = value['parameters']['ax']
        fields['X координата правой верхнней точки области'] = value['parameters']['bx']
        fields['Y координата левой нижней точки области'] = value['parameters']['ay']
        fields['Y координата правой верхнней точки области'] = value['parameters']['by']
        fields['Eps'] = value['parameters']['eps']
        fields['Плотность воздуха'] = value['parameters']['ro1']
        fields['Плотность воды'] = value['parameters']['ro2']
        fields['Вязкость воздуха'] = value['parameters']['mu1']
        fields['Вязкость воды'] = value['parameters']['mu2']
        fields['Шаг по времени'] = value['parameters']['tau']
        fields['Коэффициент диффузии'] = value['parameters']['D'] 
        fields['Sq'] = value['parameters']['Sq']        
        div = html.Div(
    [
        dbc.Button(
            f"Показать информацию о рассчетете №{i+1}",
            id={"open-button": f"{i}"},
            className="mb-3",
            color="primary",
            n_clicks=0,
        ),
        dbc.Collapse(
            dbc.Card(dbc.CardBody([
                html.Pre(str(fields), style={"overflowX": "auto", "whiteSpace": "pre-wrap"}, id={'pre': f"{i}"}),
                dbc.Button("Остановить рассчет", id = {"stop-button": f"{i}"}, style = {"margin-right": "20px"}),
                dbc.Button("Скачать файл с рассчетом", id = {"download-button": f"{i}"}, style = {"margin-right": "20px"})
                ])),
            id={"collapse": f"{i}"},
            is_open=False,
        ),
        html.Br()
    ], style={'display': 'flex', 'justify-content': 'space-between'}
)
        divs.append(div)
    return divs
    
    
def history_layout(username):
    table = prepare_calculations_table(username)
    container = dbc.Container([
                html.H1('История запусков'),
                dcc.Link('Назад', href='/app'),
                dbc.Row(id='delete-alert-row'),
                dcc.Download(id = 'download-data'),
                ], id='calc-history-container')
    for elem in table:
        container.children.append(elem)
    
    return container

layout = dbc.Container([
    dcc.Location(id='history-app', refresh=True), html.Div([], id='history-layout')])

@callback(Output('history-app', 'pathname'),
          Output('history-layout', 'children'),
          Input('user-name', 'modified_timestamp'),
          State('user-name', 'data'),
          State('url', 'pathname'),
)
def set_layout(ts_user_name, user_name, url):
    if user_name is None:
        return '/login', dash.no_update
    return dash.no_update, history_layout(user_name)

@callback(Output({'collapse': ALL}, 'is_open'),
          Input({'open-button': ALL}, 'n_clicks'),
          Input({'collapse': ALL}, 'is_open'),
          prevent_initial_call=True)
def open_history(n_clicks, is_open):
    list_of_returns = [dash.no_update for i in is_open]
    if ctx.triggered[0]['value'] is not None:
        button_id = ctx.triggered_id['open-button']
        is_open = is_open[int(button_id)]
        if is_open:
            list_of_returns[int(button_id)] = False
            return list_of_returns
        else:
            list_of_returns[int(button_id)] = True
            return list_of_returns
    return dash.no_update


@callback(Output('delete-alert-row', 'children'),
          Input({'stop-button': ALL}, 'n_clicks'),
          Input({'pre': ALL}, 'children'),
          State('user-name', 'data'),
          prevent_initial_call=True)
def stop_calculating(n_clicks, content, username):
    if ctx.triggered[0]['value'] is not None:
        user = UserFinctionality()
        button_id = int(ctx.triggered_id['stop-button'])
        process_id = ast.literal_eval(content[button_id])['Id процесса']
        data = {'username': username, 'process_id': process_id}
        response = user.send_stop_calculate(data)
        if response.status_code == 200:
            return dbc.Alert(response.content.decode('utf-8'), color="success", duration=4000)
        else:
            return dbc.Alert("Извините, что-то пошло нет так", color="warning", duration=4000)
    return dash.no_update



@callback(Output('download-data', 'data'),
          Input({'download-button': ALL}, 'n_clicks'),
          Input({'pre': ALL}, 'children'),
          State('user-name', 'data'),
          prevent_initial_call=True)
def download_data(n_clicks, content, username):
    if ctx.triggered[0]['value'] is not None:
        user = UserFinctionality()
        button_id = int(ctx.triggered_id['download-button'])
        process_id = ast.literal_eval(content[button_id])['Id процесса']
        data = {'username': username, 'process_id': process_id}
        response = user.send_download(data)
        if response.status_code == 200:
            file = response.content
            return dcc.send_bytes(file, f"process_{process_id}_results.dat")
        else:
             return dbc.Alert("Извините, что-то пошло нет так", color="warning", duration=4000)
    return dash.no_update