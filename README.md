# 2526_Projet1AB_Khess
> [!Note]
> Projet de 1ère année ENSEA sur une caisse enregistreuse pour la K-Fet.

## Cahier des charges
### Caisse enregistreuse portable avec écran tactile
* Interface utilisateur intuitive
* Gestion des produits et des prix
* Paiement avec carte étudiante

### Contraintes
* Portabilité (batterie) : terminal de paiement
* Fiabilité des transactions
* Sécurité des données

## Composants
Voir [Hardware/README.md](Hardware/README.md).


## Modèle 3D de la caisse (liens onshape)
* caisse : Voir [Caisse entière avec socle.stl](Caisse entière avec socle.stl).
* module de paiement : https://cad.onshape.com/documents/279f59e2f2ffc111bf11212e/w/8f97b6e779ccb8f32fd35210/e/959d8722d16775ab3e654e7e?renderMode=0&uiState=6a0e3c683f317a82c571ae84
* changement support tablette : https://cad.onshape.com/documents/76ad7ea018552db6a3f1dc99/w/96b32424fd40eb196727c949/e/cde944de5d408b099ab94c4d?renderMode=0&uiState=6a0e3c51ea0349263bbd5f3c

## Codes développés
* code site internet : voir [Software/Django](Software/Django).
* code de test pour la caisse enregistreuse : voir [Software/Caisse_enregistreuse-teste](Software/Caisse_enregistreuse-teste).

## Avancée du projet
### Ce qui a été réalisé

* prise en main du projet
* création des PCB
* soudure des PCB
* développement du site internet/ interface vendeur avec gestion des stocks, des commandes
* modification 3D de la caisse en changeant les dimensions du socle soutenant la tablette
* modélisation 3D du module de paiement avec plusieurs variantes afin de correspondre à la taille du PCB contenu à l'intérieur
* développement du code du module de payement
* modification 3D de la caisse en changeant le support tablette se mettant sur le socle

## Technologies utilisées

- Python
- Django
- Raspberry Pi
- KiCad
- Onshape
- Impression 3D
  
### Ce qui n'a pas (encore) été réalisé

* test du PCB
* assemblage de l'ensemble

### Améliorations possibles

* revoir le design de la caisse
* améliorer le site internet

## Membres du projet

| <img src="https://images.weserv.nl/?url=github.com/Ahhj93.png&mask=circle" width="100"> | <img src="https://images.weserv.nl/?url=github.com/NKRIMAT.png&mask=circle" width="100"> | <img src="https://images.weserv.nl/?url=github.com/Margaux-Lapl.png&mask=circle" width="100"> | <img src="https://images.weserv.nl/?url=github.com/StrangeKobe.png&mask=circle" width="100"> | <img src="https://images.weserv.nl/?url=github.com/zhang-estelle.png&mask=circle" width="100"> | <img src="https://images.weserv.nl/?url=github.com/ClementJ493.png&mask=circle" width="100"> | <img src="https://images.weserv.nl/?url=github.com/rim-05-mma.png&mask=circle" width="100"> |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| [@Ahhj93](https://github.com/Ahhj93)<br>Bryan-Sowanna Ing | [@NKRIMAT](https://github.com/NKRIMAT)<br>Naïm Krimat | [@Margaux-Lapl](https://github.com/Margaux-Lapl)<br>Margaux Laplante | [@StrangeKobe](https://github.com/StrangeKobe)<br>Rayan Laghouane | [@zhang-estelle](https://github.com/zhang-estelle)<br>Estelle Zhang | [@ClementJ493](https://github.com/ClementJ493)<br>Clément Jouneau | [@rim-05-mma](https://github.com/rim-05-mma)<br>Rim Bouchikhi |
## Licence

Projet académique ENSEA — usage pédagogique.
