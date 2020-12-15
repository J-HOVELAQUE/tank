#! /usr/bin/python3.5
# -*- coding:utf-8 -*

from tkinter import *
from obus_prot import *
import math
from time import sleep
from terrain_prot import *

class Bombarde(object):

	def __init__(self, aire, terrain, x, y, score = 0, angle=90,name="player 1", color='dark red'):

		self.aire = aire			# Canva rattaché
		self.x, self.y = x, y 		# Coordonnées du centre du tank
		self.angle = angle 			# Angle d'origine du canon
		self.color = color			# Couleur du tank
		self.force = 75 			# Force de départ

		self.name = name
		self.broken = False

		self.score = score				# Nombre de manche remportées

		self.terrain = terrain 		# Le terrain sur lequel est posée la bombarde

		self.chassis = self.aire.create_arc(self.x-15, self.y-15, self.x+15, self.y+15, start=0, extent=180,fill=self.color,tag='tank')	# Dessiner le corp
		self.canon = self.aire.create_line(self.x, self.y,\
		 self.x + 30*math.cos(math.radians(self.angle)), self.y - 30*math.sin(math.radians(self.angle)),\
		 width=3,fill=self.color,tag='tank')																							# Dessiner le canon

		self.info = Label(text="Angle : {}\nPuissance : {}\n\nScore : {}".format(self.angle, self.force, self.score), fg=self.color)


	def augmenter_angle(self, *event):

		"""Augmente l'angle du canon"""

		if self.angle < 180:
			self.angle += 1
			self.aire.coords(self.canon,self.x,self.y,self.x+30*math.cos(math.radians(self.angle)),self.y-30*math.sin(math.radians(self.angle)))

		self.maj_info()
		
	def diminuer_angle(self, *event):

		"""Diminue l'angle du canon"""

		if self.angle > 0:
			self.angle -= 1
			self.aire.coords(self.canon,self.x,self.y,self.x+30*math.cos(math.radians(self.angle)),self.y-30*math.sin(math.radians(self.angle)))

		self.maj_info()

	def augmenter_force(self, *event):

		"""Augmente la puissance du tir"""

		self.force += 1
		self.maj_info()

	def diminuer_force(self, *event):

		"""Diminue la puissance du tir"""

		self.force -= 1
		self.maj_info()


	def tirer(self, *event):

		"""Pour initialiser un tir d'obus"""

		projectile = Projectile(self.aire, self.terrain, self.x, self.y, self.angle, self.force)
		return projectile

	def destroy(self):

		"""Détruit le tank"""

		self.aire.delete(self.chassis)
		self.aire.delete(self.canon)
		self.broken = True

	def maj_info(self):

		"""Renvoi l'angle et la puissance sous forme de chaine en vue de les afficher"""

		self.info.configure(text="Angle : {}\nPuissance : {}\n\nScore : {}".format(self.angle, self.force, self.score))

	def replacer(self, terrain, x, y, angle = 45):

		self.aire.delete(self.chassis)
		self.aire.delete(self.canon)

		self.angle = 90
		self.force = 75

		self.terrain = terrain

		self.x, self.y = x, y 		# Coordonnées du centre du tank

		self.chassis = self.aire.create_arc(self.x-15, self.y-15, self.x+15, self.y+15, start=0, extent=180,fill=self.color,tag='tank')	# Dessiner le corp
		self.canon = self.aire.create_line(self.x, self.y,\
		 self.x + 30*math.cos(math.radians(self.angle)), self.y - 30*math.sin(math.radians(self.angle)),\
		 width=3,fill=self.color,tag='tank')																							# Dessiner le canon

class JoueurDeTank(object):

	def __init__(self, aire, terrain, x, y, angle=45,name="player 1", color='dark red'):

		self.tank = Bombarde(aire, terrain, x, y, angle=45,name="player 1", color='dark red')




if __name__ == "__main__":

	test = Tk()

	aire = Canvas(test, height= 800, width=1400)
	aire.pack()

	tank = Bombarde(aire, 500,800)

	test.bind("<Left>",tank.augmenter_angle)
	test.bind("<Right>",tank.diminuer_angle)
	test.bind("<Up>",tank.augmenter_force)
	test.bind("<Down>",tank.diminuer_force)
	test.bind("<Return>",tank.tirer)

	test.mainloop()