```markdown
# Crime a Montfleur – Jeu d'Aventure Textuel en Python

## 1. Introduction
Crime a Montfleur est un jeu d’aventure textuel dans lequel le joueur incarne un enquêteur chargé de résoudre un meurtre.  
Le jeu repose sur l’exploration, la collecte d’indices, l’analyse d’objets et l’interrogation de personnages non joueurs.  
L’objectif est d’identifier le coupable avant la fin du temps imparti.

Objectif principal :
- Explorer les salles
- Collecter les 6 objets importants
- Les analyser au laboratoire
- Parler au Chimiste pour obtenir les resultats
- Accuser Durand au Commissariat
- Ne pas depasser 40 deplacements

Public cible :
- Etudiants en Python
- Amateurs de jeux textuels
- Joueurs aimant les enigmes

---

## 2. Installation

Prerequis :
- Python 3.7 ou superieur
- Terminal ou invite de commande

Installation :
```bash
git clone https://github.com/DanielCourivaud/TBA.git
cd TBA
python game.py
```

---

## 3. Univers du jeu

Le jeu se deroule dans la ville de Montfleur.  
Un meurtre a eu lieu dans la Maison du crime.  
Plusieurs suspects, des indices disperses et un delai limite rendent l’enquete complexe.

Elements importants :
- Atmosphere de mystere
- Temoins peu fiables
- Indices caches dans plusieurs salles
- Progression narrative lineaire

---

## 4. Regles du jeu

Conditions de victoire :
1. Analyser les 6 objets : couteau, cle, lettre, coffre, photos, arme  
2. Parler au Chimiste apres les analyses  
3. Accuser Durand au Commissariat(il faut avoir les 6 objets analysés sinon le policier nous demande de trouver des preuves)
4. Ne pas depasser 40 deplacements

Conditions de defaite :
- Accuser la mauvaise personne
- Depasser 40 deplacements

Deplacements gratuits :
- Grenier
- Cave
- Jardin
- Labo

---

## 5. Commandes
(Important: Ne mettez pas d'espaces après les <...> !)
Navigation :
- `go <direction>`  
- `back`  
- `history`  

Exploration :
- `look`  
- `check`  
- `take <objet>`  
- `drop <objet>`  
- `examine <objet>`  

Interaction :
- `talk <nom>`  
- `use <objet1> on <objet2>`  
- `analyze <objet>`  
- `accuse <nom>`  

Systeme :
- `help`  
- `quests`  
- `quit`  

Directions : N, E, S, O, U, D

---

## 6. Carte du jeu

### Vue d'ensemble des 13 salles

VUE D'ENSEMBLE DES 13 SALLES

labo___Commissariat ___Morgue    Durand               Grenier
              |                    |                 //
             cafe___________Rue Montfleur ___ Maison_crime _____ Jardin
                                  |                 //
                                Lenoir            Cave
                                  |
                                 Parc ___ Bibliotheque
```

Salles principales :
- Rue de Montfleur (hub)
- Maison du crime
- Maison de Durand
- Maison de Lenoir
- Cafe
- Commissariat
- Parc
- Bibliotheque
- Grenier
- Cave
- Jardin
- Morgue
- Labo

Exemples de connexions :
- Rue -> Maison du crime (E)
- Maison du crime -> Grenier (U)
- Maison du crime -> Cave (D)
- Maison du crime -> Jardin (E)
- Cafe -> Commissariat (N)
- Commissariat -> Morgue (E)
- Commissariat -> Labo (O)

---

## 7. Objets et indices

Objets a analyser :
1. couteau (Maison du crime)  
2. cle (Maison de Durand)  
3. lettre (Maison de Lenoir)  
4. coffre (Cave)  
5. photos (Grenier)  
6. arme (Jardin)

Objet bonus :
- livre_ville (Bibliotheque)

Systemes importants :
- `examine` : donne des indices
- `use` : interactions (ex : `use cle on coffre`)
- `analyze` : obligatoire pour gagner

---

## 8. Personnages (PNJ)

Durand :
- Suspect principal
- Se deplace entre Rue, Maison du crime, Commissariat

Lenoir :
- Vieille dame temoin
- Reste chez elle

Policier :
- Au Commissariat
- Permet l’accusation finale

Medecin legiste :
- A la Morgue
- Fournit l’autopsie

Chimiste :
- Au Labo
- Analyse les objets
- Etape obligatoire avant l’accusation

---

## 9. Quetes (resume)

Quete 1 : Inspecter la maison du crime  
Quete 2 : Analyser les objets au Labo  
Quete 3 : Aller a la Morgue    
Quete 4 : Inspecter chez Lenoir  
Quete 5 : Analyser la lettre  
Quete 6 : Inspecter chez Durand  
Quete 7 : Resoudre l’enigme (accuser Durand)

Quetes optionnelles :
- Ouvrir le coffre
- Lire la lettre

Progression generale :
Maison du crime -> Environs -> Lenoir -> Durand -> Labo -> Morgue -> Accusation

---

## 10. Architecture du code

Fichiers principaux :
- `game.py` : moteur du jeu
- `room.py` : salles
- `player.py` : joueur
- `character.py` : PNJ
- `item.py` : objets
- `actions.py` : actions du joueur
- `command.py` : structure des commandes
- `quest.py` : systeme de quetes

Principes utilises :
- Programmation orientee objet
- Dictionnaires pour les inventaires
- Listes pour l’historique et les quetes
- Modularite du code

Resume des classes :
- Game : boucle principale, gestion des commandes, victoire/defaite
- Room : description, sorties, objets, PNJ
- Player : inventaire, position, historique
- Character : dialogues, deplacements
- Item : description des objets
- Quest / QuestManager : gestion des objectifs

---




