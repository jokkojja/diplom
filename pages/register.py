from dash.exceptions import PreventUpdate
from dash import Dash, html, dcc, Output, Input, State, callback
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
import dash
from dash_iconify import DashIconify

from utils.validation import check_name, check_password
from utils.work_with_api import UserFinctionality


dash.register_page(__name__, path_template="/registration")

def registration_layout():
    return dbc.Container([
                dbc.Col(html.H2("Registration",
                                style={'paddingBottom': '20px'}),
                        width={'size': 4, 'offset': 4}),
                dbc.Col([dbc.Label("Username", html_for="example-email-grid"),
                         dbc.Input(type="text", n_submit=0, id="uname-registration",
                                   placeholder=['Enter your username']),
                         ], width={'size': 4, 'offset': 4}
                        ),
                dbc.Col([dbc.Label("Email", html_for="example-email-grid"),
                         dbc.Input(type="text", n_submit=0, id="email-registration",
                                   placeholder=['Enter your email']),
                         ], width={'size': 4, 'offset': 4}
                        ),
                dbc.Col([dbc.Label(["Password", ' ',
                                    DashIconify(icon="ant-design:question-circle-outlined",
                                                id="password-help-icon", width=16, color='#7491A5'),
                                    dbc.Popover(
                                        dbc.PopoverBody("Password must include at least one uppercase, one lowercase letter, one number and one special character (!@#$&*) and be 8-20 characters long"),
                                        target="password-help-icon",
                                        trigger="legacy hover",
                                        placement="top",
                                        hide_arrow=True)
                                    ], html_for="example-password-grid"),
                         html.Div(children=
                                  [dbc.Input(
                                            type="password", n_submit=0, id="pwd-registration",
                                            placeholder='Enter your password',
                                            style={'background-color': 'transparent', 'width': 'calc(100% - 50px)',
                                                   'display': 'inline', 'box-shadow': 'none'}
                                            ),
                                   dmc.Button(children=[DashIconify(icon="ant-design:eye-outlined",
                                                                    width=30, color='#7a8288',
                                                                    id='pwd-registration-icon')],
                                              style={'background-color': 'transparent',
                                                     'vertical-align': 'middle'}, compact=True,
                                              id='pwd-registration-icon-button')
                                  ],
                                  style={'padding': '0px'},
                                  className='form-control'),
                         ], width={'size': 4, 'offset': 4}
                        ),
                dbc.Col([dbc.Label("Repeat password", html_for="example-password-grid"),
                         html.Div(children=[
                             dbc.Input(
                                 type="password",
                                 n_submit=0,
                                 id="pwd2-registration",
                                 placeholder='Repeat password',
                                 style={'background-color': 'transparent', 'width': 'calc(100% - 50px)',
                                        'display': 'inline', 'box-shadow': 'none'}),
                             dmc.Button(children=[DashIconify(icon="ant-design:eye-outlined",
                                         width=30, color='#7a8288', id='pwd2-registration-icon')],
                                        style={'background-color': 'transparent',
                                               'vertical-align': 'middle'}, compact=True,
                                        id='pwd2-registration-icon-button'),
                         ],
                             style={'padding': '0px'},
                             className='form-control'),
                         ], width={'size': 4, 'offset': 4}
                        ),
                dbc.Col(dbc.Spinner(color="primary", show_initially=False, delay_show=500, children = dbc.Button(children=["Registration"], n_clicks=0, type='submit',
                                            id='register-button', style={'marginTop': '20px'})),
                                 width={'size': 4, 'offset': 4}),
                dbc.Col(html.Div(children='', id='output-registration'), style={'marginTop': '20px'},
                        width={'size': 4, 'offset': 4}),
                dbc.Col([html.A(["Have an account?"]),
                         dcc.Link(children=["Login"], href='/login', refresh=False)],
                        width={'size': 4, 'offset': 4})], style={'paddingBottom': '20px'}, id='login-main-container')
    
layout = dbc.Container([dcc.Location(id='registration-login', refresh=True), html.Div([], id='registration-layout')])


@callback(Output('registration-login', 'pathname'),
          Output('output-registration', 'children'),
          Input('register-button', 'n_clicks'),
          Input('uname-registration', 'value'),
          Input('email-registration', 'value'),
          Input('pwd-registration', 'value'),
          )  
def registration(n_clicks, username, email, password):
    if n_clicks > 0:
        user = UserFinctionality()
        response = user.send_register(username, password, email)
        status_code = response.status_code
        if status_code == 200:
            return '/login', dbc.Alert(response.text, color="success")
        else:
            return dash.no_update, dbc.Alert(response.text, color="danger")
    return dash.no_update

@callback(Output('uname-registration', 'valid'),
          Output('uname-registration', 'invalid'),
          Input('uname-registration', 'value'),
          prevent_initiall_call=False
)
def valid_username(username):
    if username is None:
        return dash.no_update
    username_valid = check_name(username)
    if username_valid:
        return True, False
    else:
        return False, True
      
            
@callback(Output('pwd-registration', 'valid'),
          Output('pwd-registration', 'invalid'),
          Input('pwd-registration', 'value'),
          prevent_initiall_call=False
)
def valid_password(pswd):
    if pswd is None:
        return dash.no_update
    pswd_valid = check_password(pswd)
    if pswd_valid:
        return True, False
    else:
        return False, True             
    
@callback(Output('pwd2-registration', 'valid'),
          Output('pwd2-registration', 'invalid'),
          Input('pwd-registration', 'value'),
          Input('pwd2-registration', 'value'),
          prevent_initiall_call=False
)
def valid_repeated_password(pswd, pswd2):
    if pswd is None or pswd2 is None:
        return dash.no_update
    pswd_valid = pswd == pswd2
    if pswd_valid:
        return True, False
    else:
        return False, True
    
@callback(
    Output('registration-layout', 'children'),
    Input('user-name', 'modified_timestamp'),
    State('user-name', 'data'))
def check_current_user(ts, username):
    if ts is None:
        raise PreventUpdate
    return registration_layout()

@callback(
    Output('pwd2-registration', 'type'),
    Output('pwd2-registration-icon', 'icon'),
    Input('pwd2-registration-icon-button', 'n_clicks'),
    State('pwd2-registration', 'type'),
    prevent_initiall_call=True
)
def hide_pass_2(n_clicks, type):
    if n_clicks is not None:
        if type == 'password':
            return 'text', 'ant-design:eye-invisible-outlined'
        else:
            return 'password', 'ant-design:eye-outlined'
    else:
        return dash.no_update, dash.no_update


@callback(
    Output('pwd-registration', 'type'),
    Output('pwd-registration-icon', 'icon'),
    Input('pwd-registration-icon-button', 'n_clicks'),
    State('pwd-registration', 'type'),
    prevent_initiall_call=True
)
def hide_pass_1(n_clicks, type):
    if n_clicks is not None:
        if type == 'password':
            return 'text', 'ant-design:eye-invisible-outlined'
        else:
            return 'password', 'ant-design:eye-outlined'
    else:
        return dash.no_update, dash.no_update