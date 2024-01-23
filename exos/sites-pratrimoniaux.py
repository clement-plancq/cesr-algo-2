"""
Exercice séance 2 - Sites pratrimoniaux
Téléchargez le fichier csv disponible à l’url https://data.culture.gouv.fr/explore/dataset/liste-des-sites-patrimoniaux-remarquables-spr/
Utilisez le module csv et une ou des listes pour extraire les communes, départements et numéros de SPR dans la région Centre Val-de-Loire. Vous exporterez le résultat dans un nouveau fichier csv.
"""

import csv

def main():
    spr_cvl = []

    with open('../data/liste-des-sites-patrimoniaux-remarquables-spr.csv') as input_file:
        csv_reader = csv.DictReader(input_file, delimiter=';')
        for row in csv_reader:
            if row['Région'] == "CENTRE-VAL DE LOIRE":
                spr_cvl.append(row)

    with open('../data/liste-des-sites-patrimoniaux-remarquables-spr-cvl.csv', 'w') as output_file:
        fieldnames = ['Département', 'Commune', 'Numéro du SPR']
        csv_writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for item in spr_cvl:
            csv_writer.writerow({'Département': item['Département'], 'Commune': item['Commune'], 'Numéro du SPR': item['numéro du SPR']})

if __name__ == '__main__':
    main()