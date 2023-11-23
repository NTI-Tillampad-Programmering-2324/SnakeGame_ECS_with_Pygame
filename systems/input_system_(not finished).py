
class InputSystem:
    def __init__(self):
        pass

    def update(self, entity, event):
        # Assuming the entity passed is the snake
        dir_component = entity.components[DirectionComponent]

        # Handle KEYDOWN events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and dir_component.dy == 0:
                dir_component.dx, dir_component.dy = 0, -CELL_SIZE
            elif event.key == pygame.K_DOWN and dir_component.dy == 0:
                dir_component.dx, dir_component.dy = 0, CELL_SIZE
            elif event.key == pygame.K_LEFT and dir_component.dx == 0:
                dir_component.dx, dir_component.dy = -CELL_SIZE, 0
            elif event.key == pygame.K_RIGHT and dir_component.dx == 0:
                dir_component.dx, dir_component.dy = CELL_SIZE, 0
