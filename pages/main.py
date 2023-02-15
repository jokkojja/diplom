import dash
from dash import html, callback, Output, Input, State, dcc
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate

dash.register_page(__name__, path_template="/")

def main_layout():
    return dbc.Container([
        html.H1('Main app')
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
    