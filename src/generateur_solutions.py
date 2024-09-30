# generateur_solutions.py

def generer_fichier_solution(nom_instance, tournees):
    """
    Génère un fichier de solution au format requis.

    :param nom_instance: Nom de l'instance (sans extension).
    :param tournees: Liste des objets Tournee.
    """
    nom_fichier_solution = f"data/solutions/{nom_instance}_sol.txt"
    with open(nom_fichier_solution, 'w') as fichier:
        # Écrire le nombre de tournées avec le commentaire
        fichier.write("//NbTournees\n")
        fichier.write(f"{len(tournees)}\n")
        
        # Pour chaque tournée
        for tournee in tournees:
            # Écrire le commentaire pour la tournée
            fichier.write("//IdTournes NbColis\n")
            # Écrire l'ID de la tournée et le nombre de colis
            fichier.write(f"{tournee.id} {len(tournee.chariot.colis)}\n")
            # Écrire le commentaire pour les colis
            fichier.write("//IdColis IdCommandeInColis NbProducts IdProd1 QtyProd1 IdProd2 QtyProd2 ...\n")
            for colis in tournee.chariot.colis:
                # Préparer la liste des produits et quantités
                produits_list = []
                for id_produit, quantite in colis.produits.items():
                    produits_list.append(f"{id_produit} {quantite}")
                produits_str = ' '.join(produits_list)
                # Écrire la ligne du colis
                fichier.write(f"{colis.id} {colis.id_commande} {len(colis.produits)} {produits_str}\n")
