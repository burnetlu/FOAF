#!/usr/bin/env python
# -*- coding: utf-8-unix -*-

########################################################################
##																	  ##
##						     VERIFICATEUR                             ##
##																	  ##
########################################################################
##																	  ##
##						Info 724 - Projet de TP                       ##
##						 										      ##
##							M1 - STIC - Info                          ##
##							       									  ##
##							  2014 / 2015							  ##
##							  										  ##
##					  Caillet / Burnet / Mollard			          ##
##							  										  ##
########################################################################

import fileinput ## Package pour la gestion des input
import sys       ## Package pour la gestion du retour de la fonction

##Declaration d'une classe sommet
class Sommet:
	##Constructeur par defaut
    def __init__( self,x ,color):
        self.x = x                 ##Initialisation avec le nom du sommet
        self.color = color         ##Initialisation avec la couleur du sommet
        self.listeVoisin = set([]) ##Initialisation d'un tableau des voisins du sommet
        self.nbVoisin = 0          ##Compteur sur le nombre de voisins

	#Methode pour l'ajout d'un voisin
    def setVoisin(self,Sommet):
		##Ajout du sommet voisin à la liste des voisins
        self.listeVoisin.add(Sommet) 
        ##On incremente le compteur du nombre de voisins
        self.nbVoisin +=1 

##Declaration d'une classe graph
class Graph :
	#Constructeur par defaut
    def __init__( self ) :
        self.v = set([]) #Tableau de sommets
        self.e = set([]) #Tableau d'arrêtes

	#Methode d'ajout d'un sommet dans le graph
    def add_v( self, Sommet ) :
        self.v.add( Sommet ) #Le sommet et de type (Sommet)
    
    #Methode d'ajout d'une arrête dans le graph
    #On remarque ici que les sommets doivents êtres ajoutée avant les arrêtes
    def add_e( self, x ) :
        try :
            it = iter(x)
            for (u,v) in it :
                self.e.add( (u,v) )
        except TypeError :
            self.e.add( (u,v) )
 
##Fonction de récupération d'un sommet dans le graph
##   -- entrée : un graph , un nom de sommet
##   -- sortie : le sommet recherché 
def recupSommet(graph,x) :
    for i in graph.v:
        if i.x == x:
            ptrSommet = i
    return ptrSommet

##Fonction d'initialisation du graph (Creation des sommets, des arrêtes ...)
##   -- entrée : un fichier input
##   -- sortie : le graph avec les sommets et les arrêtes
def initialisationGraph(v):
    list_sommet = []
  
    ##On parcour chaque lignes du fichier input
    for i in v :
		
		##Pour la ligne n°1 on intialise un graph vide
        if v.filelineno() == 1 :
            graph = Graph()
            
        ##Pour la ligne n°2 on intialise les sommets
        if v.filelineno() == 2:
			##On récupére la lsite des sommets
            list_sommet = map(str, i.split(" ")) 
            ##On supprime le dernier (\n)
            list_sommet.pop()
            ##On ajoute les sommets de la liste             
            for j in list_sommet:
				##Initialisation du sommet "j" avec la couleur "nothing" (pas de couleur)
                mysommet = Sommet(j,"nothing") 
                ##On ajout le nouveau sommet dans le graph
                graph.add_v(mysommet) 
                
		##Pour les qui n'on que deux argument (les arrêtes)
        elif len( i.split( '--' ) ) == 2 :
			##On formatte la ligne (suppression retour à la ligne)
            i = i.replace('\n', '')
            ##On récupére les deux sommets
            (n,m) = map( str, i.split( '--' ) )
            #On ajoute l'arrête dans le graph
            graph.add_e( [ (n,m) ] )
            
        ##Pour les lignes qui ons 3 arguments (les couleurs)
        elif len( i.split( '--' ) ) == 3 :
			#On récupére les 3 arguments (c--nom_sommet--couleur)
			(n,m,o) = map( str, i.split( '--' ) )
			#On récupére le sommet concerné dans le graph
			mySommet = recupSommet(graph,m)
			#On lui attribu la couleur
			mySommet.color = o
			
    return graph

##Procédure pour l'ajout des voisins de chaques sommets du graph
##   -- entrée : un graph 
def ajout_Voisin(graph):
	##Parcours des sommets du graph
    for j in graph.v:
		##Parcours des arrêtes du graph
        for i in graph.e:
			##On verifie si le sommet j est un des sommets de l'arrête i
            if i[0] == j.x:
                j.setVoisin(i[1])
            elif i[1] == j.x:
                j.setVoisin(i[0])

##Fonction la couleur de chaques sommets par rapports à leurs voisins
##   -- entrée : un graph
##   -- sortie : 0 - Graph bien coloré
##               1 - Graph mal coloré
def verification(graph):
	#on parcours les sommets
	for i in graph.v:
		#pour chaque sommet on parcours ces voisins
		for j in i.listeVoisin:
			mySommet = recupSommet(graph,j)
			if mySommet.color == i.color:
				return 1
	return 0


##Programme principale
##   -- entrée : un fichier input au format d'un graph + un certificat au bon format de certificat (voir README + Documentation)
##   -- sortie : 0 - graph bien colorié
##               1 - graph mal colorié
if __name__ == "__main__" :
	##On récupérer le fichier input
	v = fileinput.input()

	##On initialise le graph avec le fichier input
	graph = initialisationGraph(v)
	
	##On ajout les voisins des sommets
	ajout_Voisin(graph)
	
	##On fait la verification et on retourne le resultat
	sys.exit(verification(graph))
















		

