import sys
import pygame
import chess

# Configuración de pantalla y colores
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 800
WHITE, BLACK = (255, 255, 255), (0, 0, 0)

def load_images():
    pieces = {}
    for piece in chess.PIECE_TYPES:
        for color in chess.COLORS:
            name = chess.Piece(piece, color).symbol()
            image = pygame.image.load(f"{name}.png")
            pieces[name] = pygame.transform.scale(image, (SCREEN_WIDTH // 8, SCREEN_HEIGHT // 8))
    return pieces

def coord_to_square(coord):
    x, y = coord
    return (7 - y) * 8 + x

def square_to_coord(square):
    return square % 8, 7 - (square // 8)

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Ajedrez con Python")
    
    clock = pygame.time.Clock()
    images = load_images()

    board = chess.Board()

    selected_piece = None
    valid_moves = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                square = coord_to_square((x // 100, y // 100))
                piece = board.piece_at(square)

                if selected_piece is not None and square in valid_moves:
                    move = chess.Move(selected_piece, square)
                    board.push(move)
                    selected_piece = None
                    valid_moves = []
                elif piece and piece.color == board.turn:
                    selected_piece = square
                    valid_moves = [move.to_square for move in board.legal_moves if move.from_square == square]

        screen.fill(WHITE)

        # Dibuja el tablero y las piezas
        for i in range(64):
            x, y = i % 8, i // 8
            if (x + y) % 2 == 0:
                pygame.draw.rect(screen, WHITE, pygame.Rect(x * 100, y * 100, 100, 100))
            else:
                pygame.draw.rect(screen, BLACK, pygame.Rect(x * 100, y * 100, 100, 100))

            if selected_piece is not None and i in valid_moves:
                pygame.draw.circle(screen, (0, 255, 0), (x * 100 + 50, y * 100 + 50), 10)

            piece = board.piece_at(i)
            if piece:
                screen.blit(images[piece.symbol()], (x * 100, y * 100))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
