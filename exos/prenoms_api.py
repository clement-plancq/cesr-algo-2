"""
Séance 7
Utilisez le module requests et l’API de prenoms pour afficher un graphe du nombre de naissances depuis 2000 pour un prénom donné
"""

import requests
import argparse
import plotly.express as px


def firstnameEvolution(api, firstname, year=2000):
    res = {}
    params = {'select': 'prenom, nombre_de_naissances, annee_triable, nom_officiel_departement', 'where': f"prenom = '{firstname}'", 'limit': '-1'}

    r = requests.get(api, params=params)
    #print(r.url)
    if r:
        api_res = r.json()
        for item in api_res['results']:
            if int(item["annee_triable"]) >= year:
                if item["annee_triable"] not in res:
                    res[item["annee_triable"]] = 0
                res[item["annee_triable"]] += int(item["nombre_de_naissances"])
        return dict(sorted(res.items(), key=lambda x: x[0]))
    else:
        return None

def displayGraph(data, prenom):
    fig = px.bar(x=data.keys(), y=data.values(),
         labels={'x':'année', 'y':'nb de naissances'},
         title=f"Évolution du prénom {prenom}")
    fig.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prenom", help="Le prénom à rechercher")
    args = parser.parse_args()
    prenom = args.prenom

    api_url = "https://data.centrevaldeloire.fr//api/explore/v2.1/catalog/datasets/prenoms-depuis-1900-centre-val-de-loire/records"

    prenom_data = firstnameEvolution(api_url, prenom)
    if prenom_data:
        print(prenom_data)
        displayGraph(prenom_data, prenom)
    else:
        print(f"Pas de données pour {prenom}")

if __name__ == '__main__':
    main()