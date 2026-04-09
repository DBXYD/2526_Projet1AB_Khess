Voici le code : 

```bash
// --- TABLES UTILISATEURS (Bleu) ---
Table User {
  id integer [primary key]
  username varchar
}

Table users_custom {
  id integer [primary key]
  user_id integer [ref: - User.id]
  first_name varchar
  last_name varchar
  sold float
  class_name varchar
  nb_transaction integer
  role varchar // admin, respo, student
  status varchar // cotisant, non_cotisant, prof
  created_at timestamp
}

// --- GESTION DES PRODUITS ET MENUS (Vert) ---
Table Article {
  id integer [primary key]
  name varchar
  quantity integer
  type varchar // le midi, boisson, snack, viennoiseries
  price_cotisant float
  price_non_cotisant float
}

Table Menu {
  id integer [primary key]
  name varchar
  price float
}

Table MenuDetails {
  id integer [primary key]
  menu_id integer [ref: > Menu.id]
  article_id integer [ref: > Article.id]
}

// --- SYSTÈME DE VENTES (Orange) ---
Table Transaction {
  id integer [primary key]
  user_id integer [ref: > User.id]
  price float
  created_at timestamp
}

Table TransactionDetails {
  id integer [primary key]
  transaction_id integer [ref: > Transaction.id]
  user_id integer [ref: > User.id]
  article_id integer [ref: > Article.id]
  type varchar
  quantity integer
  price float
  payment_type varchar // cash, card
  created_at timestamp
}

// --- COMPTABILITÉ (Gris) ---
Table Cash {
  id integer [primary key]
  sold_cash float
  gain_card float
  gain_cash float
  total float
}
```

1 (Obligatoire) : L'élément doit exister. Un badge de la K-FET est forcément attaché à 1 personne. Il ne peut pas être "orphelin".
0..1 (Optionnel) : L'élément peut exister ou non. Une personne peut avoir 0 badge (si elle n'est pas inscrite) ou 1 badge maximum.

## Les différents liens : 

1. User ↔ users_custom : Un utilisateur ne peut avoir qu'un seul profil users_custom car son solde et son statut (cotisant ou non) doivent être uniques pour éviter les erreurs de compte.
2. User ↔ Transaction : Un utilisateur peut faire plusieurs transactions car il peut venir acheter à la K-FET plusieurs fois par jour ou par an.
3. Transaction ↔ TransactionDetails : Une seule transaction peut avoir plusieurs détails car un client peut acheter plusieurs articles différents en un seul passage en caisse.
4.Article ↔ TransactionDetails : Un même article peut être relié à plusieurs lignes de détails car le même produit (ex: un café) est vendu à plein de clients différents.
5.Menu ↔ MenuDetails : Un menu peut être lié à plusieurs articles (via les détails) car une "Formule Midi" est composée de plusieurs produits comme un plat, une boisson et un dessert.
6.Article ↔ MenuDetails : Un article peut appartenir à plusieurs menus car un même soda peut faire partie de la "Formule Snack" et de la "Formule Midi".

