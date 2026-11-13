# Tetris — Python & Pygame

<div align="center">
  [![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
  [![Pygame](https://img.shields.io/badge/Pygame-2.0%2B-yellow?logo=python&logoColor=white)](https://www.pygame.org/)
  [![BUT Informatique](https://img.shields.io/badge/Module-R3.04_Qualit%C3%A9_de_d%C3%A9veloppement-green)](#)
  [![License](https://img.shields.io/badge/Licence-GPL-lightgrey)](LICENSE)
</div>

<br/>

Reconception et implémentation du jeu culte **Tetris** en **Python** avec la bibliothèque **Pygame**. Réalisé dans le cadre de la ressource universitaire **R3.04 (Qualité de développement)** en BUT Informatique, ce projet met l'accent sur la structuration du code, le respect des standards de style (PEP 8, formatage YAPF) et la modélisation rigoureuse de la boucle de jeu.

---

## Fonctionnalités

- **Moteur de Tétrominos Complet** : Gestion des 7 pièces classiques (I, J, L, O, S, T, Z) avec leurs matrices de rotation respectives et codes couleur distincts.
- **Gestion Précise des Collisions** : Détection des limites de bordure et superposition avec les blocs déjà fixés.
- **Effacement de Lignes & Score** : Détection automatique des lignes complétées, descente des blocs supérieurs et calcul du score.
- **Accélération Progressive** : Vitesse de chute augmentant avec le niveau et score pour un challenge croissant.
- **Mode Pause & Redémarrage** : Possibilité d'interrompre et reprendre la partie instantanément.

---

## Contrôles du Jeu

| Touche | Action |
| :--- | :--- |
| <kbd>←</kbd> | Déplacer le tétromino vers la gauche |
| <kbd>→</kbd> | Déplacer le tétromino vers la droite |
| <kbd>↑</kbd> | Rotation de la pièce |
| <kbd>↓</kbd> | Chute accélérée (*soft drop*) |
| <kbd>Espace</kbd> | Chute instantanée (*hard drop*) |
| <kbd>P</kbd> | Mettre en pause / Reprendre |
| <kbd>Échap</kbd> | Quitter la partie |

---

## Organisation du Code

```text
.
├── tetris.py           # Boucle principale de jeu, gestion des événements Pygame, logique métier
├── constantes.py       # Définition des pièces, grilles, dimensions, polices et couleurs
├── requirements.txt    # Dépendance principale (pygame)
└── LICENSE             # Licence GPL
```

---

## Installation & Lancement

### 1. Cloner le dépôt
```bash
git clone https://github.com/NedjarYanis/R3.04-proj01-tetris.git
cd R3.04-proj01-tetris
```

### 2. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 3. Démarrer le jeu
```bash
python tetris.py
```

---

<div align="center">
  <sub>Projet universitaire BUT Informatique — Réalisé par Yanis Nedjar</sub>
</div>
