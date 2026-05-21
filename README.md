# 2526_Projet1AB_Khess
> [!Note]
> Projet de 1ère année ENSEA sur une caisse enregistreuse pour la K-Fet.

## Sommaire
- [Cahier des charges](#cahier-des-charges)
	- [Caisse enregistreuse portable avec écran tactile](#caisse-enregistreuse-portable-avec-écran-tactile)
	- [Contraintes](#contraintes)
- [Composants](#composants)
- [Modèle 3D de la caisse](#mod%C3%A8le-3d-de-la-caisse)
- [Codes développés](#codes-d%C3%A9velopp%C3%A9s)
- [Technologies utilisées](#technologies-utilis%C3%A9es)
- [Avancée du projet](#avanc%C3%A9e-du-projet)
	- [Ce qui a été réalisé](#ce-qui-a-%C3%A9t%C3%A9-r%C3%A9alis%C3%A9)
	- [Ce qui n'a pas (encore) été réalisé](#ce-qui-na-pas-encore-ete-r%C3%A9alis%C3%A9)
	- [Améliorations possibles](#am%C3%A9liorations-possibles)
- [Membres du projet](#membres-du-projet)
- [Licence](#licence)

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


## Modèle 3D de la caisse
* [Caisse entière avec socle](3D/Caisse%20entière%20avec%20socle.stl) 
* [Module paiement final](3D/Module%20payement%20final.stl)
* [Support tablette final](3D/Support%20tablette%20final.stl)

## Codes développés
* code site internet : voir [Software/Django](Software/Django).
* code de test pour la caisse enregistreuse : voir [Software/Caisse_enregistreuse-teste](Software/Caisse_enregistreuse-teste).

## Technologies utilisées

- Python
- Django
- Raspberry Pi
- KiCad
- Onshape
- Impression 3D
  
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
