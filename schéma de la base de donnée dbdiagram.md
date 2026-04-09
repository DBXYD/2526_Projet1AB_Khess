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
