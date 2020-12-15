#! /usr/bin/python3.5
# -*- coding : utf -8 -*

"""Tentative de définir un projectile en tant que classe"""

from tkinter import *
from terrain_prot import *
import winsound

import math

class Projectile(object):

	def __init__(self, surface, terrain, x0, y0, angle, puissance, gravite = 0.4, vent = 0, vitesse = 5, rayon_explosion=20):

		
		self.etat = False

		self.x0 = x0																			# Position de la bombarde faisant feu
		self.y0 = y0

		self.aire = surface																		# Canvas attaché
		self.terrain = terrain 																	# Environement dans lequel l'obus est lancé
		self.obstacles = self.aire.find_withtag("terrain") + self.aire.find_withtag("tank")
		self.angle = angle																		# Angle du canon faisant feu
		self.force = puissance/10																# Puissance de feu
		self.g = gravite 																		# Force d'attraction de la planète
		self.vent = self.terrain.vent 															# Force du vent
		self.vitesse = vitesse 																	# Vitesse du tir

		self.evolution = True 																	# Si l'obus est toujour en progression

		self.progression = 0																	# Progression de l'explosion
		self.rayon = rayon_explosion

		self.t = 0																				# Instant de départ
		self.curve = [(self.x0 + 30*math.cos(math.radians(self.angle)), self.y0 - 30*math.sin(math.radians(self.angle)))]	# Origine de la trajectoire (extrémitée du canon)
		self.x, self.y = self.x0 + 30*math.cos(math.radians(self.angle)), self.y0 - 30*math.sin(math.radians(self.angle))	# Point de départ de l'obus

		self.trajectoire_recursive(self.g, self.vent, self.vitesse)								# Mise à feu

	


	def trajectoire_recursive(self, g=0.1, vent=0, vitesse_tir=5):

		"""Dessine la trajectoire (curve) d'un obus point par point en fonction de :
			- l'angle du canon (self.angle)
			- la puissance de feu (self.force)
			- la force de gravitée (g)
			- la force du vent (vent) (idéalement entre -10 et 10)

			prend aussi en compte la vitesse d'affichage : vitesse_tir
			"""

		self.etat = True

		angle = math.radians(self.angle)											# Conversion de l'angle du canon en radians
		vent = self.vent/300 															# Etalonnage du vent

		x = (vent * (self.t**2) / 2) + (self.force * math.cos(angle) * self.t)		# Application des equations horaires de la trajectoire (instant t)
		y = - ((g * (self.t**2)) / 2) + (self.force * math.sin(angle) * self.t)

		self.y = -y + (self.y0 - 30*math.sin(angle))								# Determiner position actuelle de l'obus
		self.x = x + (self.x0 + 30*math.cos(angle))

		self.curve.append((self.x,self.y))											# Continuer de tracer la trajectoire
		self.aire.create_line(self.curve, fill='red', smooth=True, tag="trainée")
		del self.curve[0]

		for obs in self.obstacles:													# Faire exploser l'obus au contact du terrain
			if obs in self.aire.find_overlapping(self.x,self.y,self.x,self.y):
				if self.t != 0:

					self.explosion()
					self.evolution = False


		self.t += 1  																# Passer à l'instant suivant

		if self.t < 1000 and self.evolution is True:								# Poursuivre l'évolution de l'obus si conditions valides
			self.aire.after(self.vitesse , self.trajectoire_recursive)
		else:
			self.etat = False
			

	def explosion(self, vitesse=10):

		"""Animation de l'explosion jusqu'à atteindre le rayon souhaité"""

		

		self.aire.create_oval\
			(self.x-self.progression,self.y-self.progression,self.x+self.progression,self.y+self.progression,\
				fill='red',tag='explosion')

		self.progression += 1

		if self.progression < self.rayon:					# On vérifie si l'expmosion est terminée
			self.aire.after(vitesse,self.explosion)
		else:
			self.aire.after(200,self.effacer_explosion)

	def effacer_explosion(self):

		"""Effacer l'explosion et casser le terrain en conséquence"""

		for cercle in self.aire.find_withtag("explosion"):
			self.aire.delete(cercle)

		self.terrain.destruction_circulaire(int(self.x),self.rayon)
		winsound.Beep(100,1000)
		

	def contours(self):

		return self.aire.find_overlapping(self.x-self.rayon,self.y-self.rayon,self.x+self.rayon,self.y+self.rayon)


