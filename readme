# **Algorithme de Préparation des Commandes - Jules Entrepos**

Ce projet implémente un algorithme de préparation de commandes pour l'entrepôt logistique de l'entreprise Jules, spécialisée dans la vente de prêt-à-porter. Le but est de minimiser la distance parcourue par les préparateurs tout en respectant les contraintes de capacité des colis et des chariots.

## **Table des matières**
1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Utilisation](#utilisation)
4. [Structure du Projet](#structure-du-projet)
5. [Données](#données)
6. [Exécution](#exécution)
7. [Tests](#tests)
8. [Exemple](#exemple)
9. [Améliorations Futures](#améliorations-futures)

---

## **Introduction**

Le but de ce projet est de générer des solutions efficaces pour la préparation des commandes dans l'entrepôt de Jules. Ces solutions permettent de :
- Répartir les produits dans des colis en respectant les contraintes de poids et de volume.
- Regrouper les colis sur des chariots ayant une capacité maximale.
- Optimiser les tournées des préparateurs pour minimiser les distances parcourues.

Le projet prend en charge des fichiers d'instances décrivant les produits, les commandes, et l'entrepôt. À partir de ces données, il génère des fichiers de solutions décrivant comment les articles sont préparés et collectés.

---

## **Installation**

### **Pré-requis**
- Python 3.8 ou plus
- Les bibliothèques Python suivantes :
  - `logging`
  - `unittest`

### **Étapes d'installation**

1. Clonez ce dépôt Git localement :
   ```bash
   git clone https://github.com/JulienZammit/order-picking-algorithm-gates
   ```

2. Accédez au répertoire du projet :
   ```bash
   cd order-picking-algorithm-gates
   ```

3. (Optionnel) Créez et activez un environnement virtuel :
   ```bash
   python -m venv env
   source env/bin/activate  # Sur Windows: env\Scripts\activate
   ```

---

## **Utilisation**

Le projet est conçu pour fonctionner à partir d'un script principal (`main.py`) qui analyse les fichiers d'instance, génère les solutions et les valide.

### **Étapes pour utiliser le projet :**

1. **Préparer les données d'instance** :  
   Les fichiers d'instance doivent être placés dans le dossier `data/instances/`. Chaque fichier contient des informations sur les produits, les commandes et l'entrepôt.

2. **Exécuter le script principal** :  
   Lancez le programme principal pour analyser les fichiers d'instances et générer les solutions correspondantes :
   ```bash
   python src/main.py
   ```

3. **Consulter les résultats** :  
   Les fichiers de solutions générés seront enregistrés dans le dossier `data/solutions/` avec le format `_sol.txt`.

---

## **Structure du Projet**

- **src/** : Contient le code source du projet.
  - `main.py` : Point d'entrée du programme. Exécute l'analyse des fichiers et la génération des solutions.
  - **algorithmes/** : Contient l'algorithme de répartition des produits dans les colis et des colis dans les chariots.
    - `algorithme_picking.py` : Implémente les algorithmes de picking (répartition et optimisation).
  - **models/** : Contient les classes principales du projet.
    - `produit.py` : Représente un produit.
    - `commande.py` : Représente une commande client.
    - `colis.py` : Gère les colis contenant les produits.
    - `chariot.py` : Gère les chariots utilisés pour regrouper les colis.
    - `tournee.py` : Représente une tournée de picking.
    - `graphe_entrepot.py` : Modélise l'entrepôt et les déplacements à l'intérieur.
  - **utils/** : Contient des fonctions utilitaires, comme les constantes et la validation.
    - `constantes.py` : Contient les constantes liées aux capacités des colis et des chariots.
    - `validation.py` : Valide la solution générée.

- **tests/** : Contient les tests unitaires du projet.
  - `test_generateur_solutions.py` : Teste la génération des fichiers de solution.
  - `test_analyseur_instances.py` : Teste l'analyse des fichiers d'instance.

- **data/** : Contient les fichiers d'instances et de solutions.
  - **instances/** : Fichiers d'instance à analyser.
  - **solutions/** : Fichiers de solutions générés.

---

## **Données**

### **Fichiers d'instances**

Les fichiers d'instances décrivent l'entrepôt, les produits et les commandes à préparer. Voici les sections attendues dans un fichier d'instance :
- `NbLocations` : Nombre de localisations dans l'entrepôt.
- `NbProducts` : Nombre de produits stockés.
- `NbOrders` : Nombre de commandes à traiter.
- `B: CapaBox` : Capacités maximales des colis (poids et volume).
- `K: NbBoxOnCart` : Capacité des chariots en nombre de colis.

### **Fichiers de solutions**

Les fichiers de solutions générés contiennent :
- Le nombre de tournées.
- Pour chaque tournée, les colis associés et les produits à ramasser avec leurs quantités.

---

## **Exécution**

### **Étapes pour exécuter une analyse complète :**

1. Placez vos fichiers d'instances dans le dossier `data/instances/`.
2. Exécutez le script principal avec la commande suivante :
   ```bash
   python src/main.py
   ```
3. Les fichiers de solutions seront générés dans le dossier `data/solutions/`.

### **Vérification des résultats :**
- Un message dans la console indique si la solution générée pour chaque fichier d'instance est valide ou non.

---

## **Tests**

Le projet inclut des tests unitaires pour vérifier le bon fonctionnement de l'algorithme et des composants du projet.

### **Exécuter les tests :**

Pour lancer tous les tests, utilisez la commande suivante :
```bash
python -m unittest discover -s tests
```

Les tests valident notamment :
- L'analyse correcte des fichiers d'instance.
- La génération correcte des fichiers de solution.
- La répartition des produits dans les colis et la validation des solutions.

---

## **Exemple**

Exemple d'une exécution réussie pour un fichier d'instance :

```bash
python src/main.py
```

Sortie attendue :
```
INFO:Traitement de l'instance : instance_0116.txt
INFO:Analyse du fichier d'instance: data/instances/instance_0116.txt
INFO:Fin de l'analyse du fichier. Produits lus: 166, Commandes lues: 2
INFO:Solution pour instance_0116.txt est valide.
```

---

## **Améliorations Futures**

- Amélioration de l'algorithme de répartition des produits pour minimiser encore plus les distances.
- Implémentation d'un système d'analyse de performance pour comparer les différentes solutions générées.
- Optimisation des logs pour traiter des fichiers d'instances plus grands et complexes.
