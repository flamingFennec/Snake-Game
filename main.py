import pygame
import random

# Initialize pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 600, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Snake attributes
BLOCK_SIZE = 20
SNAKE_SPEED = 10

# Game variables
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 25)

# Functions
def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(WIN, GREEN, (segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE))

def draw_food(food_pos):
    pygame.draw.rect(WIN, RED, (food_pos[0], food_pos[1], BLOCK_SIZE, BLOCK_SIZE))

def move_snake(snake, direction):
    if snake:  # Check if snake is not empty
        head = list(snake[0])
        if direction == "UP":
            head[1] -= BLOCK_SIZE
        elif direction == "DOWN":
            head[1] += BLOCK_SIZE
        elif direction == "LEFT":
            head[0] -= BLOCK_SIZE
        elif direction == "RIGHT":
            head[0] += BLOCK_SIZE
        snake.insert(0, head)
        return snake[:-1]  # Remove the last segment to keep the snake length
    return snake

def generate_food(snake):
    # Generate food position not on the snake's body
    while True:
        food_x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        food_y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        food_pos = (food_x, food_y)
        if food_pos not in snake:
            return food_pos

def is_collision(snake):
    head = snake[0]
    # Check if the head collides with any part of the snake's body, starting from index 1
    for segment in snake[1:]:
        if head == segment:
            return True
    return False

def check_food_collision(snake_head, food_pos):
    food_x, food_y = food_pos
    head_x, head_y = snake_head

    # Check if the coordinates of the snake's head overlap with the coordinates of the food
    if (food_x <= head_x <= food_x + BLOCK_SIZE) and (food_y <= head_y <= food_y + BLOCK_SIZE):
        return True
    return False

def game_loop():
    snake = [[WIDTH / 2, HEIGHT / 2]]  # Initialize the snake with a single segment at the center
    food_pos = generate_food(snake)
    direction = None
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    direction = "RIGHT"

        if snake:
            snake = move_snake(snake, direction)

        if is_collision(snake):
            print("Game Over! You hit yourself!")
            running = False

        if (snake[0][0] < 0 or snake[0][0] >= WIDTH or
            snake[0][1] < 0 or snake[0][1] >= HEIGHT):
            print("Game Over! You hit the wall!")
            running = False

        if check_food_collision(snake[0], food_pos):
            food_pos = generate_food(snake)
            score += 1
            # Add another segment to the snake's body at the tail position
            tail = snake[-1][:]
            snake.append(tail)

        WIN.fill(BLACK)
        draw_snake(snake)
        draw_food(food_pos)

        text = font.render("Score: " + str(score), True, WHITE)
        WIN.blit(text, [10, 10])

        pygame.display.update()
        clock.tick(SNAKE_SPEED)

    pygame.quit()

game_loop()
