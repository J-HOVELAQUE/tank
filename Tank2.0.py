#! /usr/bin/python3.5
# -*- coding:utf-8 -*

from tkinter import *
from bombarde_prot import *
from obus_prot import *
from terrain_prot import *
#from explosion import *
from random import randrange
from time import sleep
import winsound


class JeuDeTank(object):

	def __init__(self, largeur=1200, hauteur=800, nb_joueurs=2):

		self.hauteur = hauteur														# Taille de l'aire de jeu
		self.largeur = largeur

		self.nb_joueurs = nb_joueurs

		self.root = Tk()															# Création de la fenètre d'interface
		self.aire = Canvas(self.root, width=self.largeur, height=self.hauteur)		# Création du canva de jeu

		self.font = PhotoImage(file='IMG_1495.gif')
		self.aire.create_image(600,400,image=self.font)

		self.aire.grid(row=1, column=1, columnspan=4)								# Affichage de l'interface

		self.terrain = Terrain(self.aire, self.largeur, self.hauteur)				# Création du terrain

		self.creation_des_joueurs(self.nb_joueurs)									# Lancer l'instanciation des joueurs
		self.changement_de_joueur()													# Pour lier les commandes

		if self.terrain.vent < 0:
			direction_vent = "<-"
		elif self.terrain.vent > 0:
			direction_vent = "->"
		elif self.terrain.vent == 0:
			direction_vent = " "

		self.info = Label(text="Vent :\n {} {}".format(direction_vent, abs(self.terrain.vent)))
		self.info.grid(row=2, column=2, columnspan=2)

		self.joueur1.info.grid(row=2, column=1)
		self.joueur2.info.grid(row=2, column=4)

		

		self.root.mainloop()

	def creation_des_joueurs(self, nb_joueurs):

		"""Instanciation des joueurs"""

		valide = False

		self.liste_des_joueurs = []

		while valide is False:

			pos_joueur_1 = randrange(10,self.largeur-10)
			

			pos_joueur_2 = randrange(10,self.largeur-10)
			

			if abs(pos_joueur_1 - pos_joueur_2) > 200:		# Vérifier que les deux joueurs sont assez éloigné
				valide = True

		self.joueur1 = Bombarde(self.aire, self.terrain, pos_joueur_1, self.terrain.skyline[pos_joueur_1][1], color='brown', name="joueur_1")
		self.liste_des_joueurs.append(self.joueur1)

		self.joueur2 = Bombarde(self.aire, self.terrain,pos_joueur_2 , self.terrain.skyline[pos_joueur_2][1], color='blue', name="joueur_2")
		self.liste_des_joueurs.append(self.joueur2)

		self.player_select = 1

	def replacer_joueurs(self):

		valide = False

		self.liste_des_joueurs = []

		while valide is False:

			pos_joueur_1 = randrange(10,self.largeur-10)
			

			pos_joueur_2 = randrange(10,self.largeur-10)
			

			if abs(pos_joueur_1 - pos_joueur_2) > 200:		# Vérifier que les deux joueurs sont assez éloigné
				valide = True

		self.joueur1.replacer(self.terrain, pos_joueur_1, self.terrain.skyline[pos_joueur_1][1])
		self.liste_des_joueurs.append(self.joueur1)

		self.joueur2.replacer(self.terrain,pos_joueur_2 , self.terrain.skyline[pos_joueur_2][1])
		self.liste_des_joueurs.append(self.joueur2)

		self.joueur1.maj_info()
		self.joueur2.maj_info()

		self.player_select = 1


	def tirer(self, *event):

		winsound.Beep(1000,200)

		self.root.unbind("<Return>")		# Impossible de lancer deux tir en même temps

		

		self.projectile = self.liste_des_joueurs[self.player_select].tirer()

		self.root.after(2000,self.bilan)

	def changement_de_joueur(self):

		""" Pour passer au joueur suivant"""

		self.player_select += 1
		if self.player_select >= len(self.liste_des_joueurs):
			self.player_select = 0

		### Redéterminer les commandes pour le joueur actif

		self.root.bind("<Left>",self.liste_des_joueurs[self.player_select].augmenter_angle)
		self.root.bind("<Right>",self.liste_des_joueurs[self.player_select].diminuer_angle)
		self.root.bind("<Up>",self.liste_des_joueurs[self.player_select].augmenter_force)
		self.root.bind("<Down>",self.liste_des_joueurs[self.player_select].diminuer_force)
		self.root.bind("<Return>",self.tirer)

		for traine in self.aire.find_withtag("trainée"):
				self.aire.delete(traine)

	def new_game(self):

		self.aire.delete(ALL)
		self.aire.create_image(600,400,image=self.font)

		self.terrain = Terrain(self.aire, self.largeur, self.hauteur)				# Création du terrain

		#self.creation_des_joueurs(self.nb_joueurs)									# Lancer l'instanciation des joueurs

		self.replacer_joueurs()
		self.changement_de_joueur()													# Pour lier les commandes

		if self.terrain.vent < 0:
			direction_vent = "<-"
		elif self.terrain.vent > 0:
			direction_vent = "->"
		elif self.terrain.vent == 0:
			direction_vent = " "

		self.info = Label(text="Vent :\n {} {}".format(direction_vent, abs(self.terrain.vent)))
		self.info.grid(row=2, column=2, columnspan=2)

		self.joueur1.info.grid(row=2, column=1)
		self.joueur2.info.grid(row=2, column=4)




	def bilan(self):

		"""Pour vérifier si un tank est détruit après un tir"""

		for tank in self.liste_des_joueurs:

			if tank.chassis in self.projectile.contours():
				winsound.Beep(100,1000)
				self.liste_des_joueurs.remove(tank)
				tank.destroy()

		if len(self.liste_des_joueurs) == 1:
			self.liste_des_joueurs[0].score += 1

			self.new_game()
		else:



			self.changement_de_joueur()


if __name__ == "__main__":
	jeu = JeuDeTank()
