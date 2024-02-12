"""prenoms.py

Travail sur https://data.centrevaldeloire.fr/explore/dataset/prenoms-depuis-1900-centre-val-de-loire/

- Listez les 10 prénoms féminins et les 10 prénoms masculins les plus donnés dans la région en 2022
- Pour 2022, listez les prénoms féminins donnés au moins 5 fois et qui se terminent par 'a'
- Calculez la taille moyenne des prénoms par année
- Écrire une fonction qui donne l’évolution d’un prénom x depuis 2000
"""

import csv
import argparse
from collections import Counter
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

def getData(filename):
    """extracts and returns data from given filename
    
    Parameters
    ----------
    filename: str
        the name of the csv file

    Returns
    -------
    list
        list of dicts
    """
    data = []
    with open(filename, encoding="utf-8") as input_file:
        reader = csv.DictReader(input_file, delimiter=";")
        for line in reader:
            data.append(line)
    return data

def mostCommon(data, top=10):
    """extract the top most common items in data

    Sorts the given dict by value and returns the top `top`

    Parameters
    ----------
    data: dict
        key: prenom, value: nb
    top: int
        number of items to return
    
    Returns
    -------
    list
        list of the top most common items
    """
    # la fonction sorted est utilisée avec 2 arguments : key et reverse
    # reverse=True permet de trier de maniere decroissante
    # key permet de definir une fonction de tri (sur quoi va être effectué le tri)
    # sorted trie une liste, ici le résultat de dict.items()
    # dict.items() renvoie une liste de tuples (2 éléments dans cet ordre : prenom, nb)
    # key reçoit ici une fonction lambda qui renvoie le nb (2e élément du tuple)
    # enfin on transforme cette liste triée en dictionnaire
    sorted_dict = dict(sorted(data.items(), key=lambda x: x[1], reverse=True))

    res = []
    for key, value in sorted_dict.items():
        res.append(f"{key} ({str(value)})")
        if len(res) == top:
            break
    return res

def prenomsFemMasc_2022(data):
    """
    Listez les 10 prénoms féminins et les 10 prénoms masculins les plus donnés dans la région en 2022
    """
    prenoms_fem_2022 = {}
    prenoms_masc_2022 = {}

    for item in data:
        if item["Année de naissance"] == "2022":
            if item["Sexe"] == "Féminin":
                if item["Prénom"] in prenoms_fem_2022:
                    prenoms_fem_2022[item["Prénom"]] += int(item["Nombre de naissances"])
                else:
                    prenoms_fem_2022[item["Prénom"]] = int(item["Nombre de naissances"])
            elif item["Sexe"] == "Masculin":
                if item["Prénom"] in prenoms_masc_2022:
                    prenoms_masc_2022[item["Prénom"]] += int(item["Nombre de naissances"])
                else:
                    prenoms_masc_2022[item["Prénom"]] = int(item["Nombre de naissances"])
    
    top_fem_2022 = mostCommon(prenoms_fem_2022)
    # autre option avec l’objet Counter 
    # plus simple puisque Counter a une fonction `most_common`
    # (https://docs.python.org/3/library/collections.html#collections.Counter)
    counter_masc_2022 = Counter(prenoms_masc_2022)
    top_masc_2022 = counter_masc_2022.most_common(10)
    return (top_fem_2022, top_masc_2022)

def prenomsFem5A(data):
    """
    Pour 2022, listez les prénoms féminins donnés au moins 5 fois et qui se terminent par 'a'
    """
    res = []
    for item in data:
        if item["Année de naissance"] == "2022" and\
            item["Prénom"].endswith("A") and\
            int(item["Nombre de naissances"]) >= 5:
            res.append(item["Prénom"])
    return res

def prenomsAnnee(data):
    res = {}
    for item in data:
        if item["Année de naissance"] not in res:
            res[item["Année de naissance"]] = []
        res[item["Année de naissance"]].append(item["Prénom"])
    return res

def firstnameEvolution(data, firstname, year=2000):
    """
    Computes firstname evolution by year from a set of data
    
    Parameters
    ----------
    data: list of dicts
        key: annee, value: nb
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
    for item in data:
        if item["Prénom"] == firstname and int(item["Année de naissance"]) >= year:
            if item["Année de naissance"] not in res:
                res[item["Année de naissance"]] = 0
            res[item["Année de naissance"]] += int(item["Nombre de naissances"])
    
    return dict(sorted(res.items(), key=lambda x: x[0]))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="csv file")
    args = parser.parse_args()

    data = getData(args.filename)

    # Prénoms les plus donnés en 2022
    top_fem_2022, top_masc_2022 = prenomsFemMasc_2022(data)
    print("Prénoms féminins les plus fréquents en 2022:")
    for item in top_fem_2022:
        print(item)
    print("---\nPrénoms masculins les plus fréquents en 2022:")
    for item in top_masc_2022:
        print(item)

    # prénoms féminins donnés au moins 5 fois en 2022 et qui se terminent par 'a'
    fem_2022_a = prenomsFem5A(data)
    print("---\nPrénoms féminins en 2022 qui se terminent par 'a' et donnés au moins 5 fois:")
    print(", ".join(fem_2022_a))

    # Calculez la taille moyenne des prénoms par année
    print("---\nTaille moyenne des prénoms par année:")
    prenoms_annee = prenomsAnnee(data)
    for year in sorted(prenoms_annee):
        moyenne = sum([len(firstname) for firstname in prenoms_annee[year]]) / len(prenoms_annee[year])
        print(f"Taille moyenne en {year} : {moyenne}")

    # Évolution d’un prénom depuis 2000
    prenom = "FATOUMATA "
    print(f"---\nEvolution du prénom {prenom}:")
    evolution = firstnameEvolution(data, prenom)
    for year in evolution:
        print(f"{year} : {evolution[year]}")
    fig = px.bar(x=evolution.keys(), y=evolution.values(),
         labels={'x':'année', 'y':'nb de naissances'},
         title=f"Évolution du prénom {prenom}")
    fig.show()
    # la même chose avec searborn : génère un graphique de type image
    # plutôt qu’une page web
    #sns.barplot(x=list(evolution.keys()), y=list(evolution.values()))
    #plt.show()

if __name__ == '__main__':
    main()

