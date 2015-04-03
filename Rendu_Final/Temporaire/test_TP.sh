#!/bin/bash
# 
# TP - INFO724
# Année 2014-2015
# 
# Fichier : test_TP.sh
# Auteur : Xavier Provençal
# 
# Le but de ce script est de vous aider à tester votre TP. 
# 
# LE FAIT QU'IL S'EXÉCUTE SANS ERREURS NE SIGBIFIE PAS QUE VOUS PROGRAMMES SONT
# VALIDE. Cepedant, s'il produit une erreur, c'est forcément qu'il y a un
# problème avec vos programmes. Cela dit, il est possible que vos programmes
# soient valides mais qu'ils mettent un temps extrêment long à terminer.
# Particulièrement dans le cas d'une instance obtenue par le programme de
# réduction. Cela est normal car la réduction à tendance à produire des
# instances plus grandes que celles fournies en entrée.
# 
#
# Avant d'utiliser ce script, vous devez NÉCESSAIREMENT le reconfigurer.
#


#######################################################################
#######################################################################
# CONFIGURATION
#
#

# Ce script est destiné à vous aider à tester vos programmes.
# Les trois prorgammes
VERIFICATEUR="./src/P1_3COL_Verificateur.py"
SOLVER="./src/P1_3COL_Solveur.py"
REDUCTEUR="./src/P1_3COL_Reducteur.py"

# P1 est le problème principal, celui dont veut montrer qu'il est NP-Complet
INSTANCE_P1_VRAI="./instances/P1_3COL_Instance_Vrai.txt"
INSTANCE_P1_FAUX="./instances/P1_3COL_Instance_Faux.txt"
	
# Certificats pour l'instance VRAI de P1
CERTIF_VALIDE_POUR_INSTANCE_P1_VRAI="./instances/P1_3COL_Certificat.txt"

# P2 est un problème qu'on sait être NP-Complet. Ces instances seront traitées
# par le programme de réduction afin de produires des instance de P1.
INSTANCE_P2_VRAI="./instances/P2_3SAT_Instance_Vrai.txt"
INSTANCE_P2_FAUX="./instances/P2_3SAT_Instance_Faux.txt"

#
#
# FIN DE LA CONFIGURATION
#######################################################################
#######################################################################

test_solver() {
	# Teste la présence des fichiers nécessaires
	if [ ! -f $SOLVER ] ; then
		echo "ERREUR : le programme solver n'exite pas."
		usage
		exit 1
	elif [ ! -f $INSTANCE_P1_VRAI ] ; then
		echo "ERREUR : l'instance P1 VRAI n'existe pas."
		usage
		exit 1
	elif [ ! -f $INSTANCE_P1_FAUX ] ; then
		echo "ERREUR : l'instance P1 FAUX n'existe pas."
		usage
		exit 1
	fi
	echo "############################################################"
	echo "Test : Solver sur instance vrai... "
	cat ${INSTANCE_P1_VRAI} |  ${SOLVER} 
	if [ $? == 0 ] ; then
	    echo "OK"
	else 
	    echo "Echec !"
	    echo "La commande suivante a échouée :"
	    echo "cat ${INSTANCE_P1_VRAI} |  ${SOLVER}"
	    exit 1
	fi

	echo "Test : Solver sur instance fausse... "
	cat ${INSTANCE_P1_FAUX} | ${SOLVER} 
	if [ $? != 0 ] ; then
	    echo "OK"
	else 
	    echo "Echec !"
	    echo "La commande suivante a échouée :"
	    echo "cat ${INSTANCE_P1_FAUX} | ${SOLVER}"
	    exit 1
	fi
	echo "############################################################"
	return 0
}

test_reduc() {
	# Teste la présence des fichiers nécessaires
	if [ ! -f $REDUCTEUR ] ; then
		echo "ERREUR : le programme réducteur n'exite pas."
		usage
		exit 1
	elif [ ! -f $SOLVER ] ; then
		echo "ERREUR : le programme solver n'exite pas."
		usage
		exit 1
	elif [ ! -f $INSTANCE_P2_VRAI ] ; then
		echo "ERREUR : l'instance P2 VRAI n'existe pas."
		usage
		exit 1
	elif [ ! -f $INSTANCE_P2_FAUX ] ; then
		echo "ERREUR : l'instance P2 FAUX n'existe pas."
		usage
		exit 1
	fi
	echo "############################################################"
	echo "Test : Réduction d'une instance vrai..."
	cat ${INSTANCE_P2_VRAI} | ${REDUCTEUR} | ${SOLVER} 
	if [ $? == 0 ] ; then
	    echo "OK"
	else 
	    echo "Echec !"
	    echo "La commande suivante a échouée :"
	    echo "cat ${INSTANCE_P2_VRAI} | ${REDUCTEUR} | ${SOLVER}"
	    exit 1
	fi

	echo "Test : Réduction d'une instance fausse..."
	cat ${INSTANCE_P2_FAUX} | ${REDUCTEUR} | ${SOLVER} 
	if [ $? != 0 ] ; then
	    echo "OK"
	else 
	    echo "Echec !"
	    echo "La commande suivante a échouée :"
	    echo "cat ${INSTANCE_P2_FAUX} | ${REDUCTEUR} | ${SOLVER}"
	    exit 1
	fi
	echo "############################################################"
	return 0
}

test_verif() {
	# Teste la présence des fichiers nécessaires
	if [ ! -f $VERIFICATEUR ] ; then
		echo "ERREUR : le programme vérificateur n'exite pas."
		usage
		exit 1
	elif [ ! -f $INSTANCE_P1_VRAI ] ; then
		echo "ERREUR : l'instance P1 VRAI n'existe pas."
		usage
		exit 1
	elif [ ! -f $INSTANCE_P1_FAUX ] ; then
		echo "ERREUR : l'instance P1 FAUX n'existe pas."
		usage
		exit 1
	elif [ ! -f $CERTIF_VALIDE_POUR_INSTANCE_P1_VRAI ] ; then
		echo "ERREUR : le certificat n'existe pas"
		usage
		exit 1
	fi
	echo "############################################################"
	echo "Test : Vérification avec certificat valide..."
	cat ${INSTANCE_P1_VRAI} ${CERTIF_VALIDE_POUR_INSTANCE_P1_VRAI} | ${VERIFICATEUR} 
	if [ $? == 0 ] ; then
	    echo "OK"
	else 
	    echo "Echec !"
	    echo "La commande suivante a échouée :"
	    echo "cat ${INSTANCE_P1_VRAI} ${CERTIF_VALIDE_POUR_INSTANCE_P1_VRAI} | ${VERIFICATEUR}"
	    exit 1
	fi
	echo "Test : Vérification d'une instance invalide..."
	cat ${INSTANCE_P1_FAUX} ${CERTIF_VALIDE_POUR_INSTANCE_P1_VRAI} | ${VERIFICATEUR} 
	if [ $? != 0 ] ; then
	    echo "OK"
	else 
	    echo "Echec !"
	    echo "La commande suivante a échouée :"
	    echo "cat ${INSTANCE_P1_FAUX} ${CERTIF_VALIDE_POUR_INSTANCE_P1_VRAI} | ${VERIFICATEUR}"
	    exit 1
	fi
	echo "############################################################"
	return 0
}

usage()
{
	echo "Usage : $0 [options]"
	echo ""
	echo "Options :"
	echo "  --tout     Effectue tous les test (activé par défaut)."
	echo ""
	echo "  --verif    Teste de programme vérification."
	echo ""
	echo "  --solver   Teste le solver."
	echo ""
	echo "  --reduc    Teste le programme de réduction, le résultat de la réduction"
	echo "             est envoyé au solver pour s'assurer de sa validité"
	echo ""
	echo "  --IP1V fichier   Spécifie le fichier contenant une instance de P1 pour"
	echo "                   laquelle la réponse est OUI."
	echo ""
	echo "  --IP1F fichier   Spécifie le fichier contenant une instance de P1 pour"
	echo "                   laquelle la réponse est NON."
	echo ""
	echo "  --IP2V fichier   Spécifie le fichier contenant une instance de P2 pour"
	echo "                   laquelle la réponse est OUI."
	echo ""
	echo "  --IP2F fichier   Spécifie le fichier contenant une instance de P2 pour"
	echo "                   laquelle la réponse est NON."
	echo ""
	echo "  --CERT fichier   Spécifie le fichier contenant un certificat valide pour"
	echo "                   l'instance de P1 dont la réponse est OUI."
	echo ""
	echo "  --help           Affiche cet aide."
	echo ""
	echo "Valeurs par défaut :"
	echo "  Programme de vérification : ${VERIFICATEUR}"
	echo "  Programme solver :          ${SOLVER}"
	echo "  Programme de réduction :    ${REDUCTEUR}"
	echo "  Instance VRAI de P1 :       ${INSTANCE_P1_VRAI}"
	echo "  Instance FAUX de P1 :       ${INSTANCE_P1_FAUX}"
	echo "  Instance VRAI de P2 :       ${INSTANCE_P2_VRAI}"
	echo "  Instance FAUX de P2 :       ${INSTANCE_P2_FAUX}"
	echo "  Certificat pour P1 VRAI :   ${CERTIF_VALIDE_POUR_INSTANCE_P1_VRAI}"
	echo ""
}

TEST_TOUT="oui"
TEST_VERIF="non"
TEST_SOLVER="non"
TEST_REDUC="non"

while [ $# -ge 1 ] ; do
	if [ $1 == "--tout" ] ; then
		TEST_TOUT="oui"
	elif [ $1 == "--verif" ] ; then
		TEST_TOUT="non"
		TEST_VERIF="oui"
	elif [ $1 == "--solver" ] ; then
		TEST_TOUT="non"
		TEST_SOLVER="oui"
	elif [ $1 == "--reduc" ] ; then
		TEST_TOUT="non"
		TEST_REDUC="oui"
	elif [ $1 == "--help" ] ; then
		usage
		exit 0
	elif [ $1 == "--IP1V" ] ; then
		shift
		INSTANCE_P1_VRAI=$1
	elif [ $1 == "--IP1F" ] ; then
		shift
		INSTANCE_P1_FAUX=$1
	elif [ $1 == "--IP2V" ] ; then
		shift
		INSTANCE_P2_VRAI=$1
	elif [ $1 == "--IP2F" ] ; then
		shift
		INSTANCE_P2_FAUX=$1
	elif [ $1 == "--CERT" ] ; then
		shift
		CERTIF_VALIDE_POUR_INSTANCE_P1_VRAI=$1
	else 
		usage
		exit 1
	fi
	shift
done
if [ $TEST_TOUT == "oui" ] ; then
	TEST_VERIF="oui"
	TEST_SOLVER="oui"
	TEST_REDUC="oui"
fi

if [ $TEST_VERIF == "oui" ] ; then
	test_verif
fi

if [ $TEST_SOLVER == "oui" ] ; then
	test_solver
fi

if [ $TEST_REDUC == "oui" ] ; then
	test_reduc
fi

exit 0
