#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
Un Tetris avec Pygame.
Ce code est basee sur le code de Sébastien CHAZALLET, auteur du livre "Python 3, les fondamentaux du language"
"""

__author__ = "votre nom"
__copyright__ = "Copyright 2022"
__credits__ = ["Sébastien CHAZALLET", "Vincent NGUYEN", "votre nom"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "votre nom"
__email__ = "votre email"

# Probleme de l'ordre des imports
from pygame.locals import *
import random
import time
import pygame
import sys
import constantes


class Jeu:
	"""gère la logique principale, l'affichage et les interactions du jeu Tetris
	"""
	def __init__(self) -> None:
		"""initialise pygame, la fenêtre de jeu et les polices

		Returns:
			None
		"""
		pygame.init()
		self.clock: pygame.time.Clock = pygame.time.Clock()
		self.surface: pygame.Surface = pygame.display.set_mode(constantes.TAILLE_FENETRE)
		self.fonts: dict = {
			'defaut': pygame.font.Font(constantes.POLICE, constantes.TAILLE_POLICE_DEFAUT),
			'titre': pygame.font.Font(constantes.POLICE, constantes.TAILLE_POLICE_TITRE),
		}
		pygame.display.set_caption(constantes.TITRE_FENETRE)

	def start(self) -> None:
		"""affiche l'écran de démarrage du jeu

		Returns:
			None
		"""
		self._afficher_texte(constantes.TEXTE_TITRE, constantes.CENTRE_FENETRE, font='titre')
		self._afficher_texte(constantes.TEXTE_ATTENTE, constantes.POS)
		self._attente()

	def stop(self) -> None:
		"""affiche l'écran de fin et ferme le jeu

		Returns:
			None
		"""
		self._afficher_texte(constantes.TEXTE_PERDU, constantes.CENTRE_FENETRE, font='titre')
		self._attente()
		self._quitter()

	def _afficher_texte(self, text: str, position: tuple, couleur: int = constantes.COULEUR_DEFAUT_TEXTE, font: str = 'defaut') -> None:
		"""affiche du texte centré sur la position donnée

		Args:
			text (str): le texte à afficher
			position (tuple): les coordonnées (x, y) du centre du texte
			couleur (int, optional): l'identifiant de la couleur du texte
			font (str, optional): la clé de la police à utiliser

		Returns:
			None
		"""
		font_obj = self.fonts.get(font, self.fonts['defaut'])
		couleur_rgb = constantes.COULEURS.get(couleur, constantes.COULEURS[constantes.COULEUR_DEFAUT_TEXTE])
		rendu = font_obj.render(text, True, couleur_rgb)
		rect = rendu.get_rect()
		rect.center = position
		self.surface.blit(rendu, rect)
        
	def _get_event(self):
		"""récupère les entrées du clavier et gère la fermeture de la fenêtre

		Returns:
			int: la valeur de la touche pressée
			None: si aucune action clavier n'est détectée
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
				
	def _quitter(self) -> None:
		"""ferme proprement pygame et quitte le programme

		Returns:
			None
		"""
		print("Quitter")
		pygame.quit()
		sys.exit()
        
	def _rendre(self) -> None:
		"""met à jour l'écran et gère la fréquence d'images

		Returns:
			None
		"""
		pygame.display.update()
		self.clock.tick()
        
	def _attente(self) -> None:
		"""met le jeu en pause jusqu'à ce qu'une touche soit pressée

		Returns:
			None
		"""
		print("Attente")
		while self._get_event() is None:
			self._rendre()
            
	def _get_piece(self) -> list:
		"""renvoie une nouvelle pièce aléatoire avec toutes ses rotations possibles

		Returns:
			list: la structure contenant les formes de la pièce
		"""
		return constantes.PIECES.get(random.choice(constantes.PIECES_KEYS))
        
	def _get_current_piece_color(self) -> int:
		"""renvoie l'identifiant de couleur de la pièce actuellement jouée

		Returns:
			int: l'index de la couleur
		"""
		for l in self.current[0]:
			for c in l:
				if c != 0:
					return c
		return 0
        
	def _calculer_donnees_piece_courante(self) -> None:
		"""calcule les coordonnées exactes des blocs de la pièce courante sur le plateau

		Returns:
			None
		"""
		m = self.current[self.position[2]]
		coords: list = []
		for i, l in enumerate(m):
			for j, k in enumerate(l):
				if k != 0:
					coords.append([i + self.position[0], j + self.position[1]])
		self.coordonnees = coords
        
	def _est_valide(self, x: int = 0, y: int = 0, r: int = 0) -> bool:
		"""vérifie si la position ou la rotation ciblée est possible (pas de collision)

		Args:
			x (int, optional): le décalage sur l'axe X
			y (int, optional): le décalage sur l'axe Y
			r (int, optional): le décalage de rotation

		Returns:
			bool: True si la position est libre et dans le plateau, False sinon
		"""
		max_x, max_y = constantes.DIM_PLATEAU
		if r == 0:
			coordonnees = self.coordonnees
		else:
			m = self.current[(self.position[2] + r) % len(self.current)]
			coords: list = []
			for i, l in enumerate(m):
				for j, k in enumerate(l):
					if k != 0:
						coords.append([i + self.position[0], j + self.position[1]])
			coordonnees = coords

		for cx, cy in coordonnees:
			if not 0 <= x + cx < max_x:
#				print("Non valide en X: cx=%s, x=%s" % (cx, x))
				return False
			elif cy < 0:
				continue
			elif y + cy >= max_y:#verfie que on transperce pas le sole
#				print("Non valide en Y: cy=%s, y=%s" % (cy, y))
				return False
			else:
				if self.plateau[cy + y][cx + x] != 0:
#					print("Position occupée sur le plateau")
					return False
#		print("Position testée valide: x=%s, y=%s" % (x, y))
		return True
        
	def _poser_piece(self) -> None:
		"""fixe la pièce sur le plateau, valide les lignes pleines et met à jour le score

		Returns:
			None
		"""
		print("La pièce est posée")
		if self.position[1] <= 0: #verfie si la piece depasse au dessus
			self.perdu = True
		# Ajout de la pièce parmi le plateau
		couleur = self._get_current_piece_color()
		for cx, cy in self.coordonnees:
			self.plateau[cy][cx] = couleur
		completees: list = []
		# calculer les lignes complétées
		for i, line in enumerate(self.plateau[::-1]): #redgarde en partant du bas 
			for case in line:
				if case == 0:#si il y a un troue (0)
					break #passe a ligne du dessu
			else:
				print(self.plateau)
				print(">>> %s" % (constantes.DIM_PLATEAU[1] - 1 - i))
				completees.append(constantes.DIM_PLATEAU[1] - 1 - i)
		lignes = len(completees)
		for i in completees:
			self.plateau.pop(i)#suprime la ligne
		for i in range(lignes):
			self.plateau.insert(0, [0] * constantes.DIM_PLATEAU[0])
		# calculer le score et autre
		self.lignes += lignes
		self.score += lignes * self.niveau
		self.niveau = int(self.lignes / constantes.LIGNES_PAR_NIVEAU) + 1
		if lignes >= constantes.LIGNES_TETRIS:
			self.tetris += 1
			self.score += self.niveau * self.tetris
		# Travail avec la pièce courante terminé
		self.current = None
        
	def _first(self) -> None:
		"""initialise les variables et génère le plateau vide pour une nouvelle partie

		Returns:
			None
		"""
		self.plateau: list = [[0] * constantes.DIM_PLATEAU[0] for _ in range(constantes.DIM_PLATEAU[1])]
		self.score: int = 0
		self.pieces: int = 0
		self.lignes: int = 0
		self.tetris: int = 0
		self.niveau: int = 1
		self.next: list = self._get_piece()
		self.current = None
		self.perdu: bool = False
        
	def _next(self) -> None:
		"""passe à la pièce suivante et la place en haut du plateau

		Returns:
			None
		"""
		print("Piece suivante")
		self.current, self.next = self.next, self._get_piece()
		self.pieces += 1
		self.position: list = [int(constantes.DIM_PLATEAU[0] / 2) - 2, -4, 0]
		self._calculer_donnees_piece_courante()
		self.dernier_mouvement = self.derniere_chute = time.time()
        
	def _gerer_evenements(self) -> None:
		"""traite les actions du joueur comme les déplacements, la rotation et la pause

		Returns:
			None
		"""
		event = self._get_event()
		if event == K_p:
			print("Pause")
			self.surface.fill(constantes.COULEURS.get(constantes.COULEUR_FOND))
			self._afficher_texte(constantes.TEXTE_PAUSE, constantes.CENTRE_FENETRE, font='titre')
			self._afficher_texte(constantes.TEXTE_ATTENTE, constantes.POS)
			self._attente()
		elif event == K_LEFT:
			print("Mouvement vers la gauche")
			if self._est_valide(x=-1):
				self.position[0] -= 1
		elif event == K_RIGHT:
			print("Mouvement vers la droite")
			if self._est_valide(x=1):
				self.position[0] += 1
		elif event == K_DOWN:
			print("Mouvement vers le bas")
			if self._est_valide(y=1):
				self.position[1] += 1
		elif event == K_UP:
			print("Mouvement de rotation")
			if self._est_valide(r=1):
				self.position[2] = (self.position[2] + 1) % len(self.current)
		elif event == K_SPACE:
			print("Mouvement de chute %s / %s" % (self.position, self.coordonnees))
			if self.position[1] <= 0:
				self.position[1] = 1
				self._calculer_donnees_piece_courante()
			a = 0
			while self._est_valide(y=a):
				a += 1
			self.position[1] += a - 1
		self._calculer_donnees_piece_courante()
        
	def _gerer_gravite(self) -> None:
		"""fait descendre automatiquement la pièce courante en fonction du temps écoulé

		Returns:
			None
		"""
		if time.time() - self.derniere_chute > constantes.DELAI_CHUTE:
			self.derniere_chute = time.time()
			if not self._est_valide():
				print ("On est dans une position invalide")
				self.position[1] -= 1
				self._calculer_donnees_piece_courante()
				self._poser_piece()
			elif self._est_valide() and not self._est_valide(y=1):
				self._calculer_donnees_piece_courante()
				self._poser_piece()
			else:
				print("On déplace vers le bas")
				self.position[1] += 1
				self._calculer_donnees_piece_courante()
                
	def _dessiner_plateau(self) -> None:
		"""dessine l'arrière-plan, la grille, les pièces et les statistiques du joueur

		Returns:
			None
		"""
		self.surface.fill(constantes.COULEURS.get(constantes.COULEUR_FOND))
		pygame.draw.rect(self.surface, constantes.COULEURS[8], constantes.START_PLABORD + constantes.TAILLE_PLABORD, constantes.BORDURE_PLATEAU)
		for i, ligne in enumerate(self.plateau):
			for j, case in enumerate(ligne):
				couleur = constantes.COULEURS[case]
				position = j, i
				coordonnees = tuple([constantes.START_PLATEAU[k] + position[k] * constantes.TAILLE_BLOC[k] for k in range(2)])
				pygame.draw.rect(self.surface, couleur, coordonnees + constantes.TAILLE_BLOC)
		if self.current is not None:
			for position in self.coordonnees:
				couleur = constantes.COULEURS.get(self._get_current_piece_color())
				coordonnees = tuple([constantes.START_PLATEAU[k] + position[k] * constantes.TAILLE_BLOC[k] for k in range(2)])
				pygame.draw.rect(self.surface, couleur, coordonnees + constantes.TAILLE_BLOC)
                
		self._afficher_texte(constantes.FORMAT_SCORE % self.score, constantes.POSITION_SCORE)
		self._afficher_texte(constantes.FORMAT_PIECES % self.pieces, constantes.POSITION_PIECES)
		self._afficher_texte(constantes.FORMAT_LIGNES % self.lignes, constantes.POSITION_LIGNES)
		self._afficher_texte(constantes.FORMAT_TETRIS % self.tetris, constantes.POSITION_TETRIS)
		self._afficher_texte(constantes.FORMAT_NIVEAU % self.niveau, constantes.POSITION_NIVEAU)

		self._rendre()
        
	def play(self) -> None:
		"""lance et maintient la boucle principale du jeu jusqu'à la défaite

		Returns:
			None
		"""
		print("Jouer")
		self.surface.fill(constantes.COULEURS.get(constantes.COULEUR_FOND))
		self._first()
		while not self.perdu:
			if self.current is None:
				self._next()
			self._gerer_evenements()
			self._gerer_gravite()
			self._dessiner_plateau()




if __name__ == '__main__':
	j = Jeu()
	print("Jeu prêt")
	j.start()
	print("Partie démarée")
	j.play()
	print("Partie terminée")
	j.stop()
	print("Arrêt du programme")
