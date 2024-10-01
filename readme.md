# **Algorithme de Préparation des Commandes - Jules Entrepos**

Ce projet implémente un algorithme de préparation de commandes pour l'entrepôt logistique de l'entreprise Jules, spécialisée dans la vente de prêt-à-porter. L'objectif est de minimiser la distance parcourue par les préparateurs tout en respectant les contraintes de capacité des colis et des chariots.

---

## **Table des matières**

1. [Introduction](#introduction)
2. [Installation](#installation)
3. [Utilisation](#utilisation)
4. [Structure du Projet](#structure-du-projet)
5. [Données](#données)
6. [Exécution](#exécution)
7. [Tests](#tests)
8. [Validation des Solutions](#validation-des-solutions)
9. [Analyse des Résultats](#analyse-des-résultats)
10. [Exemple](#exemple)
11. [Améliorations Futures](#améliorations-futures)
12. [Contact](#contact)

---

## **Introduction**

Le but de ce projet est de générer des solutions efficaces pour la préparation des commandes dans l'entrepôt de Jules. Ces solutions permettent de :

- **Répartir les produits dans des colis** en respectant les contraintes de poids et de volume.
- **Regrouper les colis sur des chariots** ayant une capacité maximale.
- **Optimiser les tournées des préparateurs** pour minimiser les distances parcourues.

Le projet prend en charge des fichiers d'instances décrivant les produits, les commandes et l'entrepôt. À partir de ces données, il génère des fichiers de solutions décrivant comment les articles sont préparés et collectés.

---

## **Installation**

### **Pré-requis**

- **Python 3.8** ou plus récent
- Les bibliothèques Python suivantes :
  - `logging`
  - `unittest`
  - `pandas` (pour l'analyse des résultats)
- **Java** (pour exécuter le checker de validation)

### **Étapes d'installation**

1. **Cloner ce dépôt Git localement** :
   ```bash
   git clone https://github.com/JulienZammit/order-picking-algorithm-gates.git
   ```

2. **Accéder au répertoire du projet** :
   ```bash
   cd order-picking-algorithm-gates
   ```

3. **(Optionnel) Créer et activer un environnement virtuel** :
   ```bash
   python -m venv env
   source env/bin/activate  # Sur Windows: env\Scripts\activate
   ```

4. **Installer les dépendances nécessaires** :
   ```bash
   pip install -r requirements.txt
   ```
   **Remarque** : Si le fichier `requirements.txt` n'existe pas, vous pouvez installer `pandas` manuellement :
   ```bash
   pip install pandas
   ```

---

## **Utilisation**

Le projet est conçu pour fonctionner à partir d'un script principal (`main.py`) qui analyse les fichiers d'instances, génère les solutions et les valide.

### **Étapes pour utiliser le projet :**

1. **Préparer les données d'instances** :  
   Les fichiers d'instances doivent être placés dans le dossier `data/instances/`. Chaque fichier contient des informations sur les produits, les commandes et l'entrepôt.

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
  - **utils/** : Contient des fonctions utilitaires.
    - `validation.py` : Valide la solution générée.
  - **generateur_solutions.py** : Gère la génération des fichiers de solution.
  - **analyseur_instances.py** : Gère l'analyse des fichiers d'instances.

- **tests/** : Contient les tests unitaires du projet.
  - `test_generateur_solutions.py` : Teste la génération des fichiers de solution.
  - `test_analyseur_instances.py` : Teste l'analyse des fichiers d'instance.

- **data/** : Contient les fichiers d'instances, de solutions et le checker Java.
  - **instances/** : Fichiers d'instances à analyser.
  - **solutions/** : Fichiers de solutions générés.
  - **checker/** : Contient le checker Java (`CheckerBatchingPicking.jar`) pour valider les solutions.

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

1. **Placez vos fichiers d'instances** dans le dossier `data/instances/`.

2. **Exécutez le script principal** avec la commande suivante :
   ```bash
   python src/main.py
   ```

3. **Les fichiers de solutions seront générés** dans le dossier `data/solutions/`.

### **Vérification des résultats :**

- Un message dans la console indique si la solution générée pour chaque fichier d'instance est valide ou non.
- Les logs détaillés sont enregistrés dans le fichier `debug.log` à la racine du projet.

---

## **Tests**

Le projet inclut des tests unitaires pour vérifier le bon fonctionnement de l'algorithme et des composants du projet.

### **Exécuter les tests :**

Pour lancer tous les tests, utilisez la commande suivante :
```bash
python -m unittest discover -s tests
```

**Remarque** : Assurez-vous que le répertoire `src` est correctement ajouté au chemin de recherche des modules dans les tests. Les fichiers `__init__.py` doivent être présents dans les répertoires `src/` et `src/models/` pour que Python reconnaisse ces dossiers comme des packages.

Les tests valident notamment :

- L'analyse correcte des fichiers d'instances.
- La génération correcte des fichiers de solution.
- La répartition des produits dans les colis et la validation des solutions.

---

## **Validation des Solutions**

Un checker Java est fourni pour valider les solutions générées. Il permet de vérifier la validité des solutions et de calculer des métriques telles que le nombre de tournées, le nombre de colis, et la distance totale parcourue.

### **Utilisation du Checker Java :**

1. **Accédez au répertoire du checker** :
   ```bash
   cd data/checker/
   ```

2. **Exécutez le checker pour une instance donnée** :
   ```bash
   java -jar CheckerBatchingPicking.jar instance_nom
   ```
   Remplacez `instance_nom` par le nom de l'instance sans l'extension `.txt`.

### **Automatisation de la Validation :**

Un script Python (`script_checker.py`) est fourni pour automatiser l'exécution du checker sur toutes les instances et générer un rapport Excel avec les résultats.

#### **Étapes pour utiliser le script d'automatisation :**

1. **Assurez-vous que Java est installé** et accessible via la commande `java` dans le terminal.

2. **Placez le script `script_checker.py`** à la racine du projet, là où se trouvent les dossiers `data/instances/` et `data/solutions/`.

3. **Exécutez le script** :
   ```bash
   python script_checker.py
   ```

4. **Consultez le fichier Excel généré** :
   Le script génère un fichier `results.xlsx` contenant les colonnes suivantes :

   - Instance
   - Number of Tours
   - Number of Parcels
   - Total Distance (m)

---

## **Analyse des Résultats**

Le fichier `results.xlsx` généré par le script d'automatisation permet d'analyser les performances de l'algorithme sur l'ensemble des instances.

Vous pouvez utiliser Excel ou tout autre outil compatible pour :

- Filtrer et trier les résultats.
- Créer des graphiques pour visualiser les métriques.
- Comparer les performances entre différentes instances.

---

## **Exemple**

### **Exécution du script principal :**

```bash
python src/main.py
```

**Sortie attendue :**

```
INFO:Traitement de l'instance : instance_0116_131940_Z2.txt
INFO:Analyse du fichier d'instance: data/instances/instance_0116_131940_Z2.txt
INFO:Début de la lecture des produits
INFO:Début de la lecture des commandes
INFO:Fin de l'analyse du fichier. Produits lus: 166, Commandes lues: 2
INFO:Solution pour instance_0116_131940_Z2.txt est valide.
```

### **Exécution des tests unitaires :**

```bash
python -m unittest discover -s tests
```

**Sortie attendue :**

```
Test réussi : les données de l'instance ont été correctement analysées.
.
----------------------------------------------------------------------
Ran 2 tests in 0.XXXs

OK
```

### **Exécution du script d'automatisation du checker :**

```bash
python script_checker.py
```

**Sortie attendue :**

```
Traitement de l'instance : instance_0116_131940_Z2
Traitement de l'instance : instance_0116_131941_Z3
Checker a échoué pour l'instance instance_0116_131941_Z3.
Traitement de l'instance : instance_0116_131942_Z4
...
Le fichier results.xlsx a été généré avec succès.
```

---

## **Améliorations Futures**

- **Amélioration de l'algorithme** : Optimiser la répartition des produits dans les colis pour minimiser encore plus les distances parcourues.
- **Gestion avancée des unités de mesure** : S'assurer que les unités de poids et de volume sont cohérentes et gérer automatiquement les conversions si nécessaire.
- **Extension du checker** : Intégrer le checker Java directement dans le script Python pour une validation plus fluide.
- **Documentation** : Ajouter une documentation complète du code pour faciliter la maintenance et les contributions.
- **Interface utilisateur** : Développer une interface graphique pour une utilisation plus intuitive du logiciel.