import pygame
import random

pygame.init()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WIDTH = 1500
HEIGHT = 800
FPS = 60 
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()
bird_width = 40
bird_height = 40
bird_x = 60
bird_y = HEIGHT // 2
bird_vel_y = 0
gravity = 0.5
jump_strength = -10
pipe_width = 60
pipe_gap = 150
pipe_vel_x = -5
score = 0
font = pygame.font.SysFont('Arial', 32)
def draw_bird(y):
    pygame.draw.rect(screen, RED   , (bird_x, y, bird_width, bird_height))
def draw_pipes(pipes):
    for pipe in pipes:
        pygame.draw.rect(screen, BLACK  , pipe['top'])
        pygame.draw.rect(screen, BLACK, pipe['bottom'])
def move_pipes(pipes):
    for pipe in pipes:
        pipe['top'].x += pipe_vel_x
        pipe['bottom'].x += pipe_vel_x
def generate_pipe():
    gap_position = random.randint(150, HEIGHT - 150)
    top = pygame.Rect(WIDTH, 0, pipe_width, gap_position)
    bottom = pygame.Rect(WIDTH, gap_position + pipe_gap, pipe_width, HEIGHT - gap_position - pipe_gap)
    return {'top': top, 'bottom': bottom}
def check_collision(bird, pipes):
    for pipe in pipes:
        if bird.colliderect(pipe['top']) or bird.colliderect(pipe['bottom']):
            return True
    if bird.top <= 0 or bird.bottom >= HEIGHT:
        return True
    return False
def game():
    global bird_y, bird_vel_y, score
    bird_rect = pygame.Rect(bird_x, bird_y, bird_width, bird_height)
    pipes = []
    add_pipe_event = pygame.USEREVENT + 1
    pygame.time.set_timer(add_pipe_event, 1500)
    running = True
    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_vel_y = jump_strength
            if event.type == add_pipe_event:
                pipes.append(generate_pipe())
        bird_vel_y += gravity
        bird_y += bird_vel_y
        bird_rect.y = bird_y
        move_pipes(pipes)
        pipes = [pipe for pipe in pipes if pipe['top'].x > -pipe_width]
        for pipe in pipes:
            if pipe['top'].x == bird_x:
                score += 1
        if check_collision(bird_rect, pipes):
            running = False
        draw_bird(bird_y)
        draw_pipes(pipes)
        score_text = font.render(f"Skorun: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
game()
