#!/usr/bin/env python
# -*- coding: utf-8-unix -*-

########################################################################
##																	  ##
##						       REDUCTEUR                              ##
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

##On declare une class Graph afin de generer un graph depuis le fichier
##en input.
class Graph :
	##Constructeur de la classe
    def __init__( self ) :
		#Tableau de sommets initialisé à vide
        self.v = set([])
        #Tableau d'arrêtes initialisé à vide 
        self.e = set([]) 
        
    ##Methode permettant l'ajout d'un, ou plusieurs sommets dans le graph.
    def add_v( self, x ) :
        try :
            it = iter(x)
            for i in it :
                self.v.add( i )
        except TypeError :
            self.v.add(x)
            
    ##Methode permettant l'ajout d'une, ou plusieurs arrêtes dans le graph.
    ##L'ajout d'une arrete induit l'ajout des deux sommets.
    def add_e( self, x ) :
        try :
            it = iter(x)
            for (u,v) in it :
                self.v.add( u )
                self.v.add( v )
                self.e.add( (u,v) )
        except TypeError :
            self.v.add( u )
            self.v.add( v )
            self.e.add( (u,v) )
            

##Fonction pour l'affichage du graph en console , permet le chainage
##avec le Solveur ( "instance_P2" | reducteur | solveur )
##	-- entrée : Un graph
##  -- sortie : Un affichage correcte pour le solveur
def affichage_graph(g):
	vertices = ""
	for i in g.v :
		vertices += "{} ".format( i )
	edges = ""
	for i in g.e :
		edges += "{}--{}\n".format( i[0], i[1] )
	print( "Graph {" )
	print( vertices )
	print( edges + "}" )


##Construction du graph special avec les trois sommets V, F, R (gadget)
##Dans ce code ces 3 sommets sont appellé sp1,sp2,sp3
##sp1 sera le sommet ou seul sp2 et sp3 sont reliés
##sp2 sera le sommet ou les arretes du gadget sont reliée (sortie unique du gadget (Pas les variables))
##sp3 sera le sommet ou les arretes des variables et leurs négation sont reliées.
##D'avantage d'information sont disponible dans la Documentation. (./Documentation.pdf)

##Fonction construction du graph
##    -- entrée : Un graph au format suivant (Input)
##
##	  Graph{
##		1,2,3,4,... //Liste des sommets
##      1--2        //Les arrêtes du graph
##      2--3 
##      ...
##      }
##
##	  -- Sortie : Un graph
def construction_graph(v):
	##Variable de compteur qui s'incrémente en fonction du nombres de clauses de l'input.
	C = 0 
	
	for s in v :

		if s in [ "3SAT {\n", "3-SAT {\n" ] :
			##Pour la premiére ligne de l'entrée (3SAT), on creer le graph
			g = Graph()
			
			##On ajoute le triangle avec les sommets spéciaux (gadget)
			g.add_e( [ ("sp1", "sp2"), ("sp2","sp3"), ("sp1","sp3") ] )
			
		elif len( s.split( ' ' ) ) == 2 :
			##On récupére la premiére ligne qui nous donne le nombre de variables et le nombres de clauses de l'entrée
			(n,m) = map( int, s.split( ' ' ) )
			
			##On creer 2n sommets pour avoir la variable + sa négation
			g.add_v( [ (i) for i in range( 1, n+1 ) ] )
			g.add_v( [ (-i) for i in range( 1, n+1 ) ] )
			
			##On ajoute les trois nouvelles arrêtes
			## 1) --> entre les deux sommet (Vairable + sa négation) 
			## 2) --> entre les deux sommets et notre triangle spécial (sommet sp3)
			g.add_e( [ (i,-i) for i in range( 1, n+1 ) ] )
			g.add_e( [ (i,"sp3") for i in range( 1, n+1 ) ] )
			g.add_e( [ (-i,"sp3") for i in range( 1, n+1 ) ] )
			
		elif len( s.split( ' ' ) ) == 3 :
			##Pour chaque clause on fait :
			##On récupére les trois variabes de la clause de 3SAT
			(a,b,c) = map( int, s.split( ' ' ) )
			
			##On creer le gadget (5 sommets de C0 à C4)
			C0 = "C" + str(C) + "n0"
			C1 = "C" + str(C) + "n1"
			C2 = "C" + str(C) + "n2"
			C3 = "C" + str(C) + "n3"
			C4 = "C" + str(C) + "n4"
			
			## On fait les liens entre les sommets spéciaux (5 nouvelles arrêtes)
			g.add_e( [ (C0, C1), (C0, C2), (C2, C3), (C2, C4), (C3, C4) ] )
			
			## On relie les sommets (a,b,c) présent dans la clause avec notre gadget (5 arrêtes)
			## 2 arrêtes reliées à notre triangle spécial (sp2, voir ci-dessus)
			## 3 arrêtes reliées au variable de la clause 
			g.add_e([(a,C3),(b,C4),(c,C1),(C0, "sp2"),(C1, "sp2")])
			
			#On incrémente le compteur de nombre de clauses
			C += 1
	return g
			
##Fonction principale du programme
##   -- Entrée : Un input (instance de 3SAT)
##   -- Sortie : Affichage du graph au bon format pour le solveur
if __name__ == "__main__" :
	
	##récupération de l'Input
	v = fileinput.input()

	##Création du graph
	myGraph = construction_graph(v)
	
	##Affichage du graph
	affichage_graph(myGraph)
	
	
	
