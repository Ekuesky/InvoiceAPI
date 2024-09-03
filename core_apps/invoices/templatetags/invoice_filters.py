from django import template

register = template.Library()

@register.simple_tag
def calculer_prix_ttc(prix_ht, tva, quantite):
    prix_ht = float(prix_ht)
    tva = float(tva)
    quantite = int(quantite)
    prix_ttc = (prix_ht * (1 + tva)) * quantite
    return f"{prix_ttc:.2f}"