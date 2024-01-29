"""
https://www.codingame.com/ide/puzzle/mime-type
"""

import sys
import math

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

mime_dico = dict()
n = int(input())  # Number of elements which make up the association table.
q = int(input())  # Number Q of file names to be analyzed.

# stockage des types mime dans le dictionnaire
for i in range(n):
    # ext: file extension
    # mime: MIME type
    ext, mime = input().split()
    mime_dico[ext.lower()] = mime
    
#print(repr(mime_dico), file=sys.stderr)

# pour chaque nom de fichier
for i in range(q):
    fname = input()  # One file name per line.
    chops = fname.split('.') # on divise le nom de fichier en plusieurs parties
    # on ne garde que la dernière partie (l’extension)
    ext = chops[-1].lower() if len(chops) > 1 else None 
    # utilisation de la fonction `get` qui permet de renvoyer une valeur par defaut
    # si la clé n'existe pas
    print(mime_dico.get(ext, "UNKNOWN"))
