import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
MAZE_WIDTH = WIDTH // CELL_SIZE
MAZE_HEIGHT = HEIGHT // CELL_SIZE
FPS = 30
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

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

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

def generate_goal(maze, min_distance=10):
    while True:
        goal_x = random.randint(0, MAZE_WIDTH - 1)
        goal_y = random.randint(0, MAZE_HEIGHT - 1)
        if maze[goal_y][goal_x] == 0 and (goal_x, goal_y) != (0, 0):
            distance = abs(goal_x - 0) + abs(goal_y - 0)
            if distance >= min_distance:
                return goal_x, goal_y

maze = generate_maze(MAZE_WIDTH, MAZE_HEIGHT)
goal_x, goal_y = generate_goal(maze)

player_x, player_y = 0, 0
target_x, target_y = player_x, player_y
animation_speed = 0.1
moving = False

start_time = time.time()
timer_duration = 60  

font = pygame.font.SysFont(None, 48)

goal_blink_time = 0.5
goal_blink_state = True
goal_blink_start = time.time()

def draw_maze(maze, player_pos, goal_pos, remaining_time):
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

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    new_x, new_y = player_x, player_y
    if keys[pygame.K_LEFT] and player_x > 0 and maze[player_y][player_x - 1] == 0:
        new_x = player_x - 1
        moving = True
    if keys[pygame.K_RIGHT] and player_x < MAZE_WIDTH - 1 and maze[player_y][player_x + 1] == 0:
        new_x = player_x + 1
        moving = True
    if keys[pygame.K_UP] and player_y > 0 and maze[player_y - 1][player_x] == 0:
        new_y = player_y - 1
        moving = True
    if keys[pygame.K_DOWN] and player_y < MAZE_HEIGHT - 1 and maze[player_y + 1][player_x] == 0:
        new_y = player_y + 1
        moving = True

    if moving:
        target_x, target_y = new_x, new_y
        moving = False

    elapsed_time = time.time() - start_time
    remaining_time = max(0, timer_duration - int(elapsed_time))

    if player_x != target_x or player_y != target_y:
        dx = (target_x - player_x) * animation_speed
        dy = (target_y - player_y) * animation_speed
        player_x += dx
        player_y += dy
        if abs(player_x - target_x) < 1 and abs(player_y - target_y) < 1:
            player_x, player_y = target_x, target_y
    else:
        player_x, player_y = int(player_x), int(player_y)

    if (player_x, player_y) == (goal_x, goal_y):
        print("Congratulations! You reached the goal!")
        running = False

    if remaining_time <= 0:
        print("Time's up! Game Over.")
        running = False

    draw_maze(maze, (int(player_x), int(player_y)), (goal_x, goal_y), remaining_time)

    clock.tick(FPS)

pygame.quit()
