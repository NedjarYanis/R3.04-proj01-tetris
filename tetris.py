#!/usr/bin/python3
# -*- coding: utf-8 -*-
# pylint: disable=line-too-long, trailing-whitespace, missing-final-newline, no-name-in-module, too-many-instance-attributes, no-member, too-many-branches
"""
[Ce bloc est la documentation du module]
Un Tetris avec Pygame.
Ce code est basee sur le code de Sébastien CHAZALLET, auteur du livre "Python 3, les fondamentaux du language"
"""

__author__ = "Yanis Nedjar"
__copyright__ = "Copyright 2022"
__credits__ = ["Sébastien CHAZALLET", "Vincent NGUYEN", "Yanis Nedjar"]
__license__ = "GPL"
__version__ = "1.0"

import random
import sys
import time

import pygame
# Probleme de l'ordre des imports
from pygame.locals import (
    QUIT, KEYUP, KEYDOWN, K_ESCAPE, K_p, 
    K_LEFT, K_RIGHT, K_DOWN, K_UP, K_SPACE
)

import constantes

# Classe Tetris
class Jeu:
    """Classe principale du jeu Tetris."""

    def __init__(self):
        """
        Initialise le jeu.

        Returns:
            None
        """
        pygame.init()
        self.clock = pygame.time.Clock()
        self.surface = pygame.display.set_mode(constantes.TAILLE_FENETRE)
        self.fonts = {
            'defaut': pygame.font.Font(constantes.POLICE, constantes.TAILLE_POLICE_DEFAUT),
            'titre': pygame.font.Font(constantes.POLICE, constantes.TAILLE_POLICE_TITRE),
        }
        pygame.display.set_caption(constantes.TITRE_FENETRE)

        self.plateau = []
        self.score = 0
        self.pieces = 0
        self.lignes = 0
        self.tetris = 0
        self.niveau = 1
        self.current = None
        self.next = self._get_piece()
        self.perdu = False
        self.position = [0, 0, 0]
        self.coordonnees = []
        self.derniere_chute = 0.0

    def start(self):
        """
        Affiche l'écran de démarrage.

        Returns:
            None
        """
        self._afficher_texte(constantes.TEXTE_TITRE, constantes.CENTRE_FENETRE, font='titre')
        self._afficher_texte(constantes.TEXTE_ATTENTE, constantes.POS)
        self._attente()

    def stop(self):
        """
        Affiche l'écran de fin.

        Returns:
            None
        """
        self._afficher_texte(constantes.TEXTE_PERDU, constantes.CENTRE_FENETRE, font='titre')
        self._attente()
        self._quitter()

    def _afficher_texte(self, text, position, couleur=constantes.COULEUR_DEFAUT_TEXTE, font='defaut'):
        """
        Affiche du texte.

        Returns:
            None
        """
        font_obj = self.fonts.get(font, self.fonts['defaut'])
        
        couleur_rgb = constantes.COULEURS.get(
            couleur, constantes.COULEURS[constantes.COULEUR_DEFAUT_TEXTE]
        )
        rendu = font_obj.render(text, True, couleur_rgb)
        rect = rendu.get_rect()
        rect.center = position
        self.surface.blit(rendu, rect)

    def _get_event(self):
        """
        Récupère les événements.

        Returns:
            int or None: La touche pressée.
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                self._quitter()
            if event.type == KEYUP:
                if event.key == K_ESCAPE:
                    self._quitter()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    continue
                return event.key
        return None

    def _quitter(self):
        """
        Quitte le jeu.

        Returns:
            None
        """
        pygame.quit()
        sys.exit()

    def _rendre(self):
        """
        Met à jour l'affichage.

        Returns:
            None
        """
        pygame.display.update()
        self.clock.tick()

    def _attente(self):
        """
        Met en attente.

        Returns:
            None
        """
        while self._get_event() is None:
            self._rendre()

    def _get_piece(self):
        """
        Retourne une pièce.

        Returns:
            list: La pièce.
        """
        return constantes.PIECES.get(random.choice(constantes.PIECES_KEYS))

    def _get_current_piece_color(self):
        """
        Retourne la couleur de la pièce courante.

        Returns:
            int: La couleur.
        """
        for ligne in self.current[0]:
            for case in ligne:
                if case != 0:
                    return case
        return 0

    def _calculer_donnees_piece_courante(self):
        """
        Calcule les coordonnées de la pièce.

        Returns:
            None
        """
        matrice = self.current[self.position[2]]
        coords = []
        for i, ligne in enumerate(matrice):
            for j, case in enumerate(ligne):
                if case != 0:
                    coords.append([i + self.position[0], j + self.position[1]])
        self.coordonnees = coords

    def _est_valide(self, dec_x=0, dec_y=0, rot=0):
        """
        Vérifie la validité de la position.

        Returns:
            bool: Vrai si valide.
        """
        max_x, max_y = constantes.DIM_PLATEAU
        if rot == 0:
            coordonnees = self.coordonnees
        else:
            matrice = self.current[(self.position[2] + rot) % len(self.current)]
            coords = []
            for i, ligne in enumerate(matrice):
                for j, case in enumerate(ligne):
                    if case != 0:
                        coords.append([i + self.position[0], j + self.position[1]])
            coordonnees = coords

        for cx, cy in coordonnees:
            if not 0 <= dec_x + cx < max_x:
                return False
            if cy < 0:
                continue
            if dec_y + cy >= max_y:
                return False
            if self.plateau[cy + dec_y][cx + dec_x] != 0:
                return False
        return True

    def _poser_piece(self):
        """
        Pose la pièce sur le plateau.

        Returns:
            None
        """
        if self.position[1] <= 0:
            self.perdu = True

        couleur = self._get_current_piece_color()
        for cx, cy in self.coordonnees:
            self.plateau[cy][cx] = couleur

        completees = []
        for i, ligne in enumerate(self.plateau[::-1]):
            for case in ligne:
                if case == 0:
                    break
            else:
                completees.append(constantes.DIM_PLATEAU[1] - 1 - i)

        lignes = len(completees)
        for i in completees:
            self.plateau.pop(i)
        for i in range(lignes):
            self.plateau.insert(0, [0] * constantes.DIM_PLATEAU[0])

        self.lignes += lignes
        self.score += lignes * self.niveau
        self.niveau = int(self.lignes / constantes.LIGNES_PAR_NIVEAU) + 1
        if lignes >= constantes.LIGNES_TETRIS:
            self.tetris += 1
            self.score += self.niveau * self.tetris
        self.current = None

    def _first(self):
        """
        Initialise la partie.

        Returns:
            None
        """
        self.plateau = [[0] * constantes.DIM_PLATEAU[0] for _ in range(constantes.DIM_PLATEAU[1])]
        self.score, self.pieces, self.lignes, self.tetris, self.niveau = 0, 0, 0, 0, 1
        self.current, self.next, self.perdu = None, self._get_piece(), False

    def _next(self):
        """
        Passe à la pièce suivante.

        Returns:
            None
        """
        self.current, self.next = self.next, self._get_piece()
        self.pieces += 1
        self.position = [int(constantes.DIM_PLATEAU[0] / 2) - 2, -4, 0]
        self._calculer_donnees_piece_courante()
        self.derniere_chute = time.time()

    def _gerer_evenements(self):
        """
        Gère les entrées clavier.

        Returns:
            None
        """
        event = self._get_event()
        if event == K_p:
            self.surface.fill(constantes.COULEURS.get(constantes.COULEUR_FOND))
            self._afficher_texte(constantes.TEXTE_PAUSE, constantes.CENTRE_FENETRE, font='titre')
            self._afficher_texte(constantes.TEXTE_ATTENTE, constantes.POS)
            self._attente()
        elif event == K_LEFT:
            if self._est_valide(dec_x=-1):
                self.position[0] -= 1
        elif event == K_RIGHT:
            if self._est_valide(dec_x=1):
                self.position[0] += 1
        elif event == K_DOWN:
            if self._est_valide(dec_y=1):
                self.position[1] += 1
        elif event == K_UP:
            if self._est_valide(rot=1):
                self.position[2] = (self.position[2] + 1) % len(self.current)
        elif event == K_SPACE:
            if self.position[1] <= 0:
                self.position[1] = 1
                self._calculer_donnees_piece_courante()
            a = 0
            while self._est_valide(dec_y=a):
                a += 1
            self.position[1] += a - 1
        if self.current:
            self._calculer_donnees_piece_courante()

    def _gerer_gravite(self):
        """
        Gère la chute.

        Returns:
            None
        """
        if time.time() - self.derniere_chute > constantes.DELAI_CHUTE:
            self.derniere_chute = time.time()
            if not self._est_valide():
                self.position[1] -= 1
                self._calculer_donnees_piece_courante()
                self._poser_piece()
            elif self._est_valide() and not self._est_valide(dec_y=1):
                self._calculer_donnees_piece_courante()
                self._poser_piece()
            else:
                self.position[1] += 1
                self._calculer_donnees_piece_courante()

    def _dessiner_plateau(self):
        """
        Dessine le plateau.

        Returns:
            None
        """
        self.surface.fill(constantes.COULEURS.get(constantes.COULEUR_FOND))
        pygame.draw.rect(self.surface, constantes.COULEURS[8],
                         constantes.START_PLABORD + constantes.TAILLE_PLABORD,
                         constantes.BORDURE_PLATEAU)

        for i, ligne in enumerate(self.plateau):
            for j, case in enumerate(ligne):
                couleur = constantes.COULEURS[case]
                position = j, i
                coordonnees = tuple(
                    constantes.START_PLATEAU[k] + position[k] * constantes.TAILLE_BLOC[k]
                    for k in range(2)
                )
                pygame.draw.rect(self.surface, couleur, coordonnees + constantes.TAILLE_BLOC)

        if self.current is not None:
            for position in self.coordonnees:
                couleur = constantes.COULEURS.get(self._get_current_piece_color())
                coordonnees = tuple(
                    constantes.START_PLATEAU[k] + position[k] * constantes.TAILLE_BLOC[k]
                    for k in range(2)
                )
                pygame.draw.rect(self.surface, couleur, coordonnees + constantes.TAILLE_BLOC)

        self._afficher_texte(constantes.FORMAT_SCORE % self.score, constantes.POSITION_SCORE)
        self._afficher_texte(constantes.FORMAT_PIECES % self.pieces, constantes.POSITION_PIECES)
        self._afficher_texte(constantes.FORMAT_LIGNES % self.lignes, constantes.POSITION_LIGNES)
        self._afficher_texte(constantes.FORMAT_TETRIS % self.tetris, constantes.POSITION_TETRIS)
        self._afficher_texte(constantes.FORMAT_NIVEAU % self.niveau, constantes.POSITION_NIVEAU)

        self._rendre()

    def play(self):
        """
        Boucle de jeu.

        Returns:
            None
        """
        self.surface.fill(constantes.COULEURS.get(constantes.COULEUR_FOND))
        self._first()
        while not self.perdu:
            if self.current is None:
                self._next()
            self._gerer_evenements()
            self._gerer_gravite()
            self._dessiner_plateau()


if __name__ == '__main__':
    jeu_instance = Jeu()
    jeu_instance.start()
    jeu_instance.play()
    jeu_instance.stop()