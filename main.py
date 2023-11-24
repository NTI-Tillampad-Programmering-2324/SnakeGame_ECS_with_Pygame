from config import SCREEN_WIDTH, SCREEN_HEIGHT, CELL_SIZE
from entities import Entity
from components import (
    PositionComponent,
    TailComponent,
    DirectionComponent,
    RenderComponent,
)
from systems import MovementSystem, RenderSystem, CollisionSystem
import random
import pygame

# INITIALIZE
pygame.init()
pygame.font.init()
game_font = pygame.font.SysFont("Arial", 30)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ECS Snake Game")
clock = pygame.time.Clock()


# Function to initialize the game entities and systems
def initialize_game():
    snake = Entity()
    snake.add_component(PositionComponent(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    snake.add_component(DirectionComponent(CELL_SIZE, 0))
    snake.add_component(RenderComponent(pygame.Color("green")))
    snake.add_component(TailComponent())

    food = Entity()
    food.add_component(
        PositionComponent(
            random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
            random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE,
        )
    )
    food.add_component(RenderComponent(pygame.Color("red")))

    entities = [snake, food]
    movement_system = MovementSystem()
    render_system = RenderSystem(pygame, CELL_SIZE)
    collision_system = CollisionSystem()

    initial_position = (
        snake.components[PositionComponent].x,
        snake.components[PositionComponent].y,
    )
    snake.components[TailComponent].segments = [initial_position, initial_position]

    return snake, food, entities, movement_system, render_system, collision_system


# Start screen function
def start_screen():
    waiting_for_start = True
    while waiting_for_start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting_for_start = False

        screen.fill(pygame.Color("black"))
        start_text = game_font.render("Press Enter to Start", True, (255, 255, 255))
        screen.blit(
            start_text,
            (SCREEN_WIDTH // 2 - start_text.get_width() // 2, SCREEN_HEIGHT // 2),
        )
        pygame.display.flip()
        clock.tick(15)
    return True


# Game over screen function
def game_over_screen(score):
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True

        screen.fill(pygame.Color("black"))
        score_text = game_font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(
            score_text,
            (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50),
        )
        game_over_text = game_font.render(
            "Game Over! Press Enter to Restart", True, (255, 255, 255)
        )
        screen.blit(
            game_over_text,
            (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2),
        )
        pygame.display.flip()
        clock.tick(15)

    return False


game_started = False
game_active = True
while game_active:
    score = 0
    if not game_started:
        if not start_screen():
            break
        game_started = True

    (
        snake,
        food,
        entities,
        movement_system,
        render_system,
        collision_system,
    ) = initialize_game()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_active = False
            if event.type == pygame.KEYDOWN:
                dir = snake.components[DirectionComponent]
                if event.key == pygame.K_UP and dir.dy == 0:
                    dir.dx, dir.dy = 0, -CELL_SIZE
                elif event.key == pygame.K_DOWN and dir.dy == 0:
                    dir.dx, dir.dy = 0, CELL_SIZE
                elif event.key == pygame.K_LEFT and dir.dx == 0:
                    dir.dx, dir.dy = -CELL_SIZE, 0
                elif event.key == pygame.K_RIGHT and dir.dx == 0:
                    dir.dx, dir.dy = CELL_SIZE, 0

        tail = snake.components[TailComponent].segments
        tail.insert(
            0,
            (
                snake.components[PositionComponent].x,
                snake.components[PositionComponent].y,
            ),
        )
        tail.pop()

        movement_system.update(snake)

        snake_pos = snake.components[PositionComponent]
        if (
            snake_pos.x < 0
            or snake_pos.x >= SCREEN_WIDTH
            or snake_pos.y < 0
            or snake_pos.y >= SCREEN_HEIGHT
        ):
            running = False

        if collision_system.check_collision(snake, food, PositionComponent):
            food.components[PositionComponent].x = (
                random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE
            )
            food.components[PositionComponent].y = (
                random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
            )
            while (
                food.components[PositionComponent].x,
                food.components[PositionComponent].y,
            ) in tail:
                food.components[PositionComponent].x = (
                    random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE
                )
                food.components[PositionComponent].y = (
                    random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
                )
            score += 1
            tail.append(
                (
                    snake.components[PositionComponent].x,
                    snake.components[PositionComponent].y,
                )
            )

        screen.fill(pygame.Color("black"))
        for entity in entities:
            render_system.update(entity, screen)

        for segment in tail:
            pygame.draw.rect(
                screen,
                pygame.Color("green"),
                (segment[0], segment[1], CELL_SIZE, CELL_SIZE),
            )

        pygame.display.flip()
        clock.tick(15)

    if not game_over_screen(score):
        break

pygame.quit()
