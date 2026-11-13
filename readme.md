# Tetris — Python & Pygame

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python" /></a>
  <a href="https://www.pygame.org/"><img src="https://img.shields.io/badge/Pygame-2.0%2B-yellow?logo=python&logoColor=white" alt="Pygame" /></a>
  <a href="#"><img src="https://img.shields.io/badge/Module-R3.04_Qualit%C3%A9_de_d%C3%A9veloppement-green" alt="R3.04" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/Licence-GPL-lightgrey" alt="Licence" /></a>
</p>

<br/>

Reconception et implémentation du jeu culte **Tetris** en **Python** avec la bibliothèque **Pygame**. Réalisé dans le cadre de la ressource universitaire **R3.04 (Qualité de développement)** en BUT Informatique, ce projet met l'accent sur la structuration du code, le respect des standards de style (PEP 8, formatage YAPF) et la modélisation rigoureuse de la boucle de jeu.

---

## Fonctionnalités

- **Moteur de Tétrominos Complet** : Gestion des 7 pièces classiques (I, J, L, O, S, T, Z) avec leurs matrices de rotation respectives et codes couleur distincts.
- **Gestion Précise des Collisions** : Détection des limites de bordure et superposition avec les blocs déjà fixés.
- **Effacement de Lignes & Score** : Détection automatique des lignes complétées, descente des blocs supérieurs et calcul du score.
- **Accélération Progressive** : Diminution de l'intervalle de chute à mesure que le joueur élimine des lignes.
- **Interface Graphique Réactive** : Boucle de rendu cadencée à 60 FPS avec affichage du prochain tétromino et des statistiques de jeu.

---

## Structure du Projet

```text
R3.04-proj01-tetris/
├── tetris.py            # Point d'entrée principal et boucle de jeu Pygame
├── constantes.py        # Dimensions de la grille, matrices de rotation, couleurs
├── requirements.txt     # Dépendances Python (pygame)
└── LICENSE              # Licence du projet
```

---

## Installation & Lancement

```bash
# Cloner le dépôt
git clone https://github.com/NedjarYanis/R3.04-proj01-tetris.git
cd R3.04-proj01-tetris

# Créer et activer un environnement virtuel
python -m venv venv
# Sur Windows :
venv\Scripts\activate
# Sur Linux/macOS :
source venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer le jeu
python tetris.py
```

---

## Contrôles du Jeu

| Touche | Action |
| :--- | :--- |
| `←` / `→` | Déplacer le tétromino à gauche / à droite |
| `↓` | Accélérer la chute douce (*Soft Drop*) |
| `↑` | Faire pivoter la pièce de 90° |
| `Espace` | Chute instantanée (*Hard Drop*) |
| `Échap` | Mettre en pause ou quitter la partie |

---

## Bonnes Pratiques & Qualité de Code

Le code source a été validé selon les critères d'évaluation académique de la SAE :
- Respect des règles de style **PEP 8**.
- Découpage modulaire strict entre la logique d'état et le rendu graphique.
- Fonctions documentées et constantes centralisées dans `constantes.py`.

---

## Auteur

Développé par **[Yanis Nedjar](https://github.com/NedjarYanis)** dans le cadre du BUT Informatique à l'IUT d'Orléans.
