import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback
from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from datetime import date, datetime
import reeDatos
from flask import Flask


server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = 'Dashboard'


REE = reeDatos.Ree()
df = REE.cargarDataFrame()


# Initialize the app
#app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
# app.config.suppress_callback_exceptions = True
LOGO = "data:image/png;base64,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"  # "https://images.plot.ly/logo/new-branding/plotly-logomark.png"

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                dbc.Row(
                    [
                        dbc.Col(html.Img(src=LOGO, height="30px")),
                        dbc.Col(
                            dbc.NavbarBrand(
                                "Powered by Lucas Ortiz & Richard Navarro",
                            )
                        ),
                    ],
                    align="center",
                ),
                href="https://paucasesnovescifp.cat/",
                style={"textDecoration": "none"},
            ),
        ]
    ),
    color="green",
    dark=True,
)


calendar = dcc.DatePickerSingle(
    id="my-date-picker",
    min_date_allowed=date(2023, 1, 1),
    max_date_allowed=date.today(),
    initial_visible_month=date.today(),
    display_format="DD/MM/yyyy",
    date=date.today(),
    style={"margin": 20},
)

grafica1 = dbc.Alert(
    [
        html.H2("Total de Demanda Eléctrica Nacional", className="alert-heading"),
        dcc.Graph(id="grafica1", figure=REE.grafIzquierda()),
    ],
    color="primary",
)
grafica2 = dbc.Alert(
    [
        html.H2("Evolucion demanda del periodo", className="alert-heading"),
        dcc.Graph(id="grafica2", figure=REE.grafCentro()),
    ],
    color="primary",
)
grafica3 = dbc.Alert(
    [
        html.H2("Tipo de Energía", className="alert-heading"),
        dcc.Graph(
            id="grafica3",
            figure=REE.grafDerecha(),
        ),
    ],
    color="primary",
)

period = dcc.RadioItems(
    id="radio",
    options=[
        {"label": "Dia", "value": "2"},
        {"label": "Semana", "value": "7"},
        {"label": "Mes", "value": "31"},
    ],
    style={"text-align": "left"},
    value="7",
)
card = dbc.Card(
    [
        dbc.CardHeader("Energía Renovable"),
        dbc.CardBody(
            [
                html.H4("450 GWh", className="card-title"),
                html.P("This is some card text", className="card-text"),
            ]
        ),
        dbc.CardFooter("This is the footer"),
    ],
    style={"width": "auto"},
)

card2 = dbc.Card(
    [
        dbc.CardHeader(html.H5("Demanda Eléctrica Baleares")),
        dbc.CardBody(
            [
                html.H2(
                    "7.46%", style={"text-align": "center"}, className="card-title"
                ),
                html.P("Respecto al consumo eléctrico nacional", className="card-text"),
            ]
        ),
    ],
    style={
        "width": "auto",
    },
)

app.layout = html.Div(
    children=[
        dbc.Stack(
            [
                html.Div(dbc.Row(navbar)),
                html.Br(),
                html.Div(
                    dbc.Row(
                        children=[
                            html.Div(id="my-output"),
                            dbc.Col(calendar),
                            dbc.Col(period),
                        ]
                    ),
                ),
                html.Br(),
                html.Div(
                    [
                        dbc.Row(
                            [
                                dbc.Col(grafica1),
                                dbc.Col(grafica3),
                            ]
                        ),
                        dbc.Row(
                            dbc.Col(grafica2),
                        ),
                    ]
                ),
            ],
            gap=2,
        ),
    ]
)


@app.callback(
    Output(component_id="grafica1", component_property="figure"),
    Output(component_id="grafica2", component_property="figure"),
    Output(component_id="grafica3", component_property="figure"),
    Input(component_id="my-date-picker", component_property="date"),
    Input(component_id="radio", component_property="value"),
)
def update_output_div(input_value, days):
    iv = input_value.split("-")
    df = REE.cargarDataFrame(
        datetime(int(iv[0]), int(iv[1]), int(iv[2]), 23, 59, 0, 0), int(days)
    )

    grafica1 = REE.grafIzquierda()
    grafica2 = REE.grafCentro()
    grafica3 = REE.grafDerecha()
    return grafica1, grafica2, grafica3

if __name__=='__main__':
    app.run_server()
