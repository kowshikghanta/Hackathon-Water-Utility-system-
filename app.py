import flask
from flask import Flask, render_template, request, redirect, session, jsonify
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
    
    html.H3("Leak Status:"),
    html.Div(id="leak_status", style={'font-size': '20px', 'font-weight': 'bold'}),
    
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
     Output("waterlevel_graph", "figure"),
     Output("leak_status", "children"),
     Output("leak_status", "style")],
    [Input("interval", "n_intervals")]
)
def update_graphs(n):
    conn = getdbconnection()
    df = pd.read_sql("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 10", conn)
    conn.close()

    flowfig = go.Figure(data=[go.Scatter(x=df["timestamp"], y=df["flowrate"], mode="lines", name="Flow Rate")])
    flowfig.update_layout(title="Flow Rate", xaxis_title="Time", yaxis_title="Flow Rate (L/min)")

    waterfig = go.Figure(data=[go.Scatter(x=df["timestamp"], y=df["waterlevel"], mode="lines", name="Water Level")])
    waterfig.update_layout(title="Water Level", xaxis_title="Time", yaxis_title="Water Level (cm)")

    if not df.empty and (df["flowrate"].iloc[0] > 10 and df["waterlevel"].iloc[0] < 10):
        leak_status = "⚠️ Leak Detected! Check the system immediately."
        leak_color = "red"
    else:
        leak_status = "✅ No Leak Detected"
        leak_color = "green"

    return flowfig, waterfig, leak_status, {'color': leak_color}

@app.route("/data")
def get_data():
    conn = getdbconnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM sensor_data ORDER BY timestamp DESC LIMIT 10")
    data = cursor.fetchall()
    conn.close()

    formatted_data = [{"timestamp": row[1], "flow_rate": row[2], "water_level": row[3]} for row in data[::-1]]  # Reverse order

    return jsonify(formatted_data)

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True, port=5000)
