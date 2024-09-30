# utils/validation.py

def valider_solution(entrepot, tournees):
    """
    Valide les solutions générées en vérifiant les contraintes.

    :param entrepot: Objet Entrepot contenant les données.
    :param tournees: Liste des objets Tournee générés.
    :return: Booléen indiquant si la solution est valide.
    """
    # Implémentation simplifiée pour l'exemple
    commandes_preparees = set()
    for tournee in tournees:
        for colis in tournee.chariot.colis:
            commande = entrepot.commandes[colis.id_commande]
            poids_colis = sum(entrepot.produits[id_prod].poids_unitaire * qte for id_prod, qte in colis.produits.items())
            volume_colis = sum(entrepot.produits[id_prod].volume_unitaire * qte for id_prod, qte in colis.produits.items())
            if poids_colis > entrepot.capacite_colis[0] or volume_colis > entrepot.capacite_colis[1]:
                print(f"Colis {colis.id} dépasse les capacités.")
                return False
            commandes_preparees.add(colis.id_commande)
    if len(commandes_preparees) != len(entrepot.commandes):
        print("Toutes les commandes n'ont pas été préparées.")
        return False
    return True
