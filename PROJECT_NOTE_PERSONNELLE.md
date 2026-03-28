# Note personnelle

## Pourquoi j'ai choisi ce sujet

Depuis que je suis en M2, j'essaie de travailler sur des projets qui ont un lien avec des trucs concrets de la vie quotidienne. La météo, c'est quelque chose que tout le monde consulte plusieurs fois par jour, mais personne ne se pose vraiment la question de savoir à quel point on peut lui faire confiance.

J'avais remarqué que les prévisions à 5 jours semblaient souvent fausses — pas d'une façon dramatique, mais suffisamment pour que ça change un plan. J'ai voulu mettre un chiffre sur cette intuition.

L'autre raison, c'est que ça m'a permis de travailler sur un pipeline de données complet (collecte → traitement → métriques → visualisation) avec quelque chose que je comprends intuitivement. C'est plus facile d'interpréter un résultat quand on sait ce que ça veut dire dans la vraie vie qu'une température de +0.7 °C de biais.

## Mes choix techniques

**Panel de villes :** j'ai pris 8 villes françaises qui représentent des situations géographiques différentes — nord (Lille), littoral méditerranéen (Nice, Marseille), Atlantique (Nantes), intérieur continental (Lyon, Toulouse, Paris) et est (Strasbourg). C'est volontairement limité pour garder quelque chose de lisible, mais la structure du code permet d'en rajouter facilement.

**Métriques :** MAE et RMSE sont les deux mesures classiques pour ce genre d'analyse. J'ai ajouté le biais parce que c'est une information différente — une prévision peut avoir un MAE correct tout en surestimant systématiquement. Pour la décision (est-ce que je pars en week-end ou pas), un biais constant dans un sens est en fait plus problématique qu'une erreur aléatoire de même amplitude.

**Mode synthétique :** je n'avais pas de vrai historique de plusieurs semaines au moment de finaliser le projet. Plutôt que de bloquer le projet sur l'absence de données réelles, j'ai construit un générateur qui intègre les effets connus (latitude, saisonnalité, variabilité locale). C'est une limite que j'assume clairement — les résultats ne décrivent pas la vraie météo de ces villes, ils valident la méthode.

**Pipeline modulaire :** j'ai séparé la collecte, l'analyse et la visualisation dans des modules distincts. Ça m'a pris plus de temps que de tout mettre dans un notebook, mais le code est plus facile à maintenir et à faire évoluer.

## Ce que j'aurais fait avec plus de temps

- Collecter un vrai historique pendant 4 à 6 semaines avec une automatisation quotidienne (j'avais commencé à regarder GitHub Actions pour ça)
- Distinguer l'analyse par horizon : est-ce que J+1 est vraiment plus fiable que J+4 ? Sur quel type de ville la dégradation est-elle la plus rapide ?
- Comparer OpenWeatherMap avec une autre source (Météo-France a une API gratuite) pour voir si les erreurs sont corrélées ou indépendantes
- Étendre le panel à des villes de montagne (Grenoble, Chamonix) pour tester l'hypothèse que les reliefs complexes rendent les prévisions moins fiables
- Faire une interface Streamlit simple pour naviguer dans les résultats sans avoir besoin de Jupyter

## Limites honnêtes

Les données sont synthétiques, le panel est petit, et l'analyse porte sur une seule variable (température). Un projet plus complet inclurait précipitations, vent, nébulosité. Les conclusions ici sont exploratoires, pas généralisables.
