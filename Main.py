import pygame
import numpy as np
import random

# Define constants
WIDTH, HEIGHT = 900, 540
TILE_SIZE = 55
MARGIN = 10
GRID_SIZE = 7
BACKGROUND_COLOR = (187, 173, 160)
TEXT_COLOR = (119, 110, 101)
BLUE_COLOR = (0, 0, 255)
LINE_COLOR = (0, 0, 0)  # Black color for the separating line
SELECTED_COLOR = (119, 110, 101)  # color for selected text
RADIUS = 15 # Border radius for buttons

TILE_COLORS = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (245, 158, 122),
    64: (245, 121, 72),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
    4096: (237, 191, 23),
}

# Initialize pygame
pygame.init()
move_sound = pygame.mixer.Sound('./move.mp3')
move_sound.set_volume(0.5)
# background_music =  pygame.mixer.Sound("C:\\Users\\noman traders\\OneDrive\Documents\\codes\\background music.mp3")
pygame.mixer.music.load("./background music.mp3")

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("4096 Game: AI vs Player (7x7)")

class Game2048:
    def __init__(self, is_ai=False, max_tile=4096, ai_depth=3):
        self.board = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
        self.max_tile = max_tile
        self.ai_depth = ai_depth
        self.add_random_tile()
        self.add_random_tile()
        self.is_ai = is_ai
        self.move_count = 0

    def add_random_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.board[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.board[i][j] = 2 if random.random() < 0.9 else 4

    def move(self, direction):
        def merge_line(line):
            non_zero = [num for num in line if num != 0]
            merged = []
            skip = False
            for i in range(len(non_zero)):
                if skip:
                    skip = False
                    continue
                if i < len(non_zero) - 1 and non_zero[i] == non_zero[i + 1]:
                    merged.append(non_zero[i] * 2)
                    skip = True
                else:
                    merged.append(non_zero[i])
            return merged + [0] * (len(line) - len(merged))

        moved = False
        new_board = self.board.copy()

        if direction == "up":
            for col in range(GRID_SIZE):
                line = [self.board[row][col] for row in range(GRID_SIZE)]
                merged = merge_line(line)
                for row in range(GRID_SIZE):
                    new_board[row][col] = merged[row]
        elif direction == "down":
            for col in range(GRID_SIZE):
                line = [self.board[row][col] for row in range(GRID_SIZE)][::-1]
                merged = merge_line(line)
                for row in range(GRID_SIZE):
                    new_board[row][col] = merged[::-1][row]
        elif direction == "left":
            for row in range(GRID_SIZE):
                merged = merge_line(self.board[row])
                new_board[row] = merged
        elif direction == "right":
            for row in range(GRID_SIZE):
                merged = merge_line(self.board[row][::-1])
                new_board[row] = merged[::-1]

        if not np.array_equal(self.board, new_board):
            moved = True
            self.move_count += 1
            self.board = new_board
            self.add_random_tile()

        return moved

    def is_game_over(self):
        if any(0 in row for row in self.board):  # Empty spaces
            return False
        for direction in ["up", "down", "left", "right"]:
            temp_game = Game2048()
            temp_game.board = self.board.copy()
            if temp_game.move(direction):
                return False
        return True

    def has_won(self):
        return np.any(self.board == self.max_tile)

    def get_score(self):
        return np.max(self.board)

    # Utility function to evaluate board state
    def evaluate(self):
        # Weighted score calculation
        empty_cells = len([(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.board[i][j] == 0])
        max_tile = np.max(self.board)
        smoothness = -sum(abs(self.board[i][j] - self.board[i + 1][j]) for i in range(GRID_SIZE - 1) for j in range(GRID_SIZE))
        smoothness -= sum(abs(self.board[i][j] - self.board[i][j + 1]) for i in range(GRID_SIZE) for j in range(GRID_SIZE - 1))
        return 10 * max_tile + 2 * empty_cells + smoothness


    # Minimax algorithm to find the best move
    def minimax(self, depth, maximizing_player, alpha, beta):
        if depth == 0 or self.is_game_over():
            return self.evaluate()

        moves = ["up", "down", "left", "right"]
        if maximizing_player:
            max_eval = -float('inf')
            for move in moves:
                temp_game = Game2048()
                temp_game.board = self.board.copy()
                if temp_game.move(move):
                    eval_value = temp_game.minimax(depth - 1, False, alpha, beta)
                    max_eval = max(max_eval, eval_value)
                    alpha = max(alpha, eval_value)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf')
            for move in moves:
                temp_game = Game2048()
                temp_game.board = self.board.copy()
                if temp_game.move(move):
                    eval_value = temp_game.minimax(depth - 1, True, alpha, beta)
                    min_eval = min(min_eval, eval_value)
                    beta = min(beta, eval_value)
                    if beta <= alpha:
                        break
            return min_eval

    # Get the best move for AI
    def get_best_move(self):
        moves = ["up", "down", "left", "right"]
        best_move = None
        max_eval = -float('inf')
        for move in moves:
            temp_game = Game2048()
            temp_game.board = self.board.copy()
            if temp_game.move(move):
                eval_value = temp_game.minimax(self.ai_depth, False, -float('inf'), float('inf'))
                if eval_value > max_eval:
                    max_eval = eval_value
                    best_move = move
        return best_move
    
def display_message(message):
    font = pygame.font.Font(None, 48)
    text = font.render(message, True, BLUE_COLOR)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text, text_rect)

def game_result(ai_game, player_game):
    ai_score = ai_game.get_score()
    player_score = player_game.get_score()
    ai_moves = ai_game.move_count
    player_moves = player_game.move_count

    if player_game.has_won():
        return f"Player wins with {player_moves} moves!\nPlayer Score: {player_score}"
    elif ai_game.has_won():
        return f"AI wins with {ai_moves} moves!\nAI Score: {ai_score}"
    elif ai_score > player_score:
        return f"AI wins with {ai_moves} moves!\nAI Score: {ai_score}, Player Score: {player_score}"
    elif player_score > ai_score:
        return f"Player wins with {player_moves} moves!\nAI Score: {ai_score}, Player Score: {player_score}"
    else:
        return f"It's a tie!\nAI Moves: {ai_moves}, Player Moves: {player_moves}, Score: {player_score}"

def display_board(game, offset_x):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            tile_value = game.board[i][j]
            pygame.draw.rect(
                screen,
                TILE_COLORS[tile_value],
                pygame.Rect(offset_x + j * (TILE_SIZE + MARGIN), i * (TILE_SIZE + MARGIN), TILE_SIZE, TILE_SIZE),
            )
            if tile_value != 0:
                font = pygame.font.Font(None, 36)
                text = font.render(str(tile_value), True, TEXT_COLOR)
                text_rect = text.get_rect(
                    center=(offset_x + j * (TILE_SIZE + MARGIN) + TILE_SIZE // 2, i * (TILE_SIZE + MARGIN) + TILE_SIZE // 2)
                )
                screen.blit(text, text_rect)

# Menu Screen
def display_menu(selected_mode=None, selected_ai_difficulty=None):
    # Load the background image
    background_image = pygame.image.load("backpic.jpg")  
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT)) 
    # Render the background image
    screen.blit(background_image, (0, 0))
    
    font = pygame.font.Font(None, 48)
    title_text = font.render("4096 Game: AI vs Player", True, (230, 220, 200))
    
    # Button Texts
    play_1024_text = font.render("Play 1024", True, (255, 255, 255) if selected_mode != 1024 else SELECTED_COLOR)
    play_2048_text = font.render("Play 2048", True, (255, 255, 255) if selected_mode != 2048 else SELECTED_COLOR)
    play_4096_text = font.render("Play 4096", True, (255, 255, 255) if selected_mode != 4096 else SELECTED_COLOR)
    difficulty_text = font.render("Select AI Difficulty:", True,  (245, 245, 220))
    easy_text = font.render("Easy", True, (255, 255, 255) if selected_ai_difficulty != 'Easy' else SELECTED_COLOR)
    medium_text = font.render("Medium", True, (255, 255, 255) if selected_ai_difficulty != 'Medium' else SELECTED_COLOR)
    hard_text = font.render("Hard", True,(255, 255, 255) if selected_ai_difficulty != 'Hard' else SELECTED_COLOR)

    # screen.fill(BACKGROUND_COLOR)

    # Title
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 10))
    screen.blit(title_text, title_rect)

    # Button dimensions
    button_width = 260
    button_height = 50
    button_spacing = 15  # Reduced spacing for better fit
    start_y = HEIGHT // 6  # Start higher up for better layout

    # Play Buttons
    play_1024_rect = pygame.Rect(WIDTH // 2 - button_width // 2, start_y, button_width, button_height)
    play_2048_rect = pygame.Rect(WIDTH // 2 - button_width // 2, start_y + (button_height + button_spacing), button_width, button_height)
    play_4096_rect = pygame.Rect(WIDTH // 2 - button_width // 2, start_y + 2 * (button_height + button_spacing), button_width, button_height)

    pygame.draw.rect(screen,  (50, 50, 50), play_1024_rect, border_radius=RADIUS)
    pygame.draw.rect(screen, (50, 50, 50), play_2048_rect, border_radius=RADIUS)
    pygame.draw.rect(screen,  (50, 50, 50), play_4096_rect, border_radius=RADIUS)

    play_1024_text_rect = play_1024_text.get_rect(center=play_1024_rect.center)
    play_2048_text_rect = play_2048_text.get_rect(center=play_2048_rect.center)
    play_4096_text_rect = play_4096_text.get_rect(center=play_4096_rect.center)

    screen.blit(play_1024_text, play_1024_text_rect)
    screen.blit(play_2048_text, play_2048_text_rect)
    screen.blit(play_4096_text, play_4096_text_rect)

    # AI Difficulty Label
    difficulty_label_y = start_y + 3 * (button_height + button_spacing) + button_spacing
    difficulty_text_rect = difficulty_text.get_rect(center=(WIDTH // 2, difficulty_label_y))
    screen.blit(difficulty_text, difficulty_text_rect)

    # AI Difficulty Buttons
    easy_rect = pygame.Rect(WIDTH // 2 - button_width // 2, difficulty_label_y + button_spacing+20, button_width, button_height)
    medium_rect = pygame.Rect(WIDTH // 2 - button_width // 2, difficulty_label_y + button_spacing +20+ (button_height + button_spacing), button_width, button_height)
    hard_rect = pygame.Rect(WIDTH // 2 - button_width // 2, difficulty_label_y + button_spacing + 2 * (button_height + button_spacing)+20, button_width, button_height)

    pygame.draw.rect(screen,  (50, 50, 50), easy_rect, border_radius=RADIUS)
    pygame.draw.rect(screen,  (50, 50, 50), medium_rect, border_radius=RADIUS)
    pygame.draw.rect(screen,  (50, 50, 50), hard_rect, border_radius=RADIUS)

    easy_text_rect = easy_text.get_rect(center=easy_rect.center)
    medium_text_rect = medium_text.get_rect(center=medium_rect.center)
    hard_text_rect = hard_text.get_rect(center=hard_rect.center)

    screen.blit(easy_text, easy_text_rect)
    screen.blit(medium_text, medium_text_rect)
    screen.blit(hard_text, hard_text_rect)

    pygame.display.flip()
    return play_1024_rect, play_2048_rect, play_4096_rect, easy_rect, medium_rect, hard_rect

def start_game(mode, ai_difficulty):
    ai_depth = 3 if ai_difficulty == 'Hard' else (2 if ai_difficulty == 'Medium' else 1)
    ai_game = Game2048(is_ai=True, max_tile=mode, ai_depth=ai_depth)
    player_game = Game2048(is_ai=False, max_tile=mode)

    clock = pygame.time.Clock()
    ai_move_delay = 500 if ai_difficulty == 'Easy' else (300 if ai_difficulty == 'Medium' else 0)
    last_ai_move_time = pygame.time.get_ticks()  # Record the current time

    player_start_time = pygame.time.get_ticks()
    ai_start_time = pygame.time.get_ticks()

    player_reached_max = False
    ai_reached_max = False
    winner_message_displayed = False

    player_elapsed_time = 0
    ai_elapsed_time = 0

    def display_message(message, delay=3000):
        """Display a message on the screen for a given duration."""
        font = pygame.font.Font(None, 48)
        text = font.render(message, True, TEXT_COLOR)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
        pygame.time.wait(delay)

    # Main game loop
    while True:
        current_time = pygame.time.get_ticks()

        # Calculate elapsed time for Player and AI
        if not player_reached_max and not player_game.is_game_over():
            player_elapsed_time = (current_time - player_start_time) // 1000
        if not ai_reached_max and not ai_game.is_game_over():
            ai_elapsed_time = (current_time - ai_start_time) // 1000

        screen.fill(BACKGROUND_COLOR)
        display_board(ai_game, 0)
        display_board(player_game, WIDTH // 2)

        # Draw the black line separating the grids
        pygame.draw.line(screen, LINE_COLOR, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)

        # Display Timers and Move Counters
        font = pygame.font.Font(None, 36)
        ai_timer_text = font.render(f"AI Time: {ai_elapsed_time // 60}:{ai_elapsed_time % 60:02}", True, (62, 39, 35))
        player_timer_text = font.render(f"Player Time: {player_elapsed_time // 60}:{player_elapsed_time % 60:02}", True, (62, 39, 35))

        ai_moves_text = font.render(f"AI Moves: {ai_game.move_count}", True, (62, 39, 35))
        player_moves_text = font.render(f"Player Moves: {player_game.move_count}", True, (62, 39, 35))

        screen.blit(ai_timer_text, (WIDTH // 4 - ai_timer_text.get_width() // 2, HEIGHT - 80))
        screen.blit(ai_moves_text, (WIDTH // 4 - ai_moves_text.get_width() // 2, HEIGHT - 40))
        screen.blit(player_timer_text, (3 * WIDTH // 4 - player_timer_text.get_width() // 2, HEIGHT - 80))
        screen.blit(player_moves_text, (3 * WIDTH // 4 - player_moves_text.get_width() // 2, HEIGHT - 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and not player_game.is_game_over() and not player_reached_max:
                move_sound.play()
                if event.key == pygame.K_UP:
                    player_game.move("up")
                elif event.key == pygame.K_DOWN:
                    player_game.move("down")
                elif event.key == pygame.K_LEFT:
                    player_game.move("left")
                elif event.key == pygame.K_RIGHT:
                    player_game.move("right")

        # AI Turn with non-blocking delay
        if current_time - last_ai_move_time >= ai_move_delay and not ai_game.is_game_over() and not ai_reached_max:
            ai_move = ai_game.get_best_move()
            ai_game.move(ai_move)
            last_ai_move_time = current_time

        pygame.display.flip()
        clock.tick(60)

        # Display Max Tile Messages
        if player_game.has_won() and not player_reached_max:
            player_reached_max = True
            display_message("Player has reached the max tile!", delay=3000)

        if ai_game.has_won() and not ai_reached_max:
            ai_reached_max = True
            display_message("AI has reached the max tile!", delay=3000)

        # End game when both have finished
        if player_game.is_game_over() and not player_reached_max:
            player_reached_max = True
        if ai_game.is_game_over() and not ai_reached_max:
            ai_reached_max = True

        if player_reached_max and ai_reached_max:
            if not winner_message_displayed:
                winner_message = calculate_winner(ai_game, player_game, player_elapsed_time, ai_elapsed_time)
                font = pygame.font.Font(pygame.font.match_font('arial', bold=True), 33)

                # Render the winner message
                text = font.render(winner_message, True, BLUE_COLOR)
                text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Center it on the screen

                # Ensure the text doesn't go out of the left or right edge
                if text_rect.left < 0:
                    text_rect.left = 0
                if text_rect.right > WIDTH:
                    text_rect.right = WIDTH

                # Prevent overflow at the bottom if necessary
                if text_rect.bottom > HEIGHT - 50:
                    text_rect.bottom = HEIGHT - 50
                screen.blit(text, text_rect)

                pygame.display.flip()
                pygame.time.wait(5000)  # Display result for 5 seconds
                winner_message_displayed = True
            return
def calculate_winner(ai_game, player_game, elapsed_time, total_time):

    def calculate_weightage(moves, time_taken, max_time):
        move_weight = 0.7 * moves
        time_weight = 0.3 * time_taken 
        return move_weight + time_weight

    ai_time_taken = total_time - elapsed_time
    player_time_taken = total_time - elapsed_time

    ai_weightage = calculate_weightage(ai_game.move_count, ai_time_taken, total_time)
    player_weightage = calculate_weightage(player_game.move_count, player_time_taken, total_time)

    if ai_weightage < player_weightage:
        return f"AI wins! Weightage: {ai_weightage:.2f} (AI) vs {player_weightage:.2f} (Player)"
    elif player_weightage < ai_weightage:
        return f"Player wins! Weightage: {player_weightage:.2f} (Player) vs {ai_weightage:.2f} (AI)"
    else:
        return "It's a tie!"

if __name__ == "__main__":
    pygame.mixer.music.play(-1)
    # Load and display the image for 5 seconds
    intro_image = pygame.image.load("4096icon.png")  # Replace with your image path
    intro_image = pygame.transform.scale(intro_image, (WIDTH, HEIGHT))  # Scale the image to fit the screen
    screen.blit(intro_image, (0, 0))
    pygame.display.flip()  # Update the screen
    pygame.time.wait(5000)  # Wait for 5 seconds

    selected_mode = None
    selected_ai_difficulty = None

    while True:
        play_1024_rect, play_2048_rect, play_4096_rect, easy_rect, medium_rect, hard_rect = display_menu(selected_mode, selected_ai_difficulty)

        # Event handling for menu
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get mouse position
                x, y = pygame.mouse.get_pos()

                # Check if any menu item is clicked
                if play_1024_rect.collidepoint(x, y):  # Check if the click is within the "Play 1024" button
                    selected_mode = 1024
                elif play_2048_rect.collidepoint(x, y):  # Check if the click is within the "Play 2048" button
                    selected_mode = 2048
                elif play_4096_rect.collidepoint(x, y):  # Check if the click is within the "Play 4096" button
                    selected_mode = 4096
                elif easy_rect.collidepoint(x, y):  # Check if the click is within the "Easy" difficulty button
                    selected_ai_difficulty = 'Easy'
                elif medium_rect.collidepoint(x, y):  # Check if the click is within the "Medium" difficulty button
                    selected_ai_difficulty = 'Medium'
                elif hard_rect.collidepoint(x, y):  # Check if the click is within the "Hard" difficulty button
                    selected_ai_difficulty = 'Hard'

        if selected_mode and selected_ai_difficulty:
            start_game(selected_mode, selected_ai_difficulty)
            break