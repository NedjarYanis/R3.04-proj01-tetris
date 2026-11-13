# Tetris ? Python & Pygame

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white" alt="Python" /></a>
  <a href="https://www.pygame.org/"><img src="https://img.shields.io/badge/Pygame-2.0%2B-yellow?logo=python&logoColor=white" alt="Pygame" /></a>
  <a href="#"><img src="https://img.shields.io/badge/Module-R3.04_Qualit?_de_d?veloppement-green" alt="R3.04" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/Licence-GPL-lightgrey" alt="Licence" /></a>
</p>

<br/>

Reconception et impl?mentation du jeu culte **Tetris** en **Python** avec la biblioth?que **Pygame**. R?alis? dans le cadre de la ressource universitaire **R3.04 (Qualit? de d?veloppement)** en BUT Informatique, ce projet met l'accent sur la structuration du code, le respect des standards de style (PEP 8, formatage YAPF) et la mod?lisation rigoureuse de la boucle de jeu.

---

## Fonctionnalit?s

- **Moteur de T?trominos Complet** : Gestion des 7 pi?ces classiques (I, J, L, O, S, T, Z) avec leurs matrices de rotation respectives et codes couleur distincts.
- **Gestion Pr?cise des Collisions** : D?tection des limites de bordure et superposition avec les blocs d?j? fix?s.
- **Effacement de Lignes & Score** : D?tection automatique des lignes compl?t?es, descente des blocs sup?rieurs et calcul du score.
- **Acc?l?ration Progressive** : Vitesse de chute augmentant avec le niveau et score pour un challenge croissant.
- **Mode Pause & Red?marrage** : Possibilit? d'interrompre et reprendre la partie instantan?ment.

---

## Contr?les du Jeu

| Touche | Action |
| :--- | :--- |
| <kbd>?</kbd> | D?placer le t?tromino vers la gauche |
| <kbd>?</kbd> | D?placer le t?tromino vers la droite |
| <kbd>?</kbd> | Rotation de la pi?ce |
| <kbd>?</kbd> | Chute acc?l?r?e (*soft drop*) |
| <kbd>Espace</kbd> | Chute instantan?e (*hard drop*) |
| <kbd>P</kbd> | Mettre en pause / Reprendre |
| <kbd>?chap</kbd> | Quitter la partie |

---

## Organisation du Code

```text
.
??? tetris.py           # Boucle principale de jeu, gestion des ?v?nements Pygame, logique m?tier
??? constantes.py       # D?finition des pi?ces, grilles, dimensions, polices et couleurs
??? requirements.txt    # D?pendance principale (pygame)
??? LICENSE             # Licence GPL
```

---

## Installation & Lancement

### 1. Cloner le d?p?t
```bash
git clone https://github.com/NedjarYanis/R3.04-proj01-tetris.git
cd R3.04-proj01-tetris
```

### 2. Installer les d?pendances
```bash
pip install -r requirements.txt
```

### 3. D?marrer le jeu
```bash
python tetris.py
```

---

<div align="center">
  <sub>Projet universitaire BUT Informatique ? R?alis? par Yanis Nedjar</sub>
</div>
