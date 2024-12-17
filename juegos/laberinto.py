import pygame
import sys

# Inicializar pygame
pygame.init()

# Configuración de la pantalla
width, height = 800, 450
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Juego de Laberinto con Rutas')

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Definir laberintos (matrices) con diferentes rutas
mazes = {
    "Ruta 1": [
        "###################",
        "# aaaaaaaaaaaaaa#c#",
        "#a###############c#",
        "#a#bbbbb#bcccccccc#",
        "#a#b#b#bbb###c###c#",
        "#a#b#b#b#bbb#c#c#c#",
        "#a#b#########c#c#c#",
        "#a#bbbbbbb#ccccc#c#",
        "#a#######b#######c#",
        "#aaabbbbbbb#cccccF#",
        "###################"
    ],
    "Ruta 2": [
        "###################",
        "# aaaaaaa#aaaaaaaaF",
        "#a#######a#######a#",
        "#a#bbbbb#bbbbbbbbb#",
        "#a#b#b#bbb#b###b###",
        "#a#b#b#b#bb#b#bbb#",
        "#a#b#########b#bbb#",
        "#a#bbbbbbb#bbbbbbb#",
        "#a#######b#######b#",
        "#aaabbbbbbb#bbbbbb#",
        "###################"
    ],
    "Ruta 3": [
        "###################",
        "#aaaaaa#aaaaaaaaaa#",
        "###a###a###a#######",
        "#bbbaaaaaa#bbb#####",
        "###bbbb###ba#bbbbbb",
        "#aaaabbbbb#a###bbbb",
        "#aaa###bbb#a#####bb",
        "#aaaabbbbbaaaaa###b",
        "#################bb",
        "Faaaaaabbbbbbbbbbbb",
        "###################"
    ]
}

# Tamaño de las celdas del laberinto
cell_size = 40

# Posición inicial del jugador
player_x, player_y = 1, 1
player_color = RED

# Conjunto de celdas visitadas
visited_cells = set()

def draw_button(text, rect, color, font, text_color):
    """Dibuja un botón con texto en la pantalla."""
    pygame.draw.rect(screen, color, rect)
    pygame.draw.rect(screen, BLACK, rect, 2)
    label = font.render(text, True, text_color)
    label_rect = label.get_rect(center=rect.center)
    screen.blit(label, label_rect)

def select_maze_window():
    """Muestra una ventana para seleccionar un laberinto."""
    font = pygame.font.SysFont(None, 36)
    buttons = []

    # Crear botones para cada laberinto
    for idx, name in enumerate(mazes.keys()):
        button_rect = pygame.Rect(300, 100 + idx * 100, 200, 50)
        buttons.append((name, button_rect))

    running = True
    while running:
        screen.fill(WHITE)
        title = font.render("Selecciona una ruta:", True, BLACK)
        screen.blit(title, (width // 2 - title.get_width() // 2, 20))

        for name, rect in buttons:
            draw_button(name, rect, GRAY, font, BLACK)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                for name, rect in buttons:
                    if rect.collidepoint(event.pos):
                        return mazes[name]

# Laberinto seleccionado
maze = select_maze_window()

# Marcar la celda inicial como visitada
visited_cells.add((player_x, player_y))

# Funciones principales (mantienen la lógica del juego)
def draw_maze():
    """Dibuja el laberinto en la pantalla."""
    for y, row in enumerate(maze):
        for x, col in enumerate(row):
            if col == 'a':
                color = RED
            elif col == 'b':
                color = BLUE
            elif col == 'c':
                color = YELLOW
            elif col == '#':
                color = BLACK
            elif col == 'F':
                color = YELLOW
            else:
                color = WHITE

            pygame.draw.rect(screen, color, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size))

            if (x, y) == (player_x, player_y):
                pygame.draw.rect(screen, BLACK, pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size), 3)

            if col == 'F':
                font = pygame.font.SysFont(None, 30)
                text = font.render('F', True, BLACK)
                screen.blit(text, (x * cell_size + 12, y * cell_size + 10))

def move_player(target_x, target_y):
    """Mueve al jugador hacia una celda adyacente dentro del laberinto."""
    global player_x, player_y, player_color

    target_cell_x = target_x // cell_size
    target_cell_y = target_y // cell_size

    dx = target_cell_x - player_x
    dy = target_cell_y - player_y

    if abs(dx) + abs(dy) == 1:
        if maze[target_cell_y][target_cell_x] != '#':
            target_cell = maze[target_cell_y][target_cell_x]
            if (target_cell == 'a' and player_color == RED) or \
               (target_cell == 'b' and player_color == BLUE) or \
               (target_cell == 'c' and player_color == YELLOW) or \
               (target_cell == 'F'):
                player_x, player_y = target_cell_x, target_cell_y
                if (player_x, player_y) in visited_cells:
                    print("¡Perdiste! Celda repetida.")
                    pygame.time.delay(1000)
                    pygame.quit()
                    sys.exit()

                visited_cells.add((player_x, player_y))

                if maze[player_y][player_x] == 'F':
                    print("¡Ganaste!")
                    pygame.time.delay(1000)
                    pygame.quit()
                    sys.exit()

def handle_mouse_click(mouse_x, mouse_y):
    move_player(mouse_x, mouse_y)

def handle_anticlick():
    global player_color
    if player_color == RED:
        player_color = BLUE
    elif player_color == BLUE:
        player_color = YELLOW
    else:
        player_color = RED

def main():
    global player_x, player_y, player_color

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    handle_mouse_click(event.pos[0], event.pos[1])
                elif event.button == 3:
                    handle_anticlick()

        screen.fill(WHITE)
        draw_maze()

        pygame.draw.rect(screen, player_color, pygame.Rect(player_x * cell_size, player_y * cell_size, cell_size, cell_size))
        pygame.draw.rect(screen, BLACK, pygame.Rect(player_x * cell_size, player_y * cell_size, cell_size, cell_size), 3)

        pygame.display.flip()
        pygame.time.Clock().tick(30)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()