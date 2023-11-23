from components import PositionComponent, RenderComponent


class RenderSystem:
    """
    A system responsible for rendering entities on the screen.

    Attributes:
    -----------
    pygame_module : module
        The Pygame module used for rendering.
    cell_size : int
        The size of each cell in pixels.

    Methods:
    --------
    update(entity, screen)
        Renders the given entity on the given screen.
    """

    def __init__(self, pygame_module, cell_size):
        """
        Initializes a new instance of the RenderSystem class.

        Args:
            pygame_module (module): The Pygame module to use for rendering.
            cell_size (int): The size of each cell in the game grid.
        """
        self.cell_size = cell_size
        self.pygame_module = pygame_module

    def update(self, entity, screen):
        """
        Update the position and render components of an entity on the screen.

        Args:
            entity (Entity): The entity to be updated.
            screen (pygame.Surface): The surface to render the entity on.
        """
        pos = entity.components[PositionComponent]
        render = entity.components[RenderComponent]
        self.pygame_module.draw.rect(
            screen, render.color, (pos.x, pos.y, self.cell_size, self.cell_size)
        )
