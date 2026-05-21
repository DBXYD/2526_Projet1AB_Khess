# Hardware
 
## Sommaire
- [PCB_Khess_Cash_Drawer](#pcb_khess_cash_drawer)
    - [Schéma](#sch%C3%A9ma)
    - [Liste des composants du PCB](#liste-des-composants-du-pcb)
    - [Liste des composants autres](#liste-des-composants-autres)
    - [PCB](#pcb)
- [PCB_Khess_Module_Payment](#pcb_khess_module_payment)
    - [Schéma](#sch%C3%A9ma-1)
    - [Liste des composants du PCB](#liste-des-composants-du-pcb-1)
    - [Liste des composants autres](#liste-des-composants-autres-1)
    - [PCB](#pcb-1)

## PCB_Khess_Cash_Drawer
### Schéma
![](/Hardware/PCB_Khess_Cash_Drawer/PCB_Khess_Cash_Drawer.png)

### Liste des composants du PCB

* Convertisseur 12V à 5V DC
    * 1 Convertisseur R-78B5.0-2.0 ([datasheet](/Datasheets/PCB_Khess_Cash_Drawer/R-78B-2.0.pdf))
    * 1 Condensateur 10uF
    * 1 Condensateur 4,7uF
    * 1 Bobine 10uH

* Conventisseur 230V à 12V DC
    * 1 Porte-fusible
    * 1 Convertisseur PSK-15E-12 ([datasheet](/Datasheets/PCB_Khess_Cash_Drawer/psk-15e.pdf))
    * 1 Condensateur 100uF
    * 1 Condensateur 1uF
    * 1 Diode TVS (824 500 500) ([datasheet](/Datasheets/PCB_Khess_Cash_Drawer/824500500.pdf))
    * 1 Résistance bobinée 6,8 Ohm (remplacée par un fil) ([datasheet](/Datasheets/PCB_Khess_Cash_Drawer/ac_ac-at_ac-ni.pdf))
    * 1 Varistance TVS 10D561K (non mise) ([datasheet](/Datasheets/PCB_Khess_Cash_Drawer/mov10d.pdf))

* Commande du tiroir caisse
    * 1 Diode DST10100S ([datasheet](/Datasheets/PCB_Khess_Cash_Drawer/littelfuse-rectifier-DST10100S-datasheet.pdf))
    * 1 Transistor BUK9637-100E,118 ([datasheet](/Datasheets/PCB_Khess_Cash_Drawer/BUK9637-100E.pdf))
    * 1 Résistance 220 Ohm
    * 1 Résistance 10k Ohm

* Connecteurs
    * 1 Connecteur 01x03
    * 1 Connecteur RJ11, remplacée par 1 Connecteur 01x02
    * 1 Bornier à vis 01x02
    * 1 Écran tactile

### Liste des composants autres

* Tiroir caisse avec connecteur standard RJ11, remplacée par des connecteurs simples
* Câble d'alimentation
* Raspberry Pi 5

## Justification des choix techniques

### Architecture d’alimentation

L’alimentation du système est réalisée en deux étapes afin d’assurer une conversion efficace et stable :

1. Conversion du secteur 230V AC vers 12V DC ;
2. Conversion du 12V DC vers 5V DC.

Le module **PSK-15E-12** a été choisi car il permet :
- une intégration compacte directement sur le PCB ;
- une puissance suffisante pour alimenter le tiroir caisse et les circuits logiques.

Le convertisseur **R-78B5.0-2.0** a été préféré à un régulateur linéaire classique pour son excellent rendement énergétique. Cela permet - d’éviter l’ajout d’un dissipateur thermique ;
- d’assurer une alimentation stable du Raspberry Pi.

Les condensateurs et la bobine de filtrage permettent de réduire les parasites haute fréquence et d’améliorer la stabilité des tensions d’alimentation.

### Protections électriques

Plusieurs composants de protection ont été ajoutés afin d’améliorer la robustesse du système :

- le porte-fusible protège la carte en cas de court-circuit ;
- la diode TVS protège contre les surtensions transitoires ;
- la varistance devait initialement renforcer la protection contre les pics secteur ;
- les condensateurs participent au filtrage des perturbations électromagnétiques.

Ces protections sont importantes car le système est directement relié au secteur et pilote une charge inductive.

### Commande du tiroir caisse

Le tiroir caisse est commandé via un MOSFET de puissance **BUK9637-100E**. Ce composant a été choisi pour :
- sa faible résistance à l’état passant ;
- sa capacité à commuter des courants importants ;
- sa compatibilité avec les niveaux logiques du Raspberry Pi.

La diode **DST10100S** agit comme diode de roue libre afin d’absorber les surtensions générées lors de la coupure du courant dans l’électroaimant du tiroir caisse.

La résistance de 220 Ω limite le courant de commande du MOSFET tandis que la résistance de 10 kΩ garantit son extinction au démarrage.

### PCB
![](/Hardware/PCB_Khess_Cash_Drawer/PCB_Khess_Cash_Drawer_F.png)
![](/Hardware/PCB_Khess_Cash_Drawer/PCB_Khess_Cash_Drawer_B.png)

---

## PCB_Khess_Module_Payment
### Schéma
![](/Hardware/PCB_Khess_Module_Payment/PCB_Khess_Module_Payment.png)

### Liste des composants du PCB

* Raspberry Pi
    * 1 Connecteur 02x20
    * 1 Diode TVS (824 500 500) ([datasheet](/Datasheets/PCB_Khess_Cash_Drawer/824500500.pdf))
    * 2 Résistances 470 Ohm
    * 2 LED
    * 1 Condensateur 100nF

* RFID
    * 1 Connecteur 01x08
    * 1 Condensateur 1uF

* Écran
    * 1 Condensateur 1uF
    * 1 Connecteur 01x04
    * 2 Résistances 4,7k Ohm

* Clavier numérique
    * 4 Résistances 10k Ohm
    * 4 Résistances 330 Ohm
    * 1 Connecteurs 01x08

### Liste des composants autres

* 1 Raspberry Zero 2W
* 1 Écran tactile
* 1 Clavier numérique
* 1 Capteur RFID
* 1 Shield pour gérer une batterie

### PCB
![](/Hardware/PCB_Khess_Module_Payment/PCB_Khess_Module_Payment_F.png)
![](/Hardware/PCB_Khess_Module_Payment/PCB_Khess_Module_Payment_In1.png)
![](/Hardware/PCB_Khess_Module_Payment/PCB_Khess_Module_Payment_In2.png)
![](/Hardware/PCB_Khess_Module_Payment/PCB_Khess_Module_Payment_B.png)

