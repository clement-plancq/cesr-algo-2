"""
Séance 7
Utilisez le module requests et l’API de prenoms pour afficher un graphe du nombre de naissances depuis 2000 pour un prénom donné
"""

import requests
import argparse
import plotly.express as px


def firstnameEvolution(api, firstname, year=2000):
    """
    Computes firstname evolution by year with one or several calls to the given API

    Parameters
    ----------
    api: url of the API
    firstname: string
        the firstname to match
    year: int
        start year (default: 2000)
    
    Returns
    -------
    dict
        dict of births number by year
    """

    res = {}
    offset = 0 
    tmp_res = [] # liste temporaire pour stocker les résultats de l’appel à l’API

    params = {'select': 'prenom, nombre_de_naissances, annee_triable, nom_officiel_departement', 'where': f"prenom = '{firstname}'", 'limit': -1, 'offset': offset}
    r = requests.get(api, params=params)
    #print(r.url)
    if r:
        api_res = r.json()
        ## L’API renvoie 100 résultats par appel au maximum
        ## Si le nombre de résultats est superieur à 100, on doit appeler l’API plusieurs fois
        if api_res['total_count'] < 100:
            tmp_res = api_res['results']
        else:
            tmp_res.extend(api_res['results']) # on utilise 'extend' plutôt que 'append' pour  « aplatir »
                                               # les listets résultats
            hundreds = api_res['total_count'] // 100 # // : division entière
            for i in range(1, hundreds + 1):
                offset = i * 100
                params = {'select': 'prenom, nombre_de_naissances, annee_triable, nom_officiel_departement', 'where': f"prenom = '{firstname}'", 'limit': -1, 'offset': offset}
                r = requests.get(api, params=params)
                if r:
                    #print(r.url)
                    api_res = r.json()
                    tmp_res.extend(api_res['results'])

        for item in tmp_res:
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

    api_url = "https://data.centrevaldeloire.fr/api/explore/v2.1/catalog/datasets/prenoms-depuis-1900-centre-val-de-loire/records"

    prenom_data = firstnameEvolution(api_url, prenom)

    if prenom_data:
        displayGraph(prenom_data, prenom)
    else:
        print(f"Pas de données pour {prenom}")

if __name__ == '__main__':
    main()