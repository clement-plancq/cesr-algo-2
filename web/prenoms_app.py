from flask import Flask
from flask import render_template
from flask import request
import plotly.graph_objs as go
import plotly.io

from prenoms_api import firstnameEvolution

app = Flask(__name__)

api_url = "https://data.centrevaldeloire.fr/api/explore/v2.1/catalog/datasets/prenoms-depuis-1900-centre-val-de-loire/records"

@app.route('/', methods=['GET'])
def prenom_form():
    return render_template('prenom_form.html')

@app.route('/prenom_result', methods=['POST'])
def prenom_result():
    firstname = request.form['firstname']
    res = firstnameEvolution(api_url, firstname, 2000)
    graph = go.Bar(
        x=list(res.keys()), y=list(res.values())
        )
    graph_json = plotly.io.to_json(graph)
    return render_template('prenom_result.html', firstname=firstname, res=res, graph_json=graph_json)