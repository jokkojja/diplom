import dash
from dash import html, callback, Output, Input, State, dcc, ctx
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import dash_mantine_components as dmc
import requests
from utils.work_with_api import UserFinctionality
dash.register_page(__name__, path_template="/login")


def login_layout():
    return dbc.Container([
                dbc.Col(html.Div(["Please log in to continue:"],
                                 style={'paddingTop': '100px', 'paddingBottom': '20px'}),
                        width={'size': 4, 'offset': 4}),
                dbc.Col([dbc.Label(["Username"], html_for="example-email-grid"),
                         dbc.Input(type="text", n_submit=0, id="uname-box",
                                   placeholder=['Enter your username']),
                         ], width={'size': 4, 'offset': 4}
                        ),
                dbc.Col([html.Div(children=
                                  [dbc.Input(
                                            type="password", n_submit=0, id="pwd-box",
                                            placeholder='Enter your password',
                                            style={'background-color': 'transparent', 'width': 'calc(100% - 50px)',
                                                   'display': 'inline', 'box-shadow': 'none'}
                                            ),
                                   dmc.Button(children=[DashIconify(icon="ant-design:eye-outlined",
                                                                    width=30, color='#7a8288',
                                                                    id='pwd-box-icon')],
                                              style={'background-color': 'transparent',
                                                     'vertical-align': 'middle'}, compact=True,
                                              id='pwd-box-icon-button')
                                  ],
                                  style={'padding': '0px'},
                                  className='form-control'),
                         ], width={'size': 4, 'offset': 4}
                        ),
                dbc.Col(dbc.Button(children=["Login"], n_clicks=0, type='submit', id='login-button',
                                   style={'marginTop': '20px'}),
                        width={'size': 4, 'offset': 4}),
                dbc.Col(html.Div(children='', id='output-state'), style={'marginTop': '20px'},
                        width={'size': 4, 'offset': 4}),

            dbc.Col([html.A(["Don't have an account?"]),
                     html.A(children=["Registration"], href='/registration')
                     ], width={'size': 4, 'offset': 4})], id='login-main-container')



layout = dbc.Container([dcc.Location(id='login-login', refresh=True), html.Div([], id='login-layout')])

@callback(Output('login-login', 'pathname'),
          Output('output-state', 'children'),
          Output('user-name', 'data'),
          Input('uname-box', 'value'),
          Input('pwd-box', 'value'),
          Input('login-button', 'n_clicks')
          )
def login(username, password, n_clicks):
    triggered_id = ctx.triggered_id
    if n_clicks > 0 and triggered_id == 'login-button':
        user = UserFinctionality()
        response = user.send_login(username, password)
        status_code = response.status_code
        if status_code == 200:
            return '/app', dbc.Alert(response.text, color="success"), username
        else:
            return dash.no_update, dbc.Alert(response.text, color="danger"), None
    return dash.no_update

@callback(
    Output('pwd-box', 'type'),
    Output('pwd-box-icon', 'icon'),
    Input('pwd-box-icon-button', 'n_clicks'),
    State('pwd-box', 'type'),
    prevent_initiall_call=True
)
def hide_pass_1(n_clicks, type_):
    if n_clicks is not None:
        if type_ == 'password':
            return 'text', 'ant-design:eye-invisible-outlined'
        else:
            return 'password', 'ant-design:eye-outlined'
    else:
        return dash.no_update, dash.no_update

@callback(
    Output('login-layout', 'children'),
    Input('user-name', 'modified_timestamp'),
    State('user-name', 'data'))
def show_layout(ts, username):
    if ts is None:
        raise PreventUpdate
    return login_layout()