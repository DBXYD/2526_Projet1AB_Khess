# 🔧 Hardware
[![PCB Version](https://img.shields.io/badge/PCB-v1.0-green.svg)](#versions)
[![KiCad](https://img.shields.io/badge/KiCad-9.x-blue?logo=kicad)](#outils)
 
## 📋 Sommaire
- [Schéma d'architecture](#schema-architecture)
- [PCB_Khess_Cash_Drawer](#pcb_khess_cash_drawer)
    - [Schéma](#sch%C3%A9ma)
    - [Liste des composants du PCB](#liste-des-composants-du-pcb)
    - [Liste des composants autres](#liste-des-composants-autres)
    - [Ouverture du tiroir caisse (Raspberry Pi 4)](#ouverture-du-tiroir-caisse-raspberry-pi-4)
    - [PCB](#pcb)
- [PCB_Khess_Module_Payment](#pcb_khess_module_payment)
    - [Schéma](#sch%C3%A9ma-1)
    - [Liste des composants du PCB](#liste-des-composants-du-pcb-1)
    - [Liste des composants autres](#liste-des-composants-autres-1)
    - [Justification des choix techniques](#justification-des-choix-techniques-1)
    - [PCB](#pcb-1)

<a id="schema-architecture"></a>
## 🔎 Schéma d'architecture

Voici une représentation Mermaid du schéma :

```mermaid
flowchart LR
    subgraph Caisse_principale[ Caisse principale ]
        A230(230V AC) --> A12(12V DC)
        A12 --> A5(5V DC)
        A5 --> RPi4[Raspberry Pi 4]
        A12 --> CmdT[Commande tiroir]
        CmdT --> Tiroir[Tiroir caisse]
        RPi4 -->|HDMI| Ecran[Ecran]
        RPi4 -->|GPIO| CmdT
        RPi4 -->|WiFi| Serveur[Serveur]
    end

    subgraph Module_paiement[ Module de paiement ]
        Shield[Shield + gestion batterie] --> RPi0[Raspberry Pi Zero 2W]
        RPi0 -->|HDMI| Ecran2[Ecran]
        RPi0 -->|SPI| RFID[Capteur RFID]
        RPi0 --> Clavier[Clavier]
    end

    RPi4 -->|Bluetooth| RPi0
```

<a id="pcb_khess_cash_drawer"></a>
## 🧾 PCB_Khess_Cash_Drawer
<a id="schéma"></a>
### 🗺️ Schéma
<details>
<summary>Afficher le schéma</summary>

![](/Hardware/PCB_Khess_Cash_Drawer/PCB_Khess_Cash_Drawer.png)

</details>

<a id="liste-des-composants-du-pcb"></a>
### 🔩 Liste des composants du PCB

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

<a id="liste-des-composants-autres"></a>
### 📦 Liste des composants autres

* Tiroir caisse avec connecteur standard RJ11, remplacée par des connecteurs simples
* Câble d'alimentation
* Raspberry Pi 4

## ⚙️ Justification des choix techniques

### 🔌 Architecture d’alimentation

L’alimentation du système est réalisée en deux étapes afin d’assurer une conversion efficace et stable :

1. Conversion du secteur 230V AC vers 12V DC ;
2. Conversion du 12V DC vers 5V DC.

Le module **PSK-15E-12** a été choisi car il permet :
- une intégration compacte directement sur le PCB ;
- une puissance suffisante pour alimenter le tiroir caisse et les circuits logiques.

Le convertisseur **R-78B5.0-2.0** a été préféré à un régulateur linéaire classique pour son excellent rendement énergétique. Cela permet - d’éviter l’ajout d’un dissipateur thermique ;
- d’assurer une alimentation stable du Raspberry Pi.

Les condensateurs et la bobine de filtrage permettent de réduire les parasites haute fréquence et d’améliorer la stabilité des tensions d’alimentation.

### 🛡️ Protections électriques

Plusieurs composants de protection ont été ajoutés afin d’améliorer la robustesse du système :

- le porte-fusible protège la carte en cas de court-circuit ;
- la diode TVS protège contre les surtensions transitoires ;
- la varistance devait initialement renforcer la protection contre les pics secteur ;
- les condensateurs participent au filtrage des perturbations électromagnétiques.

Ces protections sont importantes car le système est directement relié au secteur et pilote une charge inductive.

### ⚡ Commande du tiroir caisse

Le tiroir caisse est commandé via un MOSFET de puissance **BUK9637-100E**. Ce composant a été choisi pour :
- sa faible résistance à l’état passant ;
- sa capacité à commuter des courants importants ;
- sa compatibilité avec les niveaux logiques du Raspberry Pi.

La diode **DST10100S** agit comme diode de roue libre afin d’absorber les surtensions générées lors de la coupure du courant dans l’électroaimant du tiroir caisse.

La résistance de 220 Ω limite le courant de commande du MOSFET tandis que la résistance de 10 kΩ garantit son extinction au démarrage.

<a id="ouverture-du-tiroir-caisse-raspberry-pi-4"></a>
### 🚪 Ouverture du tiroir caisse (Raspberry Pi 4)

L’ouverture du tiroir caisse se fait via le PCB :

1. La **Raspberry Pi 4** envoie un signal de commande sur un **GPIO** ;
2. Le GPIO pilote la grille du **MOSFET** sur le PCB ;
3. Le MOSFET commute l’alimentation **12V** de l’électroaimant du tiroir ;
4. Le tiroir caisse s’ouvre pendant l’impulsion.

Nous n’avions pas de port **RJ11** disponible sur notre montage.  
Nous avons donc remplacé les connecteurs RJ11 par des **pinheaders**.

<a id="pcb"></a>
### 🧩 PCB
<details>
<summary>Voir PCB (face côté avant)</summary>

![](/Hardware/PCB_Khess_Cash_Drawer/PCB_Khess_Cash_Drawer_F.png)

</details>

<details>
<summary>Voir PCB (face arrière)</summary>

![](/Hardware/PCB_Khess_Cash_Drawer/PCB_Khess_Cash_Drawer_B.png)

</details>

---

<a id="pcb_khess_module_payment"></a>
## 🧾 PCB_Khess_Module_Payment
<a id="schéma-1"></a>
### 🗺️ Schéma
<details>
<summary>Afficher le schéma</summary>

![](/Hardware/PCB_Khess_Module_Payment/PCB_Khess_Module_Payment.png)

</details>

<a id="liste-des-composants-du-pcb-1"></a>
### 🔩 Liste des composants du PCB

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

<a id="liste-des-composants-autres-1"></a>
### 📦 Liste des composants autres

* 1 Raspberry Zero 2W
* 1 Écran tactile
* 1 Clavier numérique
* 1 Capteur RFID
* 1 Shield pour gérer une batterie

<a id="justification-des-choix-techniques-1"></a>
### ⚙️ Justification des choix techniques

#### 🖥️ Raspberry Pi Zero 2W

Le Raspberry Pi Zero 2W a été choisi comme unité centrale du module de paiement pour plusieurs raisons :
- faible consommation énergétique ;
- connectivité Wi-Fi intégrée ;
- puissance suffisante pour gérer l’interface utilisateur et les périphériques.

#### 🛰️ Interface RFID

Le module RFID permet l’identification sans contact des utilisateurs.

Le connecteur 01x08 qui permet la comminication via le bus SPI, facilite le remplacement ou la maintenance du module RFID. Le condensateur de 1 µF améliore la stabilité de son alimentation et limite les perturbations lors des communications.

#### 🖱️ Interface écran

L’écran tactile est connecté via une interface dédiée afin de simplifier le montage.

Les résistances de pull-up de 4,7 kΩ servent de résistances de tirage pour les lignes de communication utilisées en I2C.

Le condensateur de 1 µF stabilise l’alimentation de l’écran et réduit les parasites.

#### 🔢 Clavier numérique

Le clavier numérique permet une interaction simple avec l’utilisateur et sert dans le cas où l'utilisateur ne possède pas sa carte.

Les résistances de 10 kΩ sont utilisées comme résistances de rappel afin d’éviter les états flottants sur les entrées numériques.

Les résistances de 330 Ω limitent le courant dans certaines lignes d’interface et protègent les GPIO du Raspberry Pi.

#### 🛡️ Protection et fiabilité

La diode TVS protège les circuits contre les surtensions et les décharges électrostatiques.

Le condensateur de 100 nF placé près du Raspberry Pi assure un découplage haute fréquence.
Les LED servent d’indicateurs visuels.

<a id="pcb-1"></a>
### 🧩 PCB
<details>
<summary>Voir PCB (face avant)</summary>

![](/Hardware/PCB_Khess_Module_Payment/PCB_Khess_Module_Payment_F.png)

</details>

<details>
<summary>Voir PCB (détails couche intérieur 1)</summary>

![](/Hardware/PCB_Khess_Module_Payment/PCB_Khess_Module_Payment_In1.png)

</details>

<details>
<summary>Voir PCB (détails couche intérieur 2)</summary>

![](/Hardware/PCB_Khess_Module_Payment/PCB_Khess_Module_Payment_In2.png)

</details>

<details>
<summary>Voir PCB (face arrière)</summary>

![](/Hardware/PCB_Khess_Module_Payment/PCB_Khess_Module_Payment_B.png)

</details>
