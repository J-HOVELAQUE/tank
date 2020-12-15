#! /usr/bin/python3.5
# -*- coding : utf-8 -*

"""Tentative de création d'une classe pour générer un terrain de jeu aléatoire"""

from tkinter import *
from random import randrange,choice
import math

class Terrain(object):

	def __init__(self, surface, largeur, hauteur):

		self.largeur = largeur
		self.hauteur = hauteur

		self.vent = randrange(-10,10)

		self.aire = surface					# Ratacher au canvas du jeu
		self.skyline = [(0,hauteur//2)]		# La ligne d'horizon et son point de départ
		self.x = 0							# Coordonnées du point d'origine qui sera amené à évoluer
		self.y = hauteur//2

		## La liste des éléments de terrains:
		self.element = [self.generer_pente_asc,self.generer_pente_desc,self.generer_plateau]

		self.generation()					# Lancer la génération procédurale du terrain

	def generation(self):

		"""Tire un élément de terrain aléatoirement et l'ajoute à la ligne d'horizon"""

		while self.x < self.largeur:
			choice(self.element)(randrange(50,200),randrange(1,5))

		self.landscape = self.aire.create_polygon(self.skyline, self.largeur,self.hauteur,0,self.hauteur,fill='green',smooth=0, tag='terrain')

	def generer_pente_asc(self,longueur=200,pente=5):

		while longueur > 0:
			self.x += 1
			self.y -= randrange(0,5)*(pente/10)
			self.skyline.append((self.x,self.y))
			longueur -= 1

	def generer_pente_desc(self,longueur=200,pente=5):

		while longueur > 0:
			self.x += 1
			self.y += randrange(0,5)*(pente/10)
			self.skyline.append((self.x,self.y))
			longueur -= 1
		
	def generer_plateau(self,longueur=200,pente=5):

		while longueur > 0:
			self.x += 1
			self.skyline.append((self.x,self.y))
			longueur -= 1

	def destruction_circulaire(self, x0=200, r=20):

		"""Détruit une portion de terrain selon un cercle de rayon r au point x=x0"""

		gabarit = []

		for x in self.skyline[x0-r:x0+r]:

			newy = r**2 - (x[0]-x0)**2
			newy = math.sqrt(newy)
			newy = self.skyline[x0][1]+newy

			trou = (x[0],newy)
			gabarit.append(trou)

		self.skyline[x0-r:x0+r] = gabarit
		self.aire.delete(self.landscape)

		self.landscape = self.aire.create_polygon(self.skyline, 1200,800,0,800,fill='green',smooth=0,tag='terrain')


	def detruire(self, x0=100, x1=200):

		while x0 < x1:
			self.skyline[x0] = (self.skyline[x0][0],self.skyline[x0][1]+50)
			x0 += 1

		self.aire.delete(self.landscape)

		self.landscape = self.aire.create_polygon(self.skyline, 1200,800,0,800,fill='green',smooth=0)


	def casser(self,*event):

		self.destruction_circulaire()





if __name__ == "__main__":
	t = Tk()
	aire = Canvas(t, width=1200, height=800)
	landscape = Terrain(aire,1200,800)
	t.bind("<Return>",landscape.casser)
	aire.pack()
	t.mainloop()
