import dash
from dash import html, callback, Output, Input, State, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from dash_iconify import DashIconify
import dash_mantine_components as dmc
#from utils.work_with_database import check_username, check_user_password

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

# @callback(Output('user-name', 'data'),
#           Output('login-login', 'pathname'),
#           [Input('login-button', 'n_clicks'),
#            Input('uname-box', 'n_submit'),
#            Input('pwd-box', 'n_submit')],
#           [State('uname-box', 'value'),
#            State('pwd-box', 'value')])
# def login(n_clicks, n_submit_uname, n_submit_pwd, input1, input2):
#     if check_username(input1):
#         if check_user_password(input1, input2):
#             return input1, '/'
#         else:
#             return None, '/login'
#     else:
#         return None, '/login'


# @callback(Output('output-state', 'children'),
#           [Input('login-button', 'n_clicks'),
#            State('uname-box', 'n_submit'),
#            State('pwd-box', 'n_submit'),
#            State('uname-box', 'value'),
#            State('pwd-box', 'value')])
# def update_output(n_clicks, n_submit_uname, n_submit_pwd, input1, input2):

#     if n_clicks > 0 or n_submit_uname > 0 or n_submit_pwd > 0:
#         user = input1
#         if check_username(user):
#             if check_user_password(user, input2):
#                 return ''
#             else:
#                 return dbc.Alert('Incorrect username or password!', color="danger")
#         else:
#             return dbc.Alert('Incorrect username or password!', color="danger")
#     else:
#         return ''
    
@callback(
    Output('login-layout', 'children'),
    Input('user-name', 'modified_timestamp'),
    State('user-name', 'data'))
def change_lang2(ts, username):
    if ts is None:
        raise PreventUpdate
    return login_layout()

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