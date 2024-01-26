# Changelog
# 26/12/2023: Clase hecha(por ahora recoge del primer mes del 2023 y solo dos requests, lo iré cambiando para que sea los últimos siete dias desde que se
# ejecuta y tenga alguna columna más que sea interesante y coherente con los datos)
# 01/01: Arreglo de un request( ahora solo muestra renovable, de un solo tipo, hidraulica)
# 03/01: Ahora se actualiza la fecha automaticamente, es decir, recoge los datos a partir de hoy y de hace 6 días
#

import json
import pandas as pd
import requests
from datetime import datetime, timedelta

#
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, callback
from dash import dcc
import plotly.graph_objects as go
import plotly.express as px
from dash.dependencies import Input, Output


# Enlace de la página de la API a consultar: https://www.ree.es/es/apidatos
class Ree(object):
    def cargarDataFrame(self, dt=datetime.now(), days=7):
        today = dt
        today2 = today.replace(second=0, microsecond=0)
        days = days - 1
        d = today - timedelta(days=days)
        d = d.replace(second=0, microsecond=0)

        iso_date = today2.isoformat()
        iso_date2 = d.isoformat()

        r = requests.get(
            "https://apidatos.ree.es/es/datos/balance/balance-electrico?start_date="
            + iso_date2[:-3]
            + "&end_date="
            + iso_date[:-3]
            + "&time_trunc=day"
        )
        x = json.loads(r.text)
        df2 = pd.json_normalize(x, ["included"])
        for i in range(0, 2):
            y = df2["attributes.content"][i]  # 0
            for c in range(0, len(y)):
                z = y[c]
                z2 = z.get("attributes")
                f = z2.get("values")
                balance_elec_rnv = pd.json_normalize(f)
                balance_elec_rnv["type"] = z["type"]
                if (c + i) == 0:
                    df = balance_elec_rnv.copy()
                else:
                    df = pd.concat([df, balance_elec_rnv], axis=0)
        self.data = df

        return df

    def grafIzquierda(self):
        grafI = px.bar(
            self.data[
                (self.data["type"] == "Generación no renovable")
                | (self.data["type"] == "Generación renovable")
            ],
            x="datetime",
            y="value",
            color="type",
        )

        grafI.update_layout(
            yaxis_title=dict(
                text="Balance eléctrico (GWh)",
                font=dict(
                    family="Arial",
                    size=16,
                    color="black",
                ),
            ),
            xaxis_title="Periodo",
        )
        return grafI

    def grafCentro(self):
        grafC = px.line(
            self.data[
                (self.data["type"] != "Generación no renovable")
                & (self.data["type"] != "Generación renovable")
            ],
            x="datetime",
            y="value",
            color="type",
            line_group="type",
        )

        grafC.update_layout(
            yaxis_title=dict(
                text="Consumo eléctrico (GWh)",
                font=dict(
                    family="Arial",
                    size=16,
                    color="black",
                ),
            ),
            xaxis_title="Periodo",
        )

        return grafC

    def grafDerecha(self):
        grafD = px.pie(
            self.data[
                (self.data["type"] == "Generación no renovable")
                | (self.data["type"] == "Generación renovable")
            ],
            values="value",
            names="type",
        )

        return grafD
