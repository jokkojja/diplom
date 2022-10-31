from dash import Dash, dcc, html
from dash.dependencies import Input, Output, State


external_stylesheets = [
    {
        "href": "C:/Users/potak/OneDrive/Desktop/test/diplom/assets/style.css"
        #"family=Lato:wght@400;700&display=swap",
        #"rel": "stylesheet",
    },
]
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Дипломная работа"

app.layout = html.Div(
    className="body",
    children=[
        html.Div(
            className="header_main",
            children=[
                html.Header(
                    className="header",
                    children=[
                        html.Div(
                            className="container",
                            children=[
                                html.Div(
                                    className="header_text",
                                    children='Дипломная работа'
                                )
                            ]
                        )
                    ]
                )
            ]
        ),
        html.Div(
            children=[
                html.Div(
                    className="vvod_dannih",
                    children=[
                        html.Div(
                            className="container",
                            children=[
                                html.Div(
                                    className="input",
                                    children=[
                                        html.Form(
                                            method="POST",
                                            action="/",
                                            children=[
                                                html.Div(
                                                    className="box",
                                                    children=[
                                                        html.Div([
                                                            dcc.Input(id='input-1-state', type='text', value=''),
                                                            dcc.Input(id='input-2-state', type='text', value=''),
                                                            html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
                                                            html.Div(id='output-state')
                                                        ])
                                                    ]   
                                                )
                                            ]
                                        )
                                        
                                    ]
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

@app.callback(Output('output-state', 'children'),
              Input('submit-button-state', 'n_clicks'),
              State('input-1-state', 'value'),
              State('input-2-state', 'value'))
def update_output(n_clicks, input1, input2):
    return u'''
        The Button has been pressed {} times,
        Input 1 is "{}",
        and Input 2 is "{}"
    '''.format(n_clicks, input1, input2)

    



if __name__ == '__main__':
    app.run_server(debug=True)
