import os
import time
import random

# Codes ANSI pour les couleurs
class Couleur:
    RESET = "\033[0m"
    GRAS = "\033[1m"
    ROUGE = "\033[91m"
    JAUNE = "\033[93m"
    BLEU = "\033[94m"
    CYAN = "\033[96m"
    FOND_BLEU = "\033[44m"
    FOND_ROUGE = "\033[41m"
    FOND_JAUNE = "\033[43m"
    FOND_BLANC = "\033[47m"
    FOND_RESET = "\033[49m"

class Puissance4:
    def __init__(self, lignes=6, colonnes=7):
        self.lignes = lignes
        self.colonnes = colonnes
        self.plateau = [[' ' for _ in range(colonnes)] for _ in range(lignes)]
        self.tour = 1
        self.dernier_coup = None
        self.en_cours = True
        # Utiliser deux espaces pour créer un cercle plus carré
        self.couleurs_joueurs = {
            1: Couleur.FOND_ROUGE + "  " + Couleur.FOND_RESET,
            2: Couleur.FOND_JAUNE + "  " + Couleur.FOND_RESET
        }
        # Représentation pour les cases vides
        self.case_vide = Couleur.FOND_BLANC + "  " + Couleur.FOND_RESET
        self.symboles_bruts = {
            1: "R",
            2: "J"
        }

    def afficher_plateau(self, jeton_en_mouvement=None):
        """Affiche le plateau avec des couleurs uniformes"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Calcul de la largeur totale du plateau
        largeur_totale = self.colonnes * 3 + 1
        
        # Ligne bleue supérieure
        print("\n" + Couleur.FOND_BLEU + " " * largeur_totale + Couleur.FOND_RESET)
        
        plateau_temp = [ligne.copy() for ligne in self.plateau]
        
        # Si un jeton est en mouvement, l'ajouter temporairement
        if jeton_en_mouvement:
            ligne, colonne, joueur = jeton_en_mouvement
            if 0 <= ligne < self.lignes and 0 <= colonne < self.colonnes:
                plateau_temp[ligne][colonne] = self.couleurs_joueurs[joueur]
        
        for ligne in plateau_temp:
            # Début de la ligne avec bord bleu
            ligne_affichage = Couleur.FOND_BLEU + " " + Couleur.FOND_RESET
            
            for case in ligne:
                if case == ' ':
                    # Case vide (fond blanc)
                    ligne_affichage += self.case_vide + Couleur.FOND_BLEU + " " + Couleur.FOND_RESET
                else:
                    # Case avec jeton (rouge ou jaune)
                    ligne_affichage += case + Couleur.FOND_BLEU + " " + Couleur.FOND_RESET
                    
            print(ligne_affichage)
            print(Couleur.FOND_BLEU + " " * largeur_totale + Couleur.FOND_RESET)
        
        # Afficher les numéros de colonnes
        print(" ", end="")
        for i in range(self.colonnes):
            print(f" {i+1} ", end="")
        print("\n")
        
        # Afficher le tour actuel
        joueur_actuel = (self.tour % 2) if (self.tour % 2) != 0 else 2
        couleur_fond = Couleur.FOND_ROUGE if joueur_actuel == 1 else Couleur.FOND_JAUNE
        print(f"Tour du joueur {joueur_actuel} {couleur_fond}  {Couleur.FOND_RESET}")

    def coup_valide(self, colonne):
        """Vérifie si un coup est valide"""
        if not (0 <= colonne < self.colonnes):
            return False
        return self.plateau[0][colonne] == ' '

    def jouer_coup(self, colonne, joueur):
        """Joue un coup et anime la chute du jeton"""
        if not self.coup_valide(colonne):
            return False
        
        # Trouver la ligne où le jeton va s'arrêter
        ligne = 0
        while ligne < self.lignes - 1 and self.plateau[ligne + 1][colonne] == ' ':
            ligne += 1
        
        # Animation de la chute du jeton
        for i in range(ligne + 1):
            self.afficher_plateau((i - 1, colonne, joueur) if i > 0 else None)
            if i < ligne:
                time.sleep(0.1)  # Vitesse de l'animation
        
        self.plateau[ligne][colonne] = self.couleurs_joueurs[joueur]
        self.dernier_coup = (ligne, colonne, self.symboles_bruts[joueur])
        self.tour += 1
        return True

    def verifier_victoire(self):
        """Vérifie si un joueur a gagné"""
        if not self.dernier_coup:
            return False
            
        ligne, colonne, symbole = self.dernier_coup
        
        # Déterminer le joueur actuel
        joueur_actuel = 1 if symbole == self.symboles_bruts[1] else 2
        
        # Simplification: Vérifier directement le fond de couleur pour déterminer le joueur
        def est_joueur_courant(cell):
            if cell == ' ':
                return False
            return (joueur_actuel == 1 and Couleur.FOND_ROUGE in cell) or (joueur_actuel == 2 and Couleur.FOND_JAUNE in cell)
        
        # Vérification horizontale
        for c in range(max(0, colonne - 3), min(colonne + 1, self.colonnes - 3)):
            if all(est_joueur_courant(self.plateau[ligne][c + i]) for i in range(4)):
                return True
                
        # Vérification verticale
        if ligne <= self.lignes - 4:
            if all(est_joueur_courant(self.plateau[ligne + i][colonne]) for i in range(4)):
                return True
                
        # Vérification diagonale (bas-droite)
        for i in range(-3, 1):
            if (0 <= ligne + i < self.lignes - 3 and 0 <= colonne + i < self.colonnes - 3):
                if all(est_joueur_courant(self.plateau[ligne + i + j][colonne + i + j]) for j in range(4)):
                    return True
                    
        # Vérification diagonale (haut-droite)
        for i in range(-3, 1):
            if (3 <= ligne + i < self.lignes and 0 <= colonne + i < self.colonnes - 3):
                if all(est_joueur_courant(self.plateau[ligne + i - j][colonne + i + j]) for j in range(4)):
                    return True
        
        return False

    def plateau_plein(self):
        """Vérifie si le plateau est plein"""
        return all(self.plateau[0][c] != ' ' for c in range(self.colonnes))

    def victoire_avec_effet(self, joueur):
        """Affiche un message de victoire avec effet"""
        os.system('cls' if os.name == 'nt' else 'clear')
        couleur = Couleur.ROUGE if joueur == 1 else Couleur.JAUNE
        fond = Couleur.FOND_ROUGE if joueur == 1 else Couleur.FOND_JAUNE
        
        for _ in range(3):  # Clignotement
            print("\n" * 3)
            print(couleur + Couleur.GRAS + "   VICTOIRE DU JOUEUR " + str(joueur) + "!!!" + Couleur.RESET)
            print("\n")
            print(couleur + "   " + "🎉 " * 10 + Couleur.RESET)
            print(couleur + "   " + "🎮 PUISSANCE 4 🎮" + Couleur.RESET)
            print(couleur + "   " + "🎉 " * 10 + Couleur.RESET)
            print("\n")
            print("   " + fond + "  " + Couleur.FOND_RESET + " Joueur " + str(joueur))
            print("\n" * 2)
            time.sleep(0.5)
            os.system('cls' if os.name == 'nt' else 'clear')
            time.sleep(0.2)

    def match_nul_avec_effet(self):
        """Affiche un message de match nul avec effet"""
        os.system('cls' if os.name == 'nt' else 'clear')
        
        for _ in range(3):  # Clignotement
            print("\n" * 3)
            print(Couleur.CYAN + Couleur.GRAS + "   MATCH NUL!" + Couleur.RESET)
            print("\n")
            print(Couleur.CYAN + "   " + "⚖️ " * 10 + Couleur.RESET)
            print(Couleur.CYAN + "   " + "🎮 PUISSANCE 4 🎮" + Couleur.RESET)
            print(Couleur.CYAN + "   " + "⚖️ " * 10 + Couleur.RESET)
            print("\n" * 3)
            time.sleep(0.5)
            os.system('cls' if os.name == 'nt' else 'clear')
            time.sleep(0.2)

    def jouer_contre_ia(self):
        """Mode de jeu contre l'IA"""
        self.afficher_plateau()
        self.en_cours = True
        
        while self.en_cours:
            joueur_actuel = (self.tour % 2) if (self.tour % 2) != 0 else 2
            
            if joueur_actuel == 1:  # Tour du joueur humain
                try:
                    choix = int(input("Choisissez une colonne (1-7): ")) - 1
                    if not self.jouer_coup(choix, joueur_actuel):
                        print(Couleur.ROUGE + "Coup invalide! Réessayez." + Couleur.RESET)
                        time.sleep(1)
                        continue
                except ValueError:
                    print(Couleur.ROUGE + "Veuillez entrer un nombre valide!" + Couleur.RESET)
                    time.sleep(1)
                    continue
            else:  # Tour de l'IA
                print("L'IA réfléchit...", end="", flush=True)
                time.sleep(random.uniform(0.5, 1.5))  # Simulation de réflexion
                
                # IA simple: essaie d'abord de gagner, puis bloque, sinon aléatoire
                choix = self.coup_ia()
                self.jouer_coup(choix, joueur_actuel)
            
            self.afficher_plateau()
            
            if self.verifier_victoire():
                self.victoire_avec_effet(joueur_actuel)
                self.en_cours = False
                break
                
            if self.plateau_plein():
                self.match_nul_avec_effet()
                self.en_cours = False
                break

    def coup_ia(self):
        """Logique simple pour l'IA"""
        # 1. Vérifier si l'IA peut gagner
        for col in range(self.colonnes):
            if self.coup_valide(col):
                # Simuler le coup
                ligne = 0
                while ligne < self.lignes - 1 and self.plateau[ligne + 1][col] == ' ':
                    ligne += 1
                
                self.plateau[ligne][col] = self.couleurs_joueurs[2]
                self.dernier_coup = (ligne, col, self.symboles_bruts[2])
                
                # Vérifier si c'est gagnant
                if self.verifier_victoire():
                    # Annuler la simulation
                    self.plateau[ligne][col] = ' '
                    self.dernier_coup = None
                    return col
                
                # Annuler la simulation
                self.plateau[ligne][col] = ' '
                self.dernier_coup = None
        
        # 2. Vérifier si le joueur peut gagner et bloquer
        for col in range(self.colonnes):
            if self.coup_valide(col):
                # Simuler le coup du joueur
                ligne = 0
                while ligne < self.lignes - 1 and self.plateau[ligne + 1][col] == ' ':
                    ligne += 1
                
                self.plateau[ligne][col] = self.couleurs_joueurs[1]
                self.dernier_coup = (ligne, col, self.symboles_bruts[1])
                
                # Vérifier si c'est gagnant pour le joueur
                if self.verifier_victoire():
                    # Annuler la simulation
                    self.plateau[ligne][col] = ' '
                    self.dernier_coup = None
                    return col
                
                # Annuler la simulation
                self.plateau[ligne][col] = ' '
                self.dernier_coup = None
        
        # 3. Jouer au centre si possible
        centre = self.colonnes // 2
        if self.coup_valide(centre):
            return centre
        
        # 4. Jouer aléatoirement
        coups_valides = [col for col in range(self.colonnes) if self.coup_valide(col)]
        if coups_valides:
            return random.choice(coups_valides)
        
        # Par défaut (ne devrait jamais arriver si plateau_plein() est vérifié)
        return 0

    def jouer_deux_joueurs(self):
        """Mode de jeu à deux joueurs"""
        self.afficher_plateau()
        self.en_cours = True
        
        while self.en_cours:
            joueur_actuel = (self.tour % 2) if (self.tour % 2) != 0 else 2
            
            try:
                choix = int(input(f"Joueur {joueur_actuel}, choisissez une colonne (1-7): ")) - 1
                if not self.jouer_coup(choix, joueur_actuel):
                    print(Couleur.ROUGE + "Coup invalide! Réessayez." + Couleur.RESET)
                    time.sleep(1)
                    continue
            except ValueError:
                print(Couleur.ROUGE + "Veuillez entrer un nombre valide!" + Couleur.RESET)
                time.sleep(1)
                continue
            
            self.afficher_plateau()
            
            if self.verifier_victoire():
                self.victoire_avec_effet(joueur_actuel)
                self.en_cours = False
                break
                
            if self.plateau_plein():
                self.match_nul_avec_effet()
                self.en_cours = False
                break

def afficher_menu():
    """Affiche le menu du jeu"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Couleur.CYAN + Couleur.GRAS + "\n" + "=" * 40 + Couleur.RESET)
    print(Couleur.CYAN + Couleur.GRAS + "           PUISSANCE 4" + Couleur.RESET)
    print(Couleur.CYAN + Couleur.GRAS + "=" * 40 + "\n" + Couleur.RESET)
    
    print("1. Jouer contre l'ordinateur")
    print("2. Jouer à deux joueurs")
    print("3. Quitter\n")
    
    choix = input(Couleur.JAUNE + "Votre choix: " + Couleur.RESET)
    return choix

def main():
    # Initialiser le terminal pour les couleurs sur Windows
    if os.name == 'nt':
        os.system('color')
        
    while True:
        choix = afficher_menu()
        
        if choix == '1':
            jeu = Puissance4()
            jeu.jouer_contre_ia()
            input(Couleur.CYAN + "\nAppuyez sur Entrée pour revenir au menu..." + Couleur.RESET)
        elif choix == '2':
            jeu = Puissance4()
            jeu.jouer_deux_joueurs()
            input(Couleur.CYAN + "\nAppuyez sur Entrée pour revenir au menu..." + Couleur.RESET)
        elif choix == '3':
            print(Couleur.CYAN + "\nMerci d'avoir joué à Puissance 4!" + Couleur.RESET)
            break
        else:
            print(Couleur.ROUGE + "\nChoix invalide. Veuillez réessayer." + Couleur.RESET)
            time.sleep(1)

if __name__ == "__main__":
    main()
