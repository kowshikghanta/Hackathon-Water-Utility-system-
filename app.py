import flask
from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from dash import html, dcc
import dash
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import pandas as pd
from modules.auth import checklogin
from modules.utils import getdbconnection


app = Flask(__name__)
app.secret_key = "supersecretkey"

dashapp = dash.Dash(__name__, server=app, url_base_pathname="/graphs/")
dashapp.layout = html.Div([
    html.H1("Live Sensor Data"),
    dcc.Graph(id="flowrate_graph"),
    dcc.Graph(id="waterlevel_graph"),
    dcc.Interval(id="interval", interval=2000, n_intervals=0)
])

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if checklogin(username, password):
            session["user"] = username
            return redirect("/dashboard")
        return "Invalid credentials"
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html")

@dashapp.callback(
    [Output("flowrate_graph", "figure"),
     Output("waterlevel_graph", "figure")],
    [Input("interval", "n_intervals")]
)
def update_graphs(n):
    conn = getdbconnection()
    df = pd.read_sql("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 10", conn)
    conn.close()

    flow_fig = go.Figure(data=[go.Scatter(x=df["timestamp"], y=df["flowrate"], mode="lines", name="Flow Rate")])
    flow_fig.update_layout(title="Flow Rate", xaxis_title="Time", yaxis_title="Flow Rate (L/min)")

    water_fig = go.Figure(data=[go.Scatter(x=df["timestamp"], y=df["waterlevel"], mode="lines", name="Water Level")])
    water_fig.update_layout(title="Water Level", xaxis_title="Time", yaxis_title="Water Level (cm)")

    return flow_fig, water_fig

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
