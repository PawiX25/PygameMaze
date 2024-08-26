import pygame
import random
import time

pygame.init()

# Screen dimensions and settings
WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Difficulty settings
DIFFICULTY_SETTINGS = {
    'easy': {
        'maze_width': 20,
        'maze_height': 15,
        'timer_duration': 120,
        'min_distance': 5
    },
    'medium': {
        'maze_width': 30,
        'maze_height': 22,
        'timer_duration': 90,
        'min_distance': 10
    },
    'hard': {
        'maze_width': 40,
        'maze_height': 30,
        'timer_duration': 60,
        'min_distance': 15
    }
}

# Directions for maze generation
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def generate_maze(width, height):
    maze = [[1] * width for _ in range(height)]
    stack = [(0, 0)]
    maze[0][0] = 0
    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in DIRS:
            nx, ny = x + 2 * dx, y + 2 * dy
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                neighbors.append((dx, dy))
        if neighbors:
            dx, dy = random.choice(neighbors)
            maze[y + dy][x + dx] = 0
            maze[y + 2 * dy][x + 2 * dx] = 0
            stack.append((x + 2 * dx, y + 2 * dy))
        else:
            stack.pop()
    return maze

def generate_goal(maze, min_distance=10):
    while True:
        goal_x = random.randint(0, len(maze[0]) - 1)
        goal_y = random.randint(0, len(maze) - 1)
        if maze[goal_y][goal_x] == 0 and (goal_x, goal_y) != (0, 0):
            distance = abs(goal_x - 0) + abs(goal_y - 0)
            if distance >= min_distance:
                return goal_x, goal_y

def draw_maze(screen, maze, player_pos, goal_pos, remaining_time, font):
    global goal_blink_state, goal_blink_start

    screen.fill(WHITE)

    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            color = BLACK if cell == 1 else WHITE
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    if time.time() - goal_blink_start >= goal_blink_time:
        goal_blink_state = not goal_blink_state
        goal_blink_start = time.time()

    if goal_blink_state:
        pygame.draw.rect(screen, GREEN, (goal_pos[0] * CELL_SIZE, goal_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    pygame.draw.rect(screen, RED, (player_pos[0] * CELL_SIZE, player_pos[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    timer_text_surface = pygame.Surface((250, 50))
    timer_text_surface.fill(YELLOW)
    screen.blit(timer_text_surface, (10, HEIGHT - 60))

    time_text = font.render(f'Time Left: {remaining_time}s', True, BLACK)
    screen.blit(time_text, (20, HEIGHT - 50))

    pygame.display.flip()

def display_game_over_screen(screen, font, message):
    screen.fill(WHITE)
    text_lines = [
        message,
        "Press 'R' to Restart",
        "Press 'Q' to Quit"
    ]
    text_surfaces = [font.render(line, True, BLACK) for line in text_lines]
    total_height = sum(text_surface.get_height() for text_surface in text_surfaces)
    y_start = HEIGHT // 2 - total_height // 2
    for text_surface in text_surfaces:
        screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, y_start))
        y_start += text_surface.get_height()
    pygame.display.flip()

def show_main_menu(screen, font):
    while True:
        screen.fill(WHITE)
        text_lines = [
            "Main Menu",
            "Press 'S' to Start",
            "Press 'I' for Instructions",
            "Press 'D' for Difficulty",
            "Press 'Q' to Quit"
        ]
        text_surfaces = [font.render(line, True, BLACK) for line in text_lines]
        total_height = sum(text_surface.get_height() for text_surface in text_surfaces)
        y_start = HEIGHT // 2 - total_height // 2
        for text_surface in text_surfaces:
            screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, y_start))
            y_start += text_surface.get_height()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    return "start"
                if event.key == pygame.K_i:
                    return "instructions"
                if event.key == pygame.K_d:
                    return "difficulty"
                if event.key == pygame.K_q:
                    pygame.quit()
                    return None

def show_difficulty_menu(screen, font):
    difficulty = 'medium'
    while True:
        screen.fill(WHITE)
        text_lines = [
            "Select Difficulty",
            "Press 'E' for Easy",
            "Press 'M' for Medium",
            "Press 'H' for Hard",
            "Press 'B' to Back"
        ]
        text_surfaces = [font.render(line, True, BLACK) for line in text_lines]
        total_height = sum(text_surface.get_height() for text_surface in text_surfaces)
        y_start = HEIGHT // 2 - total_height // 2
        for text_surface in text_surfaces:
            screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, y_start))
            y_start += text_surface.get_height()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    difficulty = 'easy'
                    return difficulty
                if event.key == pygame.K_m:
                    difficulty = 'medium'
                    return difficulty
                if event.key == pygame.K_h:
                    difficulty = 'hard'
                    return difficulty
                if event.key == pygame.K_b:
                    return None

def show_instructions(screen, font):
    while True:
        screen.fill(WHITE)
        text_lines = [
            "Instructions",
            "Use arrow keys or WASD to move",
            "Reach the green goal to win",
            "Press 'P' to Pause",
            "Press 'Q' to Quit"
        ]
        text_surfaces = [font.render(line, True, BLACK) for line in text_lines]
        total_height = sum(text_surface.get_height() for text_surface in text_surfaces)
        y_start = HEIGHT // 2 - total_height // 2
        for text_surface in text_surfaces:
            screen.blit(text_surface, (WIDTH // 2 - text_surface.get_width() // 2, y_start))
            y_start += text_surface.get_height()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    return
                if event.key == pygame.K_i:
                    return

def game_loop(screen, font, difficulty):
    settings = DIFFICULTY_SETTINGS[difficulty]
    maze_width = settings['maze_width']
    maze_height = settings['maze_height']
    timer_duration = settings['timer_duration']
    min_distance = settings['min_distance']

    global goal_blink_time, goal_blink_state, goal_blink_start

    goal_blink_time = 0.5
    goal_blink_state = True
    goal_blink_start = time.time()

    maze = generate_maze(maze_width, maze_height)
    goal_x, goal_y = generate_goal(maze, min_distance)
    player_x, player_y = 0, 0
    target_x, target_y = player_x, player_y
    animation_progress = 1.0
    animation_speed = 15

    start_time = time.time()

    clock = pygame.time.Clock()
    running = True
    paused = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    return False

        if not paused:
            keys = pygame.key.get_pressed()
            if animation_progress >= 1.0:
                new_x, new_y = player_x, player_y
                if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and int(player_x) > 0 and maze[int(player_y)][int(player_x) - 1] == 0:
                    new_x = player_x - 1
                if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and int(player_x) < maze_width - 1 and maze[int(player_y)][int(player_x) + 1] == 0:
                    new_x = player_x + 1
                if (keys[pygame.K_UP] or keys[pygame.K_w]) and int(player_y) > 0 and maze[int(player_y) - 1][int(player_x)] == 0:
                    new_y = player_y - 1
                if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and int(player_y) < maze_height - 1 and maze[int(player_y) + 1][int(player_x)] == 0:
                    new_y = player_y + 1

                if (new_x, new_y) != (player_x, player_y):
                    target_x, target_y = new_x, new_y
                    animation_progress = 0.0

            if animation_progress < 1.0:
                animation_progress += animation_speed / FPS
                animation_progress = min(animation_progress, 1.0)

                player_x = player_x + (target_x - player_x) * animation_progress
                player_y = player_y + (target_y - player_y) * animation_progress

            elapsed_time = time.time() - start_time
            remaining_time = max(0, timer_duration - int(elapsed_time))

            if int(player_x) == goal_x and int(player_y) == goal_y:
                display_game_over_screen(screen, font, "Congratulations! You reached the goal!")
                pygame.display.flip()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                return True
                            if event.key == pygame.K_q:
                                pygame.quit()
                                return False

            if remaining_time <= 0:
                display_game_over_screen(screen, font, "Time's up! Game Over.")
                pygame.display.flip()
                while True:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return False
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_r:
                                return True
                            if event.key == pygame.K_q:
                                pygame.quit()
                                return False

            draw_maze(screen, maze, (int(player_x), int(player_y)), (goal_x, goal_y), remaining_time, font)
            clock.tick(FPS)

def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze Game")
    font = pygame.font.SysFont(None, 36)

    while True:
        menu_choice = show_main_menu(screen, font)
        if menu_choice == "instructions":
            show_instructions(screen, font)
        elif menu_choice == "difficulty":
            difficulty = show_difficulty_menu(screen, font)
            if difficulty is None:
                continue
        elif menu_choice == "start":
            if difficulty is None:
                difficulty = 'medium'  # Default difficulty if none selected
            if not game_loop(screen, font, difficulty):
                break

    pygame.quit()

if __name__ == "__main__":
    main()
