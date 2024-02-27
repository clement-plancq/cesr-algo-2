"""
Séance 7
Utilisez l’API de https://data.education.gouv.fr/explore/dataset/fr-en-ips_lycees/ pour lister par ordre décroissant les IPS des lycées de Tours (ou de la ville qui vous plaira)
"""

import requests

def main():

    api_url = "https://data.education.gouv.fr/api/explore/v2.1/catalog/datasets/fr-en-ips_lycees/records"

    params = {
        'select': 'nom_de_l_etablissment, ips_ensemble_gt_pro',
        'where': "rentree_scolaire = '2021-2022' and nom_de_la_commune = 'TOURS'", 'limit': '-1', 'order_by': 'ips_ensemble_gt_pro desc'
        }

    r = requests.get(api_url, params=params)
    #print(r.url)
    if r:
        res = r.json()
        for item in res['results']:
            print(f"{item['nom_de_l_etablissment']} : {item['ips_ensemble_gt_pro']}")
    else:
        print(f"Pas de résultats pour la requête.\nStatus code : {r.status_code}")
if __name__ == '__main__':
    main()