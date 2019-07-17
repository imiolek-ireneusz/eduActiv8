# -*- coding: utf-8 -*-

# This is a list of words used by the word builder and word maze games and possibly other games built in the future
# these words are a naive translation of a part of most commonly used words in English in each sub-list in the list di
# first number is a number of words in the sub-list to avoid counting it every time the list is selected the sub-lists
# are consisting of words with len() of 3 - 10. I think the way of going about internationalization here would be to
# create a new list with words most commonly used in your language rather than translating the English version.
# I am not sure if they are appropriate for children, but if anyone is interested we can try to built something more
# suitable or if you like you can try to edit this list - remove the words that you think are either not in German or
# are not suitable for under 10 years old children and send it back to the email address shown at the start of the game.
# If you have a better list please send it to me and I will format it and add it to the game. This is a very naive
# translation from google translate - only resorted and counted.

di = [
    [17, 'ans', 'bec', 'bon', 'cot', 'dit', 'est', 'ici', 'lit', 'mou', 'oui', 'par', 'qui', 'son', 'sud', 'sur', 'une',
     'été'],
    [57, 'avec', 'base', 'beau', 'bleu', 'bord', 'choc', 'clac', 'coup', 'côté', 'deux', 'dont', 'fixe', 'flux', 'fois',
     'huit', 'idée', 'joie', 'jour', 'lent', 'leur', 'lire', 'long', 'main', 'mars', 'maïs', 'mois', 'mort', 'mots',
     'même', 'nage', 'noir', 'nord', 'peau', 'peur', 'peur', 'peur', 'plan', 'plat', 'plus', 'pour', 'prêt', 'père',
     'quoi', 'rare', 'rien', 'sans', 'sauf', 'sens', 'soin', 'sort', 'tige', 'tout', 'tout', 'trou', 'venu', 'vêtu',
     'zéro'],
    [60, 'ainsi', 'alors', 'autre', 'autre', 'bande', 'blanc', 'cadre', 'champ', 'chant', 'chaud', 'chose', 'clair',
     'comte', 'donné', 'drapé', 'entre', 'faire', 'faire', 'fleur', 'flûte', 'force', 'forme', 'grand', 'grand',
     'grève', 'gâter', 'jabot', 'juste', 'lampe', 'laver', 'marié', 'noire', 'notre', 'passé', 'pente', 'petit',
     'pièce', 'pièce', 'piège', 'poche', 'poids', 'poème', 'poêle', 'quand', 'raide', 'rouge', 'règle', 'sauté',
     'signe', 'silex', 'situé', 'sucre', 'suite', 'tache', 'tendu', 'terne', 'terre', 'venir', 'voile', 'votre'],
    [66, 'anneau', 'bondit', 'bouche', 'bourru', 'braire', 'brosse', 'bétail', 'calmar', 'camion', 'chacun', 'chemin',
     'commun', 'dessin', 'dérive', 'désert', 'emploi', 'encore', 'espion', 'esprit', 'faible', 'fierté', 'figure',
     'flamme', 'fleurs', 'flotte', 'fluage', 'fluide', 'fraise', 'fruits', 'garçon', 'glisse', 'goutte', 'goutte',
     'gramme', 'greffe', 'griffe', 'grille', 'heures', 'hommes', 'hélice', 'jamais', 'jambes', 'manger', 'marque',
     'modèle', 'montré', 'navire', 'numéro', 'parler', 'penser', 'preuve', 'projet', 'raisin', 'rapide', 'regard',
     'remuer', 'retour', 'savait', 'siècle', 'sombre', 'stable', 'séjour', 'taches', 'usines', 'valeur', 'vérité'],
    [55, 'aveugle', 'baisser', 'berceau', 'berceau', 'bifteck', 'boucher', 'briques', 'brûlure', 'cerveau', 'chiffon',
     'complot', 'composé', 'conseil', 'courges', 'demandé', 'devenir', 'défiler', 'détails', 'falaise', 'frotter',
     'grandir', 'grognon', 'manteau', 'mauvais', 'miettes', 'méthode', 'nouveau', 'oiseaux', 'parfois', 'placard',
     'plaider', 'plantes', 'poisson', 'proposé', 'quelque', 'quitter', 'ronfler', 'réponse', 'saigner', 'silence',
     'soldats', 'sommeil', 'soudain', 'soulevé', 'suivant', 'tableau', 'traiter', 'voiture', 'volonté', 'voyager',
     'écouter', 'élaboré', 'élevage', 'énergie', 'étendue'],
    [47, 'accident', 'adjectif', 'affaires', 'arracher', 'arrosage', 'assiette', 'attendre', 'attraper', 'balancer',
     'balayage', 'brancard', 'brillant', 'brillant', 'consonne', 'continue', 'contrôle', 'coquille', 'cultures',
     'ensemble', 'entendre', 'entendre', 'esquisse', 'excitant', 'grimoire', 'généraux', 'insectes', 'meilleur',
     'milliers', 'millions', 'plancher', 'problème', 'produits', 'produits', 'protéger', 'précieux', 'préparer',
     'regarder', 'regarder', 'ressenti', 'rousseur', 'ruisseau', 'résultat', 'souligné', 'souvenir', 'statisme',
     'syllabes', 'symboles'],
    [26, 'abondance', 'cependant', 'collation', 'conserver', 'courageux', 'difficile', 'différent', 'dissident',
     'découvert', 'eux-mêmes', 'graphique', 'industrie', 'lentement', 'molécules', 'montagnes', 'mouvement',
     'pantoufle', 'parcourir', 'plusieurs', 'programme', 'promenade', 'prononcer', 'président', 'tortiller',
     'vêtements', 'éclaireur'],
    [20, 'auparavant', 'caracolent', 'changement', 'comprendre', 'différence', 'discussion', 'déterminer', 'développés',
     'expérience', 'grenouille', 'grognement', 'hirondelle', 'maintenant', 'nourriture', 'nécessaire', 'paragraphe',
     'principale', 'professeur', 'succursale', 'électrique']]
