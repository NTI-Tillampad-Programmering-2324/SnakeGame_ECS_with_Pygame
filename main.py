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
# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("ECS Snake Game")
clock = pygame.time.Clock()

# Initialize the game entities

# Create the snake entity and add suitable components
snake = Entity()
snake.add_component(PositionComponent(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
snake.add_component(DirectionComponent(CELL_SIZE, 0))
snake.add_component(RenderComponent(pygame.Color("green")))
snake.add_component(TailComponent())

# Create the food entity and add suitable components
food = Entity()
food.add_component(
    PositionComponent(
        random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE,
        random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE,
    )
)
food.add_component(RenderComponent(pygame.Color("red")))

entities = [snake, food]

# Initialize systems
movement_system = MovementSystem()
render_system = RenderSystem(pygame, CELL_SIZE)
collision_system = CollisionSystem()

# Initialize snake with a small tail
initial_position = (
    snake.components[PositionComponent].x,
    snake.components[PositionComponent].y,
)
snake.components[TailComponent].segments = [initial_position, initial_position]

# GAME LOOP
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
        (snake.components[PositionComponent].x, snake.components[PositionComponent].y),
    )
    tail.pop()

    movement_system.update(snake)

    # Boundary Check
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
        # Ensure the food doesn't overlap with the snake's body
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

pygame.quit()
