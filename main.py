import tkinter as tk
from PIL import Image, ImageTk

class Piece:

    tour = "white"
    def __init__(self, canvas, row, col, color, role, image_path):
        # Initialisation des attributs
        self.canvas = canvas
        self.row = row
        self.col = col
        self.color = color
        self.role = role
        self.image_path = image_path
        self.load_image()
        self.draw()
        self.selected = False
        self.canvas.tag_bind(self.image_id, '<Button-1>', self.on_click)
        self.highlighted_circle_ids = []

    def load_image(self):
        # Charger l'image à partir du chemin spécifié
        self.image = Image.open(self.image_path)
        # Redimensionner l'image pour s'adapter à la taille de la case
        self.image = self.image.resize((50, 50))
        # Convertir l'image en un format compatible avec tkinter
        self.img_tk = ImageTk.PhotoImage(self.image)

    def draw(self):
        # Dessiner l'image sur le canvas
        self.image_id = self.canvas.create_image(self.col * 50 + 25, self.row * 50 + 25, image=self.img_tk)

    def on_click(self, event):
        if self.color == Piece.tour : 
            if self.selected:
                self.remove_highlighted_circles()
                self.selected = False
            else:
                retire_button()
                self.selected = True
                self.highlight_possible_moves()

    def highlight_possible_moves(self):
        # Récupere les coups légaux 
        possible_moves = self.get_possible_moves()

        # Retire les coups qui s'auto-mets en echec 
        coups_valides = []
        for move in possible_moves : 
            if not self.move_to_test(move[1], move[0]) :
                coups_valides.append(move)

        # Dessiner des cercles gris transparents sur les cases possibles pour le déplacement de la pièce
        for move in coups_valides:
            x = move[0] * 50 + 25
            y = move[1] * 50 + 25
            circle_id = self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="gray60", outline="gray60")
            self.highlighted_circle_ids.append(circle_id)
            # Associez un événement de clic à chaque cercle gris
            self.canvas.tag_bind(circle_id, '<Button-1>', lambda event, row=move[1], col=move[0]: self.move_to(row, col))

    def move_to(self, row, col):
        # Copiez les coordonnées actuelles de la pièce
        if verif_piece(col, row) : 
            del_piece(col, row)
        # Déplacez temporairement la pièce à une nouvelle position
        self.row = row
        self.col = col
        
        self.canvas.coords(self.image_id, col * 50 + 25, row * 50 + 25)

        # Supprimez les cercles de mise en évidence et réinitialisez l'état de sélection
        self.remove_highlighted_circles()
        self.selected = False

        # Vérifiez si le roi adverse est en échec après le mouvement
        if self.color == 'white':
            opponent_king = find_opponent_king('black')
        else:
            opponent_king = find_opponent_king('white')

        if is_check(opponent_king):
            if is_checkmate(opponent_king): 
                show_game_over(self.color)

        if Piece.tour == "white":    
            Piece.tour = "black"
        else: 
            Piece.tour = "white"

    def move_to_test(self, row, col) : 
        # Save la position initial : 
        row_init = self.row
        col_init = self.col

        # Effectue le mouvement
        self.row = row
        self.col = col
        
        # Verifie si il y a echec
        if is_check(find_opponent_king(self.color)) : 
            echec_after_move = True
        else : 
            echec_after_move = False
        
        self.row = row_init
        self.col = col_init

        return echec_after_move

    def remove_highlighted_circles(self):
        # Supprimer tous les cercles gris
        for circle_id in self.highlighted_circle_ids:
            self.canvas.delete(circle_id)
        self.highlighted_circle_ids.clear()

    def get_possible_moves(self):
        liste = []
        if self.color == "white" : 
            color_opose = "black"
        else : 
            color_opose = "white"
        
        #liste des coups possibles pour le pion blanc 
        if self.color == "white" and self.role == "pawn" : 
            if not verif_piece(self.col, self.row-1) :
                liste.append((self.col, self.row-1))
            if self.row == 6 and not verif_piece(self.col, self.row-2):
                liste.append((self.col, self.row-2))
            if verif_piece(self.col-1, self.row-1) and verif_color(self.col-1, self.row-1) == "black":
                liste.append((self.col-1, self.row-1))
            if verif_piece(self.col+1, self.row-1) and verif_color(self.col+1, self.row-1) == "black": 
                liste.append((self.col+1, self.row-1))
        #liste des coups possibles pour le pion noir
        elif self.color == "black" and self.role == "pawn" : 
            if not verif_piece(self.col, self.row+1):
                liste.append((self.col, self.row+1))
            if self.row == 1 and not verif_piece(self.col, self.row+2) :
                liste.append((self.col, self.row+2))
            if verif_piece(self.col-1, self.row+1) and verif_color(self.col-1, self.row+1) == "white" :
                liste.append((self.col-1, self.row+1))
            if verif_piece(self.col+1, self.row+1) and verif_color(self.col+1, self.row+1) == "white" : 
                liste.append((self.col+1, self.row+1))
        #liste des coups possibles pour le fou
        elif self.role == "bishop" : 
            #deplacement vers haut gache
            x, y = self.col-1, self.row-1
            continuer = True
            while x >= 0 and y>= 0 and continuer :
                if verif_piece(x, y) and verif_color(x, y) == color_opose : 
                    liste.append((x, y))
                    continuer = False
                elif verif_piece(x, y) and verif_color(x, y) == self.color: 
                    continuer = False
                else : 
                    liste.append((x, y))
                    x -= 1
                    y -= 1
            #deplacement vers bas gauche
            x, y = self.col-1, self.row+1
            continuer = True
            while x >= 0 and y<= 7 and continuer :
                if verif_piece(x, y) and verif_color(x, y) == color_opose : 
                    liste.append((x, y))
                    continuer = False
                elif verif_piece(x, y) and verif_color(x, y) == self.color: 
                    continuer = False
                else : 
                    liste.append((x, y))
                    x -= 1
                    y += 1
            #deplacement vers bas gauche
            x, y = self.col+1, self.row-1
            continuer = True
            while x <= 7 and y>= 0 and continuer :
                if verif_piece(x, y) and verif_color(x, y) == color_opose : 
                    liste.append((x, y))
                    continuer = False
                elif verif_piece(x, y) and verif_color(x, y) == self.color: 
                    continuer = False
                else : 
                    liste.append((x, y))
                    x += 1
                    y -= 1
            #deplacement vers bas droite
            x, y = self.col+1, self.row+1
            continuer = True
            while x <= 7 and y<= 7 and continuer :
                if verif_piece(x, y) and verif_color(x, y) == color_opose : 
                    liste.append((x, y))
                    continuer = False
                elif verif_piece(x, y)and verif_color(x, y) == self.color : 
                    continuer = False
                else : 
                    liste.append((x, y))
                    x += 1
                    y += 1
        #liste des coups possibles pour la tour
        elif self.role == 'rook' : 
            x, y = self.col, self.row
            continuer = True
            #deplacement vers le haut
            y -= 1
            while y >= 0 and continuer : 
                if verif_piece(x, y) and verif_color(x, y) == color_opose : 
                    liste.append((x, y))
                    continuer = False
                elif verif_piece(x, y) and verif_color(x, y) == self.color: 
                    continuer = False
                else : 
                    liste.append((x, y))
                    y -= 1
            x, y = self.col, self.row
            continuer = True
            #deplacement vers le bas
            y += 1
            while y <= 7 and continuer : 
                if verif_piece(x, y) and verif_color(x, y) == color_opose : 
                    liste.append((x, y))
                    continuer = False
                elif verif_piece(x, y) and verif_color(x, y) == self.color: 
                    continuer = False
                else : 
                    liste.append((x, y))
                    y += 1
            x, y = self.col, self.row
            continuer = True
            #deplacement vers la gauche
            x -= 1
            while x >= 0 and continuer : 
                if verif_piece(x, y) and verif_color(x, y) == color_opose : 
                    liste.append((x, y))
                    continuer = False
                elif verif_piece(x, y)and verif_color(x, y) == self.color : 
                    continuer = False
                else : 
                    liste.append((x, y))
                    x -= 1
            x, y = self.col, self.row
            continuer = True
            #deplacement vers la droite
            x += 1
            while x <= 7 and continuer : 
                if verif_piece(x, y) and verif_color(x, y) == color_opose : 
                    liste.append((x, y))
                    continuer = False
                elif verif_piece(x, y) and verif_color(x, y) == self.color: 
                    continuer = False
                else : 
                    liste.append((x, y))
                    x += 1
        #liste des coups possibles pour le cavalier
        elif self.role == "knight" : 
            if verif_piece(self.col-1, self.row-2) and verif_color(self.col-1, self.row-2) != self.color or not verif_piece(self.col-1, self.row-2) : 
                liste.append((self.col-1, self.row-2))
            if verif_piece(self.col+1, self.row-2) and verif_color(self.col+1, self.row-2) != self.color or not verif_piece(self.col+1, self.row-2) : 
                liste.append((self.col+1, self.row-2))
            if verif_piece(self.col-2, self.row-1) and verif_color(self.col-2, self.row-1) != self.color or not verif_piece(self.col-2, self.row-1) : 
                liste.append((self.col-2, self.row-1))
            if verif_piece(self.col+2, self.row-1) and verif_color(self.col+2, self.row-1) != self.color or not verif_piece(self.col+2, self.row-1) : 
                liste.append((self.col+2, self.row-1))
            if verif_piece(self.col-1, self.row+2) and verif_color(self.col-1, self.row+2) != self.color or not verif_piece(self.col-1, self.row+2) : 
                liste.append((self.col-1, self.row+2))
            if verif_piece(self.col+1, self.row+2) and verif_color(self.col+1, self.row+2) != self.color or not verif_piece(self.col+1, self.row+2) : 
                liste.append((self.col+1, self.row+2))
            if verif_piece(self.col-2, self.row+1) and verif_color(self.col-2, self.row+1) != self.color or not verif_piece(self.col-2, self.row+1) : 
                liste.append((self.col-2, self.row+1))
            if verif_piece(self.col+2, self.row+1) and verif_color(self.col+2, self.row+1) != self.color or not verif_piece(self.col+2, self.row+1) : 
                liste.append((self.col+2, self.row+1))
        #liste des coups possibles pour la reine
        elif self.role == "queen" : 
            x, y = self.col, self.row
            continuer = True
            #deplacement vers le haut
            y -= 1
            while y >= 0 and continuer : 
                if verif_piece(x, y) and verif_color(x, y) == color_opose : 
                    liste.append((x, y))
                    continuer = False
                elif verif_piece(x, y) and verif_color(x, y) == self.color: 
                    continuer = False
                else : 
                    liste.append((x, y))
                    y -= 1
            x, y = self.col, self.row
            continuer = True
            #deplacement vers le bas
            y += 1
            while y <= 7 and continuer : 
                if verif_piece(x, y) and verif_color(x, y) == color_opose : 
                    liste.append((x, y))
                    continuer = False
                elif verif_piece(x, y)and verif_color(x, y) == self.color : 
                    continuer = False
                else : 
                    liste.append((x, y))
                    y += 1
            x, y = self.col, self.row
            continuer = True
            #deplacement vers la gauche
            x -= 1
            while x >= 0 and continuer : 
                if verif_piece(x, y) and verif_color(x, y) == color_opose : 
                    liste.append((x, y))
                    continuer = False
                elif verif_piece(x, y) and verif_color(x, y) == self.color: 
                    continuer = False
                else : 
                    liste.append((x, y))
                    x -= 1
            x, y = self.col, self.row
            continuer = True
            #deplacement vers la droite
            x += 1
            while x <= 7 and continuer : 
                if verif_piece(x, y) and verif_color(x, y) == color_opose : 
                    liste.append((x, y))
                    continuer = False
                elif verif_piece(x, y)and verif_color(x, y) == self.color : 
                    continuer = False
                else : 
                    liste.append((x, y))
                    x += 1
            #deplacement vers haut gache
            x, y = self.col-1, self.row-1
            continuer = True
            while x >= 0 and y>= 0 and continuer :
                if verif_piece(x, y) and verif_color(x, y) == color_opose : 
                    liste.append((x, y))
                    continuer = False
                elif verif_piece(x, y)and verif_color(x, y) == self.color : 
                    continuer = False
                else : 
                    liste.append((x, y))
                    x -= 1
                    y -= 1
            #deplacement vers bas gauche
            x, y = self.col-1, self.row+1
            continuer = True
            while x >= 0 and y<= 7 and continuer :
                if verif_piece(x, y) and verif_color(x, y) == color_opose : 
                    liste.append((x, y))
                    continuer = False
                elif verif_piece(x, y)and verif_color(x, y) == self.color : 
                    continuer = False
                else : 
                    liste.append((x, y))
                    x -= 1
                    y += 1
            #deplacement vers bas gauche
            x, y = self.col+1, self.row-1
            continuer = True
            while x <= 7 and y>= 0 and continuer :
                if verif_piece(x, y) and verif_color(x, y) == color_opose : 
                    liste.append((x, y))
                    continuer = False
                elif verif_piece(x, y) and verif_color(x, y) == self.color: 
                    continuer = False
                else : 
                    liste.append((x, y))
                    x += 1
                    y -= 1
            #deplacement vers bas droite
            x, y = self.col+1, self.row+1
            continuer = True
            while x <= 7 and y<= 7 and continuer :
                if verif_piece(x, y) and verif_color(x, y) == color_opose : 
                    liste.append((x, y))
                    continuer = False
                elif verif_piece(x, y)and verif_color(x, y) == self.color : 
                    continuer = False
                else : 
                    liste.append((x, y))
                    x += 1
                    y += 1
        #listed des coups possibles pour le roi
        elif self.role == "king" : 
            if verif_piece(self.col -1, self.row) and verif_color(self.col-1, self.row) != self.color or not verif_piece(self.col-1,self.row) : 
                liste.append((self.col-1, self.row))
            if verif_piece(self.col -1, self.row-1) and verif_color(self.col-1, self.row-1) != self.color or not verif_piece(self.col-1,self.row-1) : 
                liste.append((self.col-1, self.row-1))
            if verif_piece(self.col, self.row-1) and verif_color(self.col, self.row-1) != self.color or not verif_piece(self.col,self.row-1) : 
                liste.append((self.col, self.row-1))
            if verif_piece(self.col -1, self.row+1) and verif_color(self.col-1, self.row+1) != self.color or not verif_piece(self.col-1,self.row+1) : 
                liste.append((self.col-1, self.row+1))
            if verif_piece(self.col +1, self.row) and verif_color(self.col+1, self.row) != self.color or not verif_piece(self.col+1,self.row) : 
                liste.append((self.col+1, self.row))
            if verif_piece(self.col +1, self.row-1) and verif_color(self.col+1, self.row-1) != self.color or not verif_piece(self.col+1,self.row-1) : 
                liste.append((self.col+1, self.row-1))
            if verif_piece(self.col, self.row+1) and verif_color(self.col, self.row+1) != self.color or not verif_piece(self.col,self.row+1) : 
                liste.append((self.col, self.row+1))
            if verif_piece(self.col -1, self.row+1) and verif_color(self.col+1, self.row+1) != self.color or not verif_piece(self.col+1,self.row+1) : 
                liste.append((self.col+1, self.row+1))

        return liste           
    
    def at_position(self, x, y) :
        return self.col == x and self.row == y
    
    def suppr(self)  :
        #supprime la piece
        self.canvas.delete(self.image_id)
        self.color = "mort"

# Initialisez les pièces et créez l'échiquier comme précédemment
all_piece = []

def retire_button() : 
    for piece in all_piece : 
        piece.remove_highlighted_circles()

def initialize_pieces(canvas):
    initial_positions = {
        'black rook': [(0, 0), (0, 7)],
        'black knight': [(0, 1), (0, 6)],
        'black bishop': [(0, 2), (0, 5)],
        'black queen': [(0, 3)],
        'black king': [(0, 4)],
        'black pawn': [(1, i) for i in range(8)],
        'white rook': [(7, 0), (7, 7)],
        'white knight': [(7, 1), (7, 6)],
        'white bishop': [(7, 2), (7, 5)],
        'white queen': [(7, 3)],
        'white king': [(7, 4)],
        'white pawn': [(6, i) for i in range(8)],
    }

    for piece_type, positions in initial_positions.items():
        for row, col in positions:
            if 'black' in piece_type:
                color = 'black'
            else:
                color = 'white'
            role = piece_type.split(' ')[1]
            piece = Piece(canvas, row, col, color, role, f"./images/{piece_type}.png")
            all_piece.append(piece)

def verif_piece(x, y) :
    for piece in all_piece :
        if piece.at_position(x, y) :
            return True
    return False

def verif_color(x, y) : 
    for piece in all_piece : 
        if piece.at_position(x, y) :
            return piece.color

def del_piece(x, y) : 
    for piece in all_piece : 
        if piece.at_position(x, y) :
            piece.suppr()
            all_piece.remove(piece)

def find_opponent_king(color):
    for piece in all_piece:
        if piece.color == color and piece.role == 'king':
            return piece
    return None

def is_check(king):
    for piece in all_piece:
        if piece.color != king.color:  # Vérifiez les pièces du joueur adverse
            possible_moves = piece.get_possible_moves()
            if (king.col, king.row) in possible_moves:
                return True
    return False

def is_checkmate(king):
    for piece in all_piece : 
        if piece.color == king.color : 
            possible_moves = piece.get_possible_moves()
            x = piece.col
            y = piece.row
            for move in possible_moves : 
                if move[0] >=  0 and move[0] < 8 and move[1] >= 0 and move[1] < 8 : 
                    piece.move_to(move[1], move[0])
                    if not is_check(king) : 
                        piece.move_to(y, x)
                        return False
                    piece.move_to(y, x)
    return True

def show_game_over(gagnant):
    def finito() : 
        root.after(100, root.destroy)
    if gagnant == "white" : 
        gagnant ="blanc"
    else : 
        gagnant = "noirs"
    # Créez une nouvelle fenêtre pour afficher le message Game Over
    game_over_window = tk.Toplevel(root)
    game_over_window.title("Game Over")

    def restart_game():
        # Supprimez toutes les pièces actuelles de l'échiquier
        game_over_window.destroy()
        Piece.tour = "white"
        for piece in all_piece:
            piece.suppr()

        # Réinitialisez les pièces sur l'échiquier
        initialize_pieces(frame)

    # Créez un canevas pour afficher le message Game Over
    canvas = tk.Canvas(game_over_window, width=300, height=200)
    canvas.pack()
    canvas.create_text(150, 100, text=f"Les {gagnant} ont gangné", font=("Helvetica", 20), fill="black")
    # Créez des boutons pour relancer et fermer la fenêtre
    restart_button = tk.Button(game_over_window, text="Relancer", command=restart_game)
    restart_button.pack(side="left", padx=10, pady=10)

    close_button = tk.Button(game_over_window, text="Fermer", command=finito)
    close_button.pack(side="right", padx=10, pady=10)


# Créer la fenêtre principale
root = tk.Tk()
root.title("Chess")

frame = tk.Canvas(root, width=400, height=400)
frame.pack()

# Créer le cadrillage
for i in range(8):
    for j in range(8):
        color = "green" if (i + j) % 2 == 0 else "white"
        frame.create_rectangle(j * 50, i * 50, (j + 1) * 50, (i + 1) * 50, fill=color)

# Initialiser toutes les pièces sur l'échiquier
initialize_pieces(frame)

# Temps

temps_blanc = 600
temps_noir = 600

# Créer les étiquettes pour afficher le temps
label_temps_blanc = tk.Label(root, text="Temps Blanc: 10:00")
label_temps_blanc.pack()

label_temps_noir = tk.Label(root, text="Temps Noir: 10:00")
label_temps_noir.pack()

# Fonction pour mettre à jour le temps restant
def mettre_a_jour_temps():
    global temps_blanc, temps_noir  # Déclarer les variables comme globales

    # Vérifier la couleur du joueur actuel
    if Piece.tour == "white":
        temps_restant_blanc = temps_blanc // 60, temps_blanc % 60
        label_temps_blanc.config(text=f"Temps Blanc: {temps_restant_blanc[0]:02d}:{temps_restant_blanc[1]:02d}")
        temps_blanc -= 1  # Décrémenter le temps restant pour le joueur blanc
    else:
        temps_restant_noir = temps_noir // 60, temps_noir % 60
        label_temps_noir.config(text=f"Temps Noir: {temps_restant_noir[0]:02d}:{temps_restant_noir[1]:02d}")
        temps_noir -= 1  # Décrémenter le temps restant pour le joueur noir

    # Mettre à jour les temps toutes les secondes
    root.after(1000, mettre_a_jour_temps)


# Appeler la fonction pour démarrer la mise à jour des temps
mettre_a_jour_temps()

root.mainloop()
