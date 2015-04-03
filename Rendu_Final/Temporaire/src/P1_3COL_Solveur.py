#!/usr/bin/env python
# -*- coding: utf-8-unix -*-

########################################################################
##																	  ##
##						       SOLVEUR                                ##
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
		##Initialisation avec le nom du sommet
        self.x = x
        ##Initialisation avec la couleur du sommet            
        self.color = color
        ##Initialisation d'un tableau des voisins du sommet      
        self.listeVoisin = set([])
        ##Compteur sur le nombre de voisins
        self.nbVoisin = 0
        ##Indicateur d'état (0 non visité / 1 visité)          
        self.visiter = 0           

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
		#Tableau de sommets
        self.v = set([])
        #Tableau d'arrêtes 
        self.e = set([])

	#Methode d'ajout d'un sommet dans le graph
    def add_v( self, Sommet ) :
		#Le sommeta ajouter est de type (Sommet)
        self.v.add( Sommet ) 
    
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
        
        ##Pour toutes les autres lignes (les arrêtes)        
        elif len( i.split( '--' ) ) == 2 :
			##On supprimer les retour à la ligne
            i = i.replace('\n', '')
            ##On récupére les deux sommets concernés
            (n,m) = map( str, i.split( '--' ) )
            ##On ajoute une arrête entre ces deux sommets dans le graph
            graph.add_e( [ (n,m) ] )
     
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

##Fonction qui verifie si tous les sommets du graph possédent bien une couleur
##   -- entrée : un graph
##   -- sortie : 0 - Tous les sommets sont coloriés
##               1 - Il reste des sommets non coloriés
def verification(graph):
    #on parcours les sommets
    for i in graph.v:
		#Verifie si le sommet à une couleur sinon --> Echec
		if i.color == "nothing":
			return 1
    return 0

##Fonction qui retourne un nombre "k" de couleur dans une liste de couleur
##   -- entrée : un entier, une liste de couleurs
##   -- sortie : une liste de couleurs 
def recup_liste_color(k,list_colors):
	list_Colors_Choix = []
	i = 0
	##NB : Pas de choix aléatoire , on prend dans l'ordre.
	while i < k:
		list_Colors_Choix.append(list_colors[i])
		i += 1
	return list_Colors_Choix

##Fonction qui test si une couleur "myColor" peut etre mise sur le sommet "S"
##On verifie qu'aucun de ses voisins ne possédent cette couleur
##   -- entrée : un graph , un sommet , une couleur
##   -- sortie : 0 - Ok pour attribuer la couleur au sommet
##               1 - Nok , un voisin posséde déja cette couleur
def test_color_voisin(myGraph,S,myColor):
	#On parcour les voisins
	for j in S.listeVoisin:
		#On recupere le sommet en cour
		tmpSommet = recupSommet(graph,j)
		#On verifie les couleurs
		if tmpSommet.color == myColor:
			return 1
	return 0

##Fonction principale qui resoud le probleme de coloriage d'un graph
##   -- entrée : un graph, un nombre de couleurs,la liste des couleurs, la liste des sommets, un sommet, le nombre de sommet
##   -- sortie : 0 - graph colorié
##               1 - Impossible de colorié le graph
def graphRecursive(myGraph,nbColor,allColors,lstSommets,numSommet,nbSommet):
	
	##On verifie si le graph est entiérement colorié
	if verification(myGraph) == 0 :
		return 0
	
	##On récupére le sommet (passé en paramétre) dans le graph
	sommetEnCour = recupSommet(myGraph,str(lstSommets[numSommet]))
	
	##Compteur pour le parcour de la liste des couleurs
	numColor = 0
	
	##On parcours toutes les couleurs possible pour le sommet
	while numColor < nbColor:
		
		##On verifie que la couleur en cour peut etre mise sur le sommet
		if test_color_voisin(myGraph,sommetEnCour,allColors[numColor]) == 0:
			
			##On attribue la couleur au sommet
			sommetEnCour.color = allColors[numColor]

			##On passe au sommet suivant
			if graphRecursive(myGraph,nbColor,allColors,lstSommets,numSommet+1,nbSommet) == 0:
				##Si le graph est entiérement colorié, on a la solution
				return 0
				
			##Si la couleur ne convient pas , on remet la couleur à "nothing"
			sommetEnCour.color = "nothing"
		
		##On passe à la couleur suivante
		numColor += 1
		
	return 1
	
##Programme principale
##   -- entrée : un fichier input au format d'un graph
##   -- sortie : 0 - graph coloriée
##               1 - graph impossible à colorier		
if __name__ == "__main__" :
		
	##Variable contient une liste de couleurs
	myListColor = ['snow', 'ghost white', 'white smoke', 'gainsboro', 'floral white', 'old lace',
    'linen', 'antique white', 'papaya whip', 'blanched almond', 'bisque', 'peach puff',
    'navajo white', 'lemon chiffon', 'mint cream', 'azure', 'alice blue', 'lavender',
    'lavender blush', 'misty rose', 'dark slate gray', 'dim gray', 'slate gray',
    'light slate gray', 'gray', 'light grey', 'midnight blue', 'navy', 'cornflower blue', 'dark slate blue',
    'slate blue', 'medium slate blue', 'light slate blue', 'medium blue', 'royal blue',  'blue',
    'dodger blue', 'deep sky blue', 'sky blue', 'light sky blue', 'steel blue', 'light steel blue',
    'light blue', 'powder blue', 'pale turquoise', 'dark turquoise', 'medium turquoise', 'turquoise',
    'cyan', 'light cyan', 'cadet blue', 'medium aquamarine', 'aquamarine', 'dark green', 'dark olive green',
    'dark sea green', 'sea green', 'medium sea green', 'light sea green', 'pale green', 'spring green',
    'lawn green', 'medium spring green', 'green yellow', 'lime green', 'yellow green',
    'forest green', 'olive drab', 'dark khaki', 'khaki', 'pale goldenrod', 'light goldenrod yellow',
    'light yellow', 'yellow', 'gold', 'light goldenrod', 'goldenrod', 'dark goldenrod', 'rosy brown',
    'indian red', 'saddle brown', 'sandy brown',
    'dark salmon', 'salmon', 'light salmon', 'orange', 'dark orange',
    'coral', 'light coral', 'tomato', 'orange red', 'red', 'hot pink', 'deep pink', 'pink', 'light pink',
    'pale violet red', 'maroon', 'medium violet red', 'violet red',
    'medium orchid', 'dark orchid', 'dark violet', 'blue violet', 'purple', 'medium purple',
    'thistle', 'snow2', 'snow3',
    'snow4', 'seashell2', 'seashell3', 'seashell4', 'AntiqueWhite1', 'AntiqueWhite2',
    'AntiqueWhite3', 'AntiqueWhite4', 'bisque2', 'bisque3', 'bisque4', 'PeachPuff2',
    'PeachPuff3', 'PeachPuff4', 'NavajoWhite2', 'NavajoWhite3', 'NavajoWhite4',
    'LemonChiffon2', 'LemonChiffon3', 'LemonChiffon4', 'cornsilk2', 'cornsilk3',
    'cornsilk4', 'ivory2', 'ivory3', 'ivory4', 'honeydew2', 'honeydew3', 'honeydew4',
    'LavenderBlush2', 'LavenderBlush3', 'LavenderBlush4', 'MistyRose2', 'MistyRose3',
    'MistyRose4', 'azure2', 'azure3', 'azure4', 'SlateBlue1', 'SlateBlue2', 'SlateBlue3',
    'SlateBlue4', 'RoyalBlue1', 'RoyalBlue2', 'RoyalBlue3', 'RoyalBlue4', 'blue2', 'blue4',
    'DodgerBlue2', 'DodgerBlue3', 'DodgerBlue4', 'SteelBlue1', 'SteelBlue2',
    'SteelBlue3', 'SteelBlue4', 'DeepSkyBlue2', 'DeepSkyBlue3', 'DeepSkyBlue4',
    'SkyBlue1', 'SkyBlue2', 'SkyBlue3', 'SkyBlue4', 'LightSkyBlue1', 'LightSkyBlue2',
    'LightSkyBlue3', 'LightSkyBlue4', 'SlateGray1', 'SlateGray2', 'SlateGray3',
    'SlateGray4', 'LightSteelBlue1', 'LightSteelBlue2', 'LightSteelBlue3',
    'LightSteelBlue4', 'LightBlue1', 'LightBlue2', 'LightBlue3', 'LightBlue4',
    'LightCyan2', 'LightCyan3', 'LightCyan4', 'PaleTurquoise1', 'PaleTurquoise2',
    'PaleTurquoise3', 'PaleTurquoise4', 'CadetBlue1', 'CadetBlue2', 'CadetBlue3',
    'CadetBlue4', 'turquoise1', 'turquoise2', 'turquoise3', 'turquoise4', 'cyan2', 'cyan3',
    'cyan4', 'DarkSlateGray1', 'DarkSlateGray2', 'DarkSlateGray3', 'DarkSlateGray4',
    'aquamarine2', 'aquamarine4', 'DarkSeaGreen1', 'DarkSeaGreen2', 'DarkSeaGreen3',
    'DarkSeaGreen4', 'SeaGreen1', 'SeaGreen2', 'SeaGreen3', 'PaleGreen1', 'PaleGreen2',
    'PaleGreen3', 'PaleGreen4', 'SpringGreen2', 'SpringGreen3', 'SpringGreen4',
    'green2', 'green3', 'green4', 'chartreuse2', 'chartreuse3', 'chartreuse4',
    'OliveDrab1', 'OliveDrab2', 'OliveDrab4', 'DarkOliveGreen1', 'DarkOliveGreen2',
    'DarkOliveGreen3', 'DarkOliveGreen4', 'khaki1', 'khaki2', 'khaki3', 'khaki4',
    'LightGoldenrod1', 'LightGoldenrod2', 'LightGoldenrod3', 'LightGoldenrod4',
    'LightYellow2', 'LightYellow3', 'LightYellow4', 'yellow2', 'yellow3', 'yellow4',
    'gold2', 'gold3', 'gold4', 'goldenrod1', 'goldenrod2', 'goldenrod3', 'goldenrod4',
    'DarkGoldenrod1', 'DarkGoldenrod2', 'DarkGoldenrod3', 'DarkGoldenrod4',
    'RosyBrown1', 'RosyBrown2', 'RosyBrown3', 'RosyBrown4', 'IndianRed1', 'IndianRed2',
    'IndianRed3', 'IndianRed4', 'sienna1', 'sienna2', 'sienna3', 'sienna4', 'burlywood1',
    'burlywood2', 'burlywood3', 'burlywood4', 'wheat1', 'wheat2', 'wheat3', 'wheat4', 'tan1',
    'tan2', 'tan4', 'chocolate1', 'chocolate2', 'chocolate3', 'firebrick1', 'firebrick2',
    'firebrick3', 'firebrick4', 'brown1', 'brown2', 'brown3', 'brown4', 'salmon1', 'salmon2',
    'salmon3', 'salmon4', 'LightSalmon2', 'LightSalmon3', 'LightSalmon4', 'orange2',
    'orange3', 'orange4', 'DarkOrange1', 'DarkOrange2', 'DarkOrange3', 'DarkOrange4',
    'coral1', 'coral2', 'coral3', 'coral4', 'tomato2', 'tomato3', 'tomato4', 'OrangeRed2',
    'OrangeRed3', 'OrangeRed4', 'red2', 'red3', 'red4', 'DeepPink2', 'DeepPink3', 'DeepPink4',
    'HotPink1', 'HotPink2', 'HotPink3', 'HotPink4', 'pink1', 'pink2', 'pink3', 'pink4',
    'LightPink1', 'LightPink2', 'LightPink3', 'LightPink4', 'PaleVioletRed1',
    'PaleVioletRed2', 'PaleVioletRed3', 'PaleVioletRed4', 'maroon1', 'maroon2',
    'maroon3', 'maroon4', 'VioletRed1', 'VioletRed2', 'VioletRed3', 'VioletRed4',
    'magenta2', 'magenta3', 'magenta4', 'orchid1', 'orchid2', 'orchid3', 'orchid4', 'plum1',
    'plum2', 'plum3', 'plum4', 'MediumOrchid1', 'MediumOrchid2', 'MediumOrchid3',
    'MediumOrchid4', 'DarkOrchid1', 'DarkOrchid2', 'DarkOrchid3', 'DarkOrchid4',
    'purple1', 'purple2', 'purple3', 'purple4', 'MediumPurple1', 'MediumPurple2',
    'MediumPurple3', 'MediumPurple4', 'thistle1', 'thistle2', 'thistle3', 'thistle4',
    'gray1', 'gray2', 'gray3', 'gray4', 'gray5', 'gray6', 'gray7', 'gray8', 'gray9', 'gray10',
    'gray11', 'gray12', 'gray13', 'gray14', 'gray15', 'gray16', 'gray17', 'gray18', 'gray19',
    'gray20', 'gray21', 'gray22', 'gray23', 'gray24', 'gray25', 'gray26', 'gray27', 'gray28',
    'gray29', 'gray30', 'gray31', 'gray32', 'gray33', 'gray34', 'gray35', 'gray36', 'gray37',
    'gray38', 'gray39', 'gray40', 'gray42', 'gray43', 'gray44', 'gray45', 'gray46', 'gray47',
    'gray48', 'gray49', 'gray50', 'gray51', 'gray52', 'gray53', 'gray54', 'gray55', 'gray56',
    'gray57', 'gray58', 'gray59', 'gray60', 'gray61', 'gray62', 'gray63', 'gray64', 'gray65',
    'gray66', 'gray67', 'gray68', 'gray69', 'gray70', 'gray71', 'gray72', 'gray73', 'gray74',
    'gray75', 'gray76', 'gray77', 'gray78', 'gray79', 'gray80', 'gray81', 'gray82', 'gray83',
    'gray84', 'gray85', 'gray86', 'gray87', 'gray88', 'gray89', 'gray90', 'gray91', 'gray92',
    'gray93', 'gray94', 'gray95', 'gray97', 'gray98', 'gray99']
    
	
	##On récupére l'input
	v = fileinput.input()
	
	##On initialise le graph
	graph = initialisationGraph(v)

	##On ajoute la liste des voisins pour chaque sommets
	ajout_Voisin(graph)
	
	##On récupére une liste de coleurs en fonction d'un nombre de couleurs voulu
	allColor = recup_liste_color(3,myListColor)

	##On récupére la liste des sommets
	list_sommet = []
	for i in graph.v:
		list_sommet.append(i.x)
	
	##On commence par le premier sommet de la liste
	##Il est possible d'emmetre une heuristique sur ce point
	firstSommet = 0

	##On lance la fonction de coloriage
	if graphRecursive(graph,3,allColor,list_sommet,0,len(list_sommet)) == 0:
		##Si le graph est colorié c'est gagné
		sys.exit(0)
	else:
		##Sinon pas gagné
		sys.exit(1)












