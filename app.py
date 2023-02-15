from dash.exceptions import PreventUpdate
import dash
from dash import Dash, html, dcc, Output, Input, State
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc
from navbar import navbar

app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
           suppress_callback_exceptions=True)


def layout (cur_user=None):
    return html.Div([navbar(user=cur_user), dash.page_container])
        


app.layout = html.Div([dcc.Location(id='url', refresh=False),
                       dcc.Store(id='user-name', storage_type='session'),
                       html.Div(dash.page_container, id='main-layout')])

@app.callback(Output("main-layout", "children"),
              Input('user-name', 'modified_timestamp'),
              State('user-name', 'data')
              )
def set_lang_main(ts2, user):
    if ts2 is None:
        raise PreventUpdate
    return layout(user)

if __name__ == '__main__':
    app.run(debug = True)